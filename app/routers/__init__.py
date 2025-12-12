"""
Routers Package Initialization
Allows FastAPI to automatically recognize router modules.
"""

from .org import router as org_router
from .admin import router as admin_router

__all__ = ["org_router", "admin_router"]
