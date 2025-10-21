"""API routes."""
from .mcp_routes import router as mcp_router
from .health_routes import router as health_router

__all__ = ["mcp_router", "health_router"]
