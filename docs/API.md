# API Reference

## `POST /api/enhance`

Enhances a prompt into a more structured version and returns simple quality metrics.

### Request

```json
{
  "prompt": "Summarize our customer interview notes.",
  "goal": "Improve specificity",
  "audience": "GPT-4 class model",
  "constraints": ["Return bullet points", "Keep it under 200 words"]
}
```

## `GET /api/templates`

Returns the built-in prompt templates.

## `GET /api/versions`

Returns all saved prompt versions.

## `POST /api/versions`

Stores a version with title, notes, tags, and prompt text.

## `GET /api/analytics`

Returns aggregate run statistics for enhancement requests.

## `GET /api/settings`

Returns runtime settings including the data directory, host, port, and application version.
