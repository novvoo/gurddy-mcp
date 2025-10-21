"""Health check and info routes."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "Gurddy MCP HTTP Server",
        "version": "0.1.8",
        "protocol": "MCP over Streamable HTTP",
        "transports": {
            "http": {
                "description": "Single request/response with optional streaming",
                "endpoint": "/mcp/http",
                "method": "POST",
                "streaming": "Add 'Accept: text/event-stream' or 'X-Stream: true' header"
            }
        },
        "examples": {
            "http_regular": "curl -X POST http://localhost:8080/mcp/http -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\",\"params\":{}}'",
            "http_streaming": "curl -X POST http://localhost:8080/mcp/http -H 'Content-Type: application/json' -H 'Accept: text/event-stream' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\",\"params\":{}}'"
        },
        "docs": "/docs - Interactive API documentation"
    }


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "gurddy-mcp"}
