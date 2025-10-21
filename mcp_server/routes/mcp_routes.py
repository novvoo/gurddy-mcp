"""MCP protocol routes."""
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from mcp_server.core import MCPHTTPServer

router = APIRouter(prefix="/mcp", tags=["mcp"])

# Global MCP server instance
mcp_server = MCPHTTPServer()


@router.post("/http")
async def http_transport_endpoint(request: Request):
    """HTTP transport: Send MCP messages via HTTP (supports both streaming and non-streaming responses).
    
    - Without streaming headers: Returns a single JSON response
    - With 'Accept: text/event-stream' or 'X-Stream: true': Returns streaming SSE-formatted response
    """
    # Check if client accepts streaming response
    accept_header = request.headers.get("Accept", "")
    wants_stream = "text/event-stream" in accept_header or request.headers.get("X-Stream", "").lower() == "true"
    
    try:
        body = await request.json()
        
        # If client wants streaming, return a streaming response
        if wants_stream:
            async def stream_response():
                try:
                    response = await mcp_server.handle_request(body)
                    if response:
                        # Send the response as SSE format
                        yield f"data: {json.dumps(response)}\n\n"
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    yield f"data: {json.dumps(error_response)}\n\n"
            
            return StreamingResponse(
                stream_response(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"
                }
            )
        else:
            # Regular non-streaming response
            response = await mcp_server.handle_request(body)
            # Return empty response for notifications
            return response if response else {"status": "ok"}
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        }
