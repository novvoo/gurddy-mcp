#!/usr/bin/env python3
"""MCP HTTP server wrapper for gurddy-mcp using streamable HTTP transport.

This server implements the Model Context Protocol (MCP) over HTTP with streaming support,
allowing it to be used as an MCP server via HTTP.
"""
from __future__ import annotations

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mcp_server.middleware import OriginValidatorMiddleware
from mcp_server.routes import mcp_router, health_router

# Import tools to register them
import mcp_server.tools.registry  # noqa: F401


app = FastAPI(
    title="Gurddy MCP HTTP Server",
    description="MCP server for Gurddy optimization library via streamable HTTP",
    version="0.1.8"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add origin validation middleware for DNS rebinding protection
app.add_middleware(
    OriginValidatorMiddleware,
    protected_paths=["/mcp/http"]
)

# Include routers
app.include_router(health_router)
app.include_router(mcp_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
