# API Reference

## Overview

PROMPTER provides a RESTful API and Python SDK for prompt management.

## Endpoints

### POST /api/enhance
Enhance a prompt with AI suggestions.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "model": "gpt-4",
  "options": {}
}
```

**Response:**
```json
{
  "enhanced": "Improved prompt...",
  "suggestions": [...],
  "metrics": {}
}
```

### Other endpoints
- GET /api/templates
- POST /api/versions
- GET /api/analytics

See full docs in code or Postman collection (coming soon).