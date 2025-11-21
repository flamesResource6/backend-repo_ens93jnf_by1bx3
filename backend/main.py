from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents
from schemas import Message, Project, TestPing

app = FastAPI(title="Venkata Sai Yandeti Portfolio API", version="1.0.0")

# CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test", response_model=TestPing)
async def test():
    return {"status": "ok"}


# Contact form submission
@app.post("/contact")
async def submit_contact(msg: Message):
    try:
        saved = await create_document("message", msg.model_dump())
        return {"ok": True, "message": "Thanks for reaching out!", "data": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Seed or list projects (simple showcase stored in DB)
class SeedProjectsRequest(BaseModel):
    items: list[Project]


@app.post("/projects/seed")
async def seed_projects(payload: SeedProjectsRequest):
    created = []
    for p in payload.items:
        created.append(await create_document("project", p.model_dump()))
    return {"count": len(created)}


@app.get("/projects")
async def list_projects(limit: int = 20):
    items = await get_documents("project", {}, limit)
    return {"items": items}
