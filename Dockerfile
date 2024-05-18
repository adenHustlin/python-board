FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY pyproject.toml ./

RUN apt-get update && apt-get -y install --no-install-recommends build-essential
RUN pip install poetry

# 종속성 설치
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# 애플리케이션 코드 복사
COPY . .

# entrypoint.sh 복사 및 실행 권한 부여
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 권한 확인
RUN ls -l /app/entrypoint.sh

# 포트 노출
EXPOSE 8000

# entrypoint.sh 스크립트를 실행
ENTRYPOINT ["/app/entrypoint.sh"]
