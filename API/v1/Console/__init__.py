from fastapi import APIRouter

from API.v1.VM.console import router as _vm_console

console_router = APIRouter()
console_router.include_router(_vm_console, tags=["vm"])
