# 게시판 프로젝트

이 프로젝트는 FastAPI, SQLAlchemy 및 Docker를 사용하여 구축된 게시판 애플리케이션입니다. 애플리케이션은 사용자 인증, 게시판 관리 및 게시물 관리를 지원하며, 페이지네이션 및 정렬과 같은 추가
기능도 포함하고 있습니다.

## 기능

- 사용자 인증 (회원가입, 로그인, 로그아웃)
- 게시판 관리 (생성, 수정, 삭제, 목록 조회)
- 게시물 관리 (생성, 수정, 삭제, 목록 조회)
- 페이지네이션 및 정렬
- Alembic을 사용한 자동 데이터베이스 마이그레이션

## 요구 사항

- Docker
- Docker Compose

## 설치

저장소를 클론합니다:

```bash
git clone https://github.com/yourusername/elice-board.git
cd elice-board
```

루트 디렉토리에 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

```env
DATABASE_URL=postgresql+asyncpg://admin:123456@db/elice-board
REDIS_URL=redis://redis/0
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### 애플리케이션 실행

poetry로 의존성을 설치합니다

Docker Compose를 사용하여 애플리케이션을 빌드하고 시작합니다:

```bash
docker-compose up --build -d
```

이 명령어는 다음을 수행합니다:

- FastAPI 애플리케이션 및 PostgreSQL 데이터베이스의 Docker 이미지를 빌드합니다.
- `docker-compose.yml` 파일에 정의된 컨테이너를 시작합니다.
- Alembic을 사용하여 데이터베이스 마이그레이션을 실행합니다.

애플리케이션은 `http://localhost:8000`에서 실행되고 있을 것입니다.

## API 문서

API 문서는 FastAPI에 의해 자동으로 생성되며, `http://localhost:8000/docs`에서 확인할 수 있습니다.

## 테스트 실행

애플리케이션 의존성이 개발 환경에 설치되어 있는지 확인합니다.

`.env` 파일을 열고 로컬 설정에 맞게 수정합니다.

`poetry`의 가상환경 파이썬 버젼을 설정합니다:

```bash
poetry env use 3.10.14
```


`poetry`를 사용하여 의존성을 설치합니다:

```bash
poetry install
```

`pytest`를 사용하여 테스트를 실행합니다:

```bash
pytest -v
```
