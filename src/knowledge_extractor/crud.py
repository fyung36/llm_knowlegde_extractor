from sqlmodel import Session
from src.db.models import Analysis
from sqlalchemy import func, String

class CreateService:
    def __init__(self, session: Session):
        self.session = session

    def create_analysis(self, text: str, summary: str, metadata: dict) -> Analysis:
        record = Analysis(
            text=text,
            summary=summary,
            title=metadata.get("title"),
            topics=metadata.get("topics", []),
            sentiment=metadata.get("sentiment"),
            keywords=metadata.get("keywords", [])
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def search_by_topic_or_keyword(self, query: str):
        query_lower = query.lower()
        return self.session.query(Analysis).filter(
            func.lower(Analysis.topics.cast(String)).like(f'%{query_lower}%') |
            func.lower(Analysis.keywords.cast(String)).like(f'%{query_lower}%')
        ).all()