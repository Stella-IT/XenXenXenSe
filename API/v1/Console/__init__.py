from fastapi import APIRouter

from API.v1.Console.info import router as _console_router

console_router = APIRouter()
console_router.include_router(_console_router, tags=["console"])
