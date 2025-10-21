"""Middleware components."""
from .origin_validator import OriginValidatorMiddleware, validate_origin_header

__all__ = ["OriginValidatorMiddleware", "validate_origin_header"]
