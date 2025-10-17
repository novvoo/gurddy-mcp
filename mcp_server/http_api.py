"""Lightweight HTTP wrapper for mcp_server exposing info, run-example and install endpoints.

Usage (development):
  uvicorn mcp_server.http_api:app --host 127.0.0.1 --port 8000
"""
from __future__ import annotations

import time
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mcp_server.handlers.gurddy import info as gurddy_info, run_example as run_example_fn, pip_install
from mcp_server.handlers.gurddy import solve_sudoku, solve_lp, solve_csp_generic, solve_production_planning
from mcp_server.handlers.gurddy import solve_n_queens, solve_graph_coloring, solve_map_coloring


app = FastAPI(title="mcp_server API")


class RunExampleRequest(BaseModel):
    example: str
    timeout_seconds: Optional[int] = 30


class SolveSudokuRequest(BaseModel):
    puzzle: list


class SolveLPRequest(BaseModel):
    problem: dict


class SolveCSPRequest(BaseModel):
    problem_type: str  # "n_queens", "graph_coloring", "map_coloring", "generic"
    parameters: dict


class SolveNQueensRequest(BaseModel):
    n: int = 8


class SolveGraphColoringRequest(BaseModel):
    edges: list  # List of [vertex1, vertex2] pairs
    num_vertices: int
    max_colors: int = 4


class SolveMapColoringRequest(BaseModel):
    regions: list  # List of region names
    adjacencies: list  # List of [region1, region2] pairs
    max_colors: int = 4


class SolveProductionRequest(BaseModel):
    profits: dict
    consumption: dict
    capacities: dict
    integer: Optional[bool] = True
    sensitivity_analysis: Optional[bool] = False


class InstallRequest(BaseModel):
    package: str
    upgrade: Optional[bool] = False


def _standardize_result(rc: Optional[int], output: Optional[str], start: float) -> dict:
    return {
        "success": (rc == 0) if rc is not None else False,
        "rc": rc,
        "output": output or "",
        "meta": {"time_seconds": time.time() - start},
    }


@app.get("/info")
async def get_info():
    return gurddy_info()


@app.post("/run-example")
async def run_example(req: RunExampleRequest):
    # Support all available examples
    valid_examples = [
        "lp", "csp", "n_queens", "graph_coloring", "map_coloring", 
        "scheduling", "logic_puzzles", "optimized_csp", "optimized_lp"
    ]
    
    if req.example not in valid_examples:
        raise HTTPException(
            status_code=400, 
            detail=f"example must be one of: {', '.join(valid_examples)}"
        )

    start = time.time()
    res = run_example_fn(req.example)
    rc = res.get("rc")
    out = res.get("output")
    return _standardize_result(rc, out, start)


@app.post("/install")
async def install(req: InstallRequest):
    # basic validation: package name simple whitelist pattern
    if not req.package or " " in req.package:
        raise HTTPException(status_code=400, detail="invalid package name")
    start = time.time()
    res = pip_install(req.package, upgrade=bool(req.upgrade))
    # pip_install currently returns {'success': 'true'/'false', 'output': str}
    success = res.get("success") == "true"
    out = res.get("output")
    rc = 0 if success else 1
    return _standardize_result(rc, out, start)


@app.post("/solve-sudoku")
async def solve_sudoku_route(req: SolveSudokuRequest):
    # basic validation performed inside handler
    start = time.time()
    res = solve_sudoku(req.puzzle)
    if not res.get("success"):
        return {"success": False, "rc": 1, "output": res.get("error"), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "solution": res.get("solution"), "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-lp')
async def solve_lp_route(req: SolveLPRequest):
    start = time.time()
    res = solve_lp(req.problem)
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    # success
    return {"success": True, "rc": 0, "output": "", "result": res, "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-csp')
async def solve_csp_route(req: SolveCSPRequest):
    start = time.time()
    res = solve_csp_generic(req.problem_type, req.parameters)
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "solution": res.get('solution'), "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-n-queens')
async def solve_n_queens_route(req: SolveNQueensRequest):
    start = time.time()
    res = solve_n_queens(req.n)
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "solution": res.get('solution'), "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-graph-coloring')
async def solve_graph_coloring_route(req: SolveGraphColoringRequest):
    start = time.time()
    res = solve_graph_coloring(req.edges, req.num_vertices, req.max_colors)
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "solution": res.get('solution'), "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-map-coloring')
async def solve_map_coloring_route(req: SolveMapColoringRequest):
    start = time.time()
    res = solve_map_coloring(req.regions, req.adjacencies, req.max_colors)
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "solution": res.get('solution'), "meta": {"time_seconds": time.time() - start}}


@app.post('/solve-production-planning')
async def solve_production_planning_route(req: SolveProductionRequest):
    start = time.time()
    res = solve_production_planning(
        req.profits, req.consumption, req.capacities, 
        req.integer, req.sensitivity_analysis
    )
    if not res.get('success'):
        return {"success": False, "rc": 1, "output": res.get('error'), "meta": {"time_seconds": time.time() - start}}
    return {"success": True, "rc": 0, "output": "", "result": res, "meta": {"time_seconds": time.time() - start}}
