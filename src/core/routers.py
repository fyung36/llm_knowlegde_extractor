from src.knowledge_extractor.routes import router

def register_routers(app):
    app.include_router(router, prefix="/api", tags=["app"])
