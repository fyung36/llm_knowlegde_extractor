import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="src.app:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        forwarded_allow_ips="*",
        proxy_headers=True,
    )
