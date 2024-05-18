from fastapi import HTTPException


def raise_not_found(detail: str, code: int = 4041):
    raise HTTPException(status_code=404, detail={"error": detail, "code": code})


def raise_forbidden(detail: str, code: int = 4031):
    raise HTTPException(status_code=403, detail={"error": detail, "code": code})


def raise_bad_request(detail: str, code: int = 4001):
    raise HTTPException(status_code=400, detail={"error": detail, "code": code})


def raise_unauthorized(detail: str, code: int = 4011):
    raise HTTPException(
        status_code=401,
        detail={"error": detail, "code": code},
        headers={"WWW-Authenticate": "Bearer"},
    )
