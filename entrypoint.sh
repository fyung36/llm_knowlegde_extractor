#!/bin/bash -xe

alembic upgrade head
uvicorn src.app:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips='*' --proxy-headers
