@echo off
REM Build script for Windows
REM This runs pre-build hooks, tests, then builds

echo Building gurddy-mcp package...

echo Running pre-build hooks...
python scripts/build_hook.py
if %ERRORLEVEL% NEQ 0 (
    echo Pre-build hooks failed!
    exit /b %ERRORLEVEL%
)

echo Running tests...
python -m pytest tests/ -v
if %ERRORLEVEL% NEQ 0 (
    echo Tests failed but continuing with build...
)

echo Building package...
python -m build %*

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)

echo Build completed successfully!