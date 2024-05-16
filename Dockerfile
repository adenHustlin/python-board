# Dockerfile

FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY pyproject.toml poetry.lock ./

RUN apt-get update
RUN apt-get -y install build-essential
RUN pip install poetry

# 종속성 설치
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# 애플리케이션 코드 복사
COPY . .
