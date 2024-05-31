#!/bin/sh

# 데이터베이스 마이그레이션 리비전 생성 및 적용
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

# 애플리케이션 시작
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
