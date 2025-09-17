from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlmodel import Session
from src.db.main import get_session
from src.knowledge_extractor import llm, nlp_utils
from src.knowledge_extractor.crud import CreateService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze-ui", response_class=HTMLResponse)
async def analyze_ui(
    request: Request,
    text: str = Form(...),
    db: Session = Depends(get_session)
):
    try:
        if not text.strip():
            return HTMLResponse("<p>Error: Empty input.</p>")

        summary, metadata = llm.analyze_text(text)
        keywords = nlp_utils.extract_top_nouns(text)
        metadata["keywords"] = keywords

        record = CreateService.create_analysis(db, text, summary, metadata)

        return HTMLResponse(f"""
            <h3>Summary:</h3><p>{record.summary}</p>
            <p><b>Title:</b> {record.title}</p>
            <p><b>Topics:</b> {', '.join(record.topics)}</p>
            <p><b>Sentiment:</b> {record.sentiment}</p>
            <p><b>Keywords:</b> {', '.join(record.keywords)}</p>
        """)
    except Exception as e:
        return HTMLResponse(f"<p>Error: {str(e)}</p>")


@router.get("/search-ui", response_class=HTMLResponse)
async def search_ui(
    topic: str,
    db: Session = Depends(get_session)
):
    try:
        results = CreateService.search_by_topic_or_keyword(db, topic)

        if not results:
            return HTMLResponse("<p>No results found.</p>")

        html = "<ul>"
        for r in results:
            html += f"<li><b>{r.title or 'Untitled'}:</b> {r.summary}</li>"
        html += "</ul>"

        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"<p>Error: {str(e)}</p>")
