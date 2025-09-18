import logging
import os

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from sqlmodel import Session
from src.db.main import get_session
from src.knowledge_extractor import llm, nlp_utils
from src.knowledge_extractor.crud import CreateService

router = APIRouter()
logger = logging.getLogger("llm-analyzer")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze-ui", response_class=HTMLResponse)
async def analyze_ui(
    request: Request,
    text: str = Form(...),
    db: Session = Depends(get_session)
):
    if not text.strip():
        return HTMLResponse("<p style='color:red;'>Error: Empty input.</p>")

    try:
        summary, metadata = llm.analyze_text(text)
    except Exception as e:
        return HTMLResponse(f"<p style='color:red;'>LLM Error: {str(e)}</p>")

    try:
        keywords = nlp_utils.extract_top_nouns(text)
        metadata["keywords"] = keywords

        service = CreateService(db)
        record = service.create_analysis(text, summary, metadata)

        return HTMLResponse(f"""
            <h3>Summary:</h3><p>{record.summary}</p>
            <p><b>Title:</b> {record.title or "Untitled"}</p>
            <p><b>Topics:</b> {', '.join(record.topics)}</p>
            <p><b>Sentiment:</b> {record.sentiment}</p>
            <p><b>Keywords:</b> {', '.join(record.keywords)}</p>
        """)
    except Exception as e:
        logger.info(f"DB Error: {str(e)}")
        return HTMLResponse(f"<p style='color:red;'>Error saving analysis: {str(e)}</p>")


@router.post("/analyze")
async def analyze_text(text: str = Form(...), db: Session = Depends(get_session)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty.")
    try:
        summary, metadata = llm.analyze_text(text)
    except Exception as e:
        logger.error(f"DB Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"LLM API call failed: {str(e)}"}
        )

    keywords = nlp_utils.extract_top_nouns(text)
    metadata["keywords"] = keywords

    record = CreateService(db).create_analysis(text, summary, metadata)

    return {
        "summary": record.summary,
        "title": record.title,
        "topics": record.topics,
        "sentiment": record.sentiment,
        "keywords": record.keywords
    }


@router.get("/search-ui", response_class=HTMLResponse)
async def search_ui(
    topic: str,
    db: Session = Depends(get_session)
):
    try:
        create_servie = CreateService(db)
        results = create_servie.search_by_topic_or_keyword(topic)

        if not results:
            return HTMLResponse("<p>No results found.</p>")

        html = "<ul>"
        for r in results:
            html += f"<li><b>{r.title or 'Untitled'}:</b> {r.summary}</li>"
        html += "</ul>"

        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"<p>Error: {str(e)}</p>")
