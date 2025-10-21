"""Tests for HTTP routes and transports."""

import pytest
from fastapi.testclient import TestClient

from mcp_server.mcp_http_server import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestHealthRoutes:
    """Test health and info routes."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns server info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Gurddy MCP HTTP Server"
        assert data["version"] == "0.1.8"
        assert "transports" in data
        assert "http" in data["transports"]
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "gurddy-mcp"


class TestHTTPTransport:
    """Test HTTP transport endpoint."""
    
    def test_http_endpoint_exists(self, client):
        """Test that /mcp/http endpoint exists."""
        # Send a valid JSON-RPC request
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post("/mcp/http", json=payload)
        assert response.status_code == 200
    
    def test_http_list_tools(self, client):
        """Test listing tools via HTTP transport."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post("/mcp/http", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "jsonrpc" in data
        assert data["jsonrpc"] == "2.0"
        assert "result" in data or "error" in data
    
    def test_http_call_info_tool(self, client):
        """Test calling info tool via HTTP transport."""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "info",
                "arguments": {}
            }
        }
        response = client.post("/mcp/http", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "jsonrpc" in data
        assert data["jsonrpc"] == "2.0"
    
    def test_http_streaming_with_accept_header(self, client):
        """Test HTTP transport with streaming via Accept header."""
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        response = client.post(
            "/mcp/http",
            json=payload,
            headers={"Accept": "text/event-stream"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    
    def test_http_streaming_with_x_stream_header(self, client):
        """Test HTTP transport with streaming via X-Stream header."""
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/list",
            "params": {}
        }
        response = client.post(
            "/mcp/http",
            json=payload,
            headers={"X-Stream": "true"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    
    def test_http_invalid_json(self, client):
        """Test HTTP transport with invalid JSON."""
        response = client.post(
            "/mcp/http",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32700  # Parse error


class TestOriginValidation:
    """Test origin validation middleware."""
    
    def test_http_without_origin_header(self, client):
        """Test HTTP endpoint without Origin header (should pass)."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post("/mcp/http", json=payload)
        assert response.status_code == 200
    
    def test_http_with_localhost_origin(self, client):
        """Test HTTP endpoint with localhost Origin header."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post(
            "/mcp/http",
            json=payload,
            headers={"Origin": "http://localhost:8080"}
        )
        assert response.status_code == 200
    
    def test_http_with_127_origin(self, client):
        """Test HTTP endpoint with 127.0.0.1 Origin header."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post(
            "/mcp/http",
            json=payload,
            headers={"Origin": "http://127.0.0.1:8080"}
        )
        assert response.status_code == 200
    
    def test_http_with_invalid_origin(self, client):
        """Test HTTP endpoint with invalid Origin header."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        # TestClient raises HTTPException, so we need to catch it
        from fastapi import HTTPException
        try:
            response = client.post(
                "/mcp/http",
                json=payload,
                headers={"Origin": "http://malicious-site.com"}
            )
            # If we get here, check the status code
            assert response.status_code == 403
        except HTTPException as e:
            # Expected: middleware raises 403
            assert e.status_code == 403
            assert "Invalid Origin header" in str(e.detail)


class TestRouteNaming:
    """Test that old routes are removed and new routes work."""
    
    def test_old_message_route_not_found(self, client):
        """Test that old /message route no longer exists."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post("/message", json=payload)
        assert response.status_code == 404
    
    def test_http_route_works(self, client):
        """Test that /mcp/http route works."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = client.post("/mcp/http", json=payload)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
