"""Origin validation middleware for DNS rebinding protection."""
from typing import List
from urllib.parse import urlparse

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


ALLOWED_ORIGINS = ["localhost", "127.0.0.1", "0.0.0.0"]


def validate_origin_header(request: Request) -> bool:
    """Validate Origin header to prevent DNS rebinding attacks."""
    origin = request.headers.get("Origin")
    if origin is None:
        # If no Origin header, check Referer as fallback
        referer = request.headers.get("Referer")
        if referer is None:
            # No origin information, allow for same-origin requests
            return True
        origin = referer
    
    # Parse the origin to get the hostname
    try:
        parsed = urlparse(origin)
        hostname = parsed.hostname
        
        # Allow if hostname is None (file:// URLs) or in allowed list
        if hostname is None or hostname in ALLOWED_ORIGINS or hostname.endswith(".localhost"):
            return True
            
        # For local development, also allow local domains
        if hostname.startswith("127.0.0.") or hostname == "0.0.0.0":
            return True
            
        # Reject if origin is not allowed
        return False
    except Exception:
        # If we can't parse the origin, reject the request
        return False


class OriginValidatorMiddleware(BaseHTTPMiddleware):
    """Middleware to validate Origin header on POST requests."""
    
    def __init__(self, app, protected_paths: List[str] = None):
        super().__init__(app)
        self.protected_paths = protected_paths or ["/message"]
    
    async def dispatch(self, request: Request, call_next):
        # Only validate POST requests to protected paths (exact match or prefix match)
        if request.method == "POST" and any(
            request.url.path == path or request.url.path.startswith(path + "/")
            for path in self.protected_paths
        ):
            if not validate_origin_header(request):
                raise HTTPException(status_code=403, detail="Invalid Origin header")
        
        response = await call_next(request)
        return response
