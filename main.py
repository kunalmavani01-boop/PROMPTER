from __future__ import annotations

import json
import os
from collections import Counter
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from threading import RLock
from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


APP_NAME = "PROMPTER"
APP_VERSION = "1.1.0"
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DEFAULT_HOST = os.getenv("PROMPTER_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("PROMPTER_PORT", "8000"))


def resolve_data_dir() -> Path:
    override = os.getenv("PROMPTER_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()

    if os.name == "nt":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / APP_NAME

    if os.name == "posix" and "darwin" in os.sys.platform:
        return Path.home() / "Library" / "Application Support" / APP_NAME

    return Path.home() / ".local" / "share" / APP_NAME.lower()


DATA_DIR = resolve_data_dir()
STORE_PATH = DATA_DIR / "data.json"


class EnhanceRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    goal: str | None = Field(default="Improve clarity and usefulness")
    audience: str | None = Field(default="General-purpose LLM")
    constraints: list[str] = Field(default_factory=list)


class PromptVersionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    prompt: str = Field(min_length=1, max_length=8000)
    notes: str | None = Field(default="")
    tags: list[str] = Field(default_factory=list)


@dataclass
class TemplateRecord:
    id: str
    name: str
    category: str
    prompt: str


DEFAULT_TEMPLATES = [
    TemplateRecord(
        id="content-brief",
        name="Content Brief",
        category="Content",
        prompt=(
            "Act as a senior content strategist. Create a content brief for {topic} "
            "covering audience, message pillars, tone, call to action, and SEO angles."
        ),
    ),
    TemplateRecord(
        id="debug-assistant",
        name="Debug Assistant",
        category="Engineering",
        prompt=(
            "You are a careful software engineer. Diagnose the issue in {system}, "
            "list likely root causes, propose tests, and produce a fix plan."
        ),
    ),
    TemplateRecord(
        id="meeting-summary",
        name="Meeting Summary",
        category="Operations",
        prompt=(
            "Summarize the meeting notes into decisions, blockers, owners, deadlines, "
            "and next actions. Keep it concise and operational."
        ),
    ),
]


class DataStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = RLock()
        self.state: dict[str, list[dict[str, Any]]] = {
            "templates": [asdict(item) for item in DEFAULT_TEMPLATES],
            "versions": [],
            "analytics": [],
        }

    def load(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.save()
            return

        with self.lock:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            self.state["templates"] = payload.get("templates") or [asdict(item) for item in DEFAULT_TEMPLATES]
            self.state["versions"] = payload.get("versions", [])
            self.state["analytics"] = payload.get("analytics", [])

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock:
            self.path.write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    def get_templates(self) -> list[dict[str, Any]]:
        with self.lock:
            return list(self.state["templates"])

    def get_versions(self) -> list[dict[str, Any]]:
        with self.lock:
            return list(self.state["versions"])

    def get_analytics(self) -> list[dict[str, Any]]:
        with self.lock:
            return list(self.state["analytics"])

    def add_version(self, item: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            self.state["versions"].append(item)
            self.save()
            return item

    def add_analytics(self, item: dict[str, Any]) -> None:
        with self.lock:
            self.state["analytics"].append(item)
            self.save()


store = DataStore(STORE_PATH)


def score_prompt(text: str) -> dict[str, float]:
    words = [word for word in text.replace("\n", " ").split(" ") if word]
    sentences = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
    constraint_markers = sum(text.lower().count(token) for token in ["must", "should", "format", "include"])
    clarity = min(100.0, 45 + len(sentences) * 8 + constraint_markers * 4)
    specificity = min(100.0, 35 + len(words) * 0.9)
    structure = min(100.0, 30 + sum(text.count(ch) for ch in [":", "-", "\n"]) * 3)
    overall = round(mean([clarity, specificity, structure]), 1)
    return {
        "clarity": round(clarity, 1),
        "specificity": round(specificity, 1),
        "structure": round(structure, 1),
        "overall": overall,
    }


def build_enhanced_prompt(request: EnhanceRequest) -> tuple[str, list[str]]:
    suggestions: list[str] = []

    if len(request.prompt.split()) < 20:
        suggestions.append("Add more task context so the model knows what success looks like.")
    if "output" not in request.prompt.lower():
        suggestions.append("Specify the preferred output format to reduce ambiguous responses.")
    if not request.constraints:
        suggestions.append("Add constraints such as tone, length, or exclusions for tighter control.")

    constraint_lines = "\n".join(f"- {item}" for item in request.constraints) or "- No extra constraints provided."
    improved = (
        f"Task:\n{request.prompt.strip()}\n\n"
        f"Goal:\n{request.goal or 'Improve clarity and usefulness'}\n\n"
        f"Audience:\n{request.audience or 'General-purpose LLM'}\n\n"
        "Constraints:\n"
        f"{constraint_lines}\n\n"
        "Instructions:\n"
        "- Think step by step internally and return only the final answer.\n"
        "- Ask for clarification only if a missing detail blocks a reliable answer.\n"
        "- Produce a structured response with concise headings when useful.\n"
        "- Call out assumptions explicitly.\n"
        "- End with concrete next steps or recommendations."
    )
    return improved, suggestions


@asynccontextmanager
async def lifespan(_: FastAPI):
    store.load()
    yield
    store.save()


app = FastAPI(
    title=APP_NAME,
    description="Prompt optimization and management toolkit",
    version=APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("PROMPTER_CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION,
        "data_file": str(STORE_PATH),
    }


@app.get("/api/settings")
def settings() -> dict[str, Any]:
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
        "data_dir": str(DATA_DIR),
    }


@app.post("/api/enhance")
def enhance_prompt(payload: EnhanceRequest) -> dict[str, Any]:
    start = perf_counter()
    enhanced, suggestions = build_enhanced_prompt(payload)
    metrics = score_prompt(enhanced)
    duration_ms = round((perf_counter() - start) * 1000, 2)
    store.add_analytics(
        {
            "id": str(uuid4()),
            "source_length": len(payload.prompt),
            "enhanced_length": len(enhanced),
            "duration_ms": duration_ms,
            "score": metrics["overall"],
        }
    )
    return {
        "enhanced": enhanced,
        "suggestions": suggestions,
        "metrics": metrics,
        "processing_ms": duration_ms,
    }


@app.get("/api/templates")
def list_templates() -> dict[str, list[dict[str, Any]]]:
    return {"templates": store.get_templates()}


@app.get("/api/versions")
def list_versions() -> dict[str, list[dict[str, Any]]]:
    return {"versions": store.get_versions()}


@app.post("/api/versions")
def create_version(payload: PromptVersionCreate) -> dict[str, Any]:
    versions = store.get_versions()
    scores = score_prompt(payload.prompt)
    previous = versions[-1]["version"] if versions else "v0.0"
    major, minor = previous.removeprefix("v").split(".")
    version_label = f"v{major}.{int(minor) + 1}"
    item = {
        "id": str(uuid4()),
        "version": version_label,
        "title": payload.title,
        "prompt": payload.prompt,
        "notes": payload.notes,
        "tags": payload.tags,
        "metrics": scores,
    }
    return store.add_version(item)


@app.get("/api/analytics")
def analytics_summary() -> dict[str, Any]:
    analytics = store.get_analytics()
    versions = store.get_versions()
    if not analytics:
        return {
            "runs": 0,
            "average_score": 0,
            "average_duration_ms": 0,
            "top_tags": [],
        }

    tag_counter = Counter(tag for version in versions for tag in version["tags"])
    return {
        "runs": len(analytics),
        "average_score": round(mean(item["score"] for item in analytics), 1),
        "average_duration_ms": round(mean(item["duration_ms"] for item in analytics), 2),
        "top_tags": [{"tag": tag, "count": count} for tag, count in tag_counter.most_common(5)],
    }


@app.get("/api/versions/{version_id}")
def get_version(version_id: str) -> dict[str, Any]:
    for item in store.get_versions():
        if item["id"] == version_id:
            return item
    raise HTTPException(status_code=404, detail="Version not found")
