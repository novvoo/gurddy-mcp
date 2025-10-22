# Gurddy MCP Server

[![PyPI version](https://badge.fury.io/py/gurddy-mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![Python Support](https://img.shields.io/pypi/pyversions/gurddy_mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-gurddy--mcp.fly.dev-blue)](https://gurddy-mcp.fly.dev)

A comprehensive Model Context Protocol (MCP) server for solving Constraint Satisfaction Problems (CSP), Linear Programming (LP), Minimax optimization, and SciPy-powered advanced optimization problems. Built on the `gurddy` optimization library with SciPy integration, it supports solving various classic problems through two MCP transports: stdio (for IDE integration) and streamable HTTP (for web clients).

**🚀 Quick Start (Stdio):** `pip install gurddy_mcp` then configure in your IDE

**🌐 Quick Start (HTTP):** `docker run -p 8080:8080 gurddy-mcp` or see deployment guide

**📦 PyPI Package:** [https://pypi.org/project/gurddy_mcp](https://pypi.org/project/gurddy_mcp)

## Main Features

### 🎯 CSP Problem Solving
- **N-Queens Problem**: Place N queens on an N×N chessboard with no attacks
- **Graph Coloring**: Assign colors to vertices so adjacent vertices differ
- **Map Coloring**: Color geographic regions with adjacent regions differing
- **Sudoku Solver**: Solve standard 9×9 Sudoku puzzles
- **Logic Puzzles**: Einstein's Zebra puzzle and custom logic problems
- **Scheduling**: Course scheduling, meeting scheduling, resource allocation
- **General CSP Solver**: Support for custom constraint satisfaction problems

### 📊 LP/Optimization Problems
- **Linear Programming**: Continuous variable optimization with linear constraints
- **Mixed Integer Programming**: Optimization with integer and continuous variables
- **Production Planning**: Resource-constrained production optimization with sensitivity analysis
- **Portfolio Optimization**: Investment allocation under risk constraints
- **Transportation Problems**: Supply chain and logistics optimization

### 🎮 Minimax/Game Theory
- **Zero-Sum Games**: Solve two-player games (Rock-Paper-Scissors, Matching Pennies, Battle of Sexes)
- **Mixed Strategy Nash Equilibria**: Find optimal probabilistic strategies
- **Robust Optimization**: Minimize worst-case loss under uncertainty
- **Maximin Decisions**: Maximize worst-case gain (conservative strategies)
- **Security Games**: Defender-attacker resource allocation
- **Robust Portfolio**: Minimize maximum loss across market scenarios
- **Production Planning**: Conservative production decisions (maximize minimum profit)
- **Advertising Competition**: Market share games and competitive strategies

### 🔬 SciPy Integration
- **Nonlinear Portfolio Optimization**: Quadratic risk models with SciPy optimization
- **Statistical Parameter Estimation**: Distribution fitting with constraints (MLE, quantile matching)
- **Signal Processing Optimization**: FIR filter design with frequency response optimization
- **Hybrid CSP-SciPy**: Discrete facility selection + continuous capacity optimization
- **Numerical Integration**: Optimization problems involving integrals and complex functions

### 🧮 Classic Math Problems
- **24-Point Game**: Find arithmetic expressions to reach 24 using four numbers
- **Chicken-Rabbit Problem**: Classic constraint problem with heads and legs
- **Mini Sudoku**: 4×4 Sudoku solver using CSP techniques
- **4-Queens Problem**: Simplified N-Queens for educational purposes
- **0-1 Knapsack**: Classic optimization problem with weight and value constraints

### 🔌 MCP Protocol Support
- **Stdio Transport**: Local IDE integration (Kiro, Claude Desktop, Cline, etc.)
- **Streamable HTTP Transport**: Web clients and remote access with optional streaming
- **Unified Interface**: Same tools across both transports
- **JSON-RPC 2.0**: Full protocol compliance
- **Auto-approval**: Configure trusted tools for seamless execution

## Installation

### From PyPI (Recommended)
```bash
# Install the latest stable version
pip install gurddy_mcp

# Or install with development dependencies
pip install gurddy_mcp[dev]
```

### From Source
```bash
# Clone the repository
git clone https://github.com/novvoo/gurddy-mcp.git
cd gurddy-mcp

# Install in development mode
pip install -e .

```

### Verify Installation
```bash
# Test MCP stdio server
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | gurddy-mcp
```

## Usage

### 1. MCP Stdio Server (Primary Interface)

The main `gurddy-mcp` command is an MCP stdio server that can be integrated with tools like Kiro.

#### Option A: Using uvx (Recommended - Always Latest Version)

Using `uvx` ensures you always run the latest published version without manual installation.

Configure in `~/.kiro/settings/mcp.json` or `.kiro/settings/mcp.json`:

**Recommended: Explicit latest version**
```json
{
  "mcpServers": {
    "gurddy": {
      "command": "uvx",
      "args": ["gurddy-mcp@latest"],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "run_example",
        "info",
        "install",
        "solve_n_queens",
        "solve_sudoku",
        "solve_graph_coloring",
        "solve_map_coloring",
        "solve_lp",
        "solve_production_planning",
        "solve_minimax_game",
        "solve_minimax_decision",
        "solve_24_point_game",
        "solve_chicken_rabbit_problem",
        "solve_scipy_portfolio_optimization",
        "solve_scipy_statistical_fitting",
        "solve_scipy_facility_location"
      ]
    }
  }
}
```

**Alternative: Without version specifier (also uses latest)**
```json
{
  "mcpServers": {
    "gurddy": {
      "command": "uvx",
      "args": ["gurddy-mcp"],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "run_example", "info", "install", "solve_n_queens", "solve_sudoku", 
        "solve_graph_coloring", "solve_map_coloring", "solve_lp", 
        "solve_production_planning", "solve_minimax_game", "solve_minimax_decision",
        "solve_24_point_game", "solve_chicken_rabbit_problem", 
        "solve_scipy_portfolio_optimization", "solve_scipy_statistical_fitting", 
        "solve_scipy_facility_location"
      ]
    }
  }
}
```

**Pin to specific version (if needed)**
```json
{
  "mcpServers": {
    "gurddy": {
      "command": "uvx",
      "args": ["gurddy-mcp==<VERSION>"],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "run_example", "info", "install", "solve_n_queens", "solve_sudoku", 
        "solve_graph_coloring", "solve_map_coloring", "solve_lp", 
        "solve_production_planning", "solve_minimax_game", "solve_minimax_decision",
        "solve_24_point_game", "solve_chicken_rabbit_problem", 
        "solve_scipy_portfolio_optimization", "solve_scipy_statistical_fitting", 
        "solve_scipy_facility_location"
      ]
    }
  }
}
```

**Why use uvx?**
- ✅ Always runs the latest published version automatically
- ✅ No manual installation or upgrade needed
- ✅ Isolated environment per execution
- ✅ No dependency conflicts with your system Python

**Prerequisites:** Install `uv` first:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Or using Homebrew (macOS)
brew install uv
```

#### Option B: Using Direct Command (After Installation)

If you've already installed `gurddy-mcp` via pip:

```json
{
  "mcpServers": {
    "gurddy": {
      "command": "gurddy-mcp",
      "args": [],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "run_example", "info", "install", "solve_n_queens", "solve_sudoku", 
        "solve_graph_coloring", "solve_map_coloring", "solve_lp", 
        "solve_production_planning", "solve_minimax_game", "solve_minimax_decision",
        "solve_24_point_game", "solve_chicken_rabbit_problem", 
        "solve_scipy_portfolio_optimization", "solve_scipy_statistical_fitting", 
        "solve_scipy_facility_location"
      ]
    }
  }
}
```

Available MCP tools (16 total):
- `info` - Get gurddy MCP server information and capabilities
- `install` - Install or upgrade the gurddy package
- `run_example` - Run example programs (n_queens, graph_coloring, minimax, scipy_optimization, classic_problems, etc.)
- `solve_n_queens` - Solve N-Queens problem for any board size
- `solve_sudoku` - Solve 9×9 Sudoku puzzles using CSP
- `solve_graph_coloring` - Solve graph coloring with configurable colors
- `solve_map_coloring` - Solve map coloring problems (e.g., Australia, USA)
- `solve_lp` - Solve Linear Programming (LP) or Mixed Integer Programming (MIP)
- `solve_production_planning` - Production optimization with optional sensitivity analysis
- `solve_minimax_game` - Two-player zero-sum games (find Nash equilibria)
- `solve_minimax_decision` - Robust optimization (minimize max loss or maximize min gain)
- `solve_24_point_game` - Solve 24-point game with four numbers using arithmetic operations
- `solve_chicken_rabbit_problem` - Solve classic chicken-rabbit problem with heads and legs constraints
- `solve_scipy_portfolio_optimization` - Solve nonlinear portfolio optimization using SciPy
- `solve_scipy_statistical_fitting` - Solve statistical parameter estimation using SciPy
- `solve_scipy_facility_location` - Solve facility location problem using hybrid CSP-SciPy approach

Test the MCP server:
```bash
# Test initialization
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | gurddy-mcp

# Test listing tools
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | gurddy-mcp

# Test info tools
echo '{"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"name":"info","arguments":{"":""}}}' | gurddy-mcp |jq 

# Test run example tools
echo '{"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"name":"run_example","arguments":{"example":"n_queens"}}}' | gurddy-mcp |jq

# Test sudoku tools
cat <<EOF | tr -d '\n'|gurddy-mcp|jq
{"jsonrpc":"2.0","id":123,"method":"tools/call","params":{
  "name":"solve_sudoku",
  "arguments":{
    "puzzle":[
      [5,3,0,0,7,0,0,0,0],
      [6,0,0,1,9,5,0,0,0],
      [0,9,8,0,0,0,0,6,0],
      [8,0,0,0,6,0,0,0,3],
      [4,0,0,8,0,3,0,0,1],
      [7,0,0,0,2,0,0,0,6],
      [0,6,0,0,0,0,2,8,0],
      [0,0,0,4,1,9,0,0,5],
      [0,0,0,0,8,0,0,7,9]
    ]
  }
}}
EOF
```

### 2. MCP HTTP Server

Start the HTTP MCP server (MCP protocol over streamable HTTP):

**Local Development:**
```bash
uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080
```

**Docker:**
```bash
# Build the image
docker build -t gurddy-mcp .

# Run the container
docker run -p 8080:8080 gurddy-mcp
```

**Access the server:**
- Root: http://127.0.0.1:8080/
- Health check: http://127.0.0.1:8080/health
- HTTP transport: http://127.0.0.1:8080/mcp/http (POST - supports both regular and streaming)

**Test the HTTP MCP server:**

**HTTP Transport (non-streaming):**
```bash
# List available tools
curl -X POST http://127.0.0.1:8080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Call a tool
curl -X POST http://127.0.0.1:8080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"info","arguments":{}}}'
```

**HTTP Transport (streaming with Accept header):**
```bash
# List tools with streaming response
curl -X POST http://127.0.0.1:8080/mcp/http \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Call a tool with streaming response
curl -X POST http://127.0.0.1:8080/mcp/http \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"solve_n_queens","arguments":{"n":4}}}'
```

**HTTP Transport (streaming with X-Stream header):**
```bash
# Alternative way to enable streaming
curl -X POST http://127.0.0.1:8080/mcp/http \
  -H "Content-Type: application/json" \
  -H "X-Stream: true" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"info","arguments":{}}}'
```

**Python Client Example:**
- `examples/streamable_http_client.py` - HTTP transport client with streaming examples


## MCP Tools

The server provides the following MCP tools:

### info
Get information about the gurddy package.
```json
{
  "name": "info",
  "arguments": {}
}
```

### install
Install or upgrade the gurddy package.
```json
{
  "name": "install",
  "arguments": {
    "package": "gurddy",
    "upgrade": false
  }
}
```

### run_example
Run a gurddy example.
```json
{
  "name": "run_example",
  "arguments": {
    "example": "n_queens"
  }
}
```
Available examples: `lp`, `csp`, `n_queens`, `graph_coloring`, `map_coloring`, `scheduling`, `logic_puzzles`, `optimized_csp`, `optimized_lp`, `minimax`, `scipy_optimization`, `classic_problems`

### solve_n_queens
Solve the N-Queens problem.
```json
{
  "name": "solve_n_queens",
  "arguments": {
    "n": 8
  }
}
```

### solve_sudoku
Solve a 9x9 Sudoku puzzle.
```json
{
  "name": "solve_sudoku",
  "arguments": {
    "puzzle": [[5,3,0,...], [6,0,0,...], ...]
  }
}
```

### solve_graph_coloring
Solve graph coloring problem.
```json
{
  "name": "solve_graph_coloring",
  "arguments": {
    "edges": [[0,1], [1,2], [2,0]],
    "num_vertices": 3,
    "max_colors": 3
  }
}
```

### solve_map_coloring
Solve map coloring problem.
```json
{
  "name": "solve_map_coloring",
  "arguments": {
    "regions": ["A", "B", "C"],
    "adjacencies": [["A", "B"], ["B", "C"]],
    "max_colors": 2
  }
}
```

### solve_lp
Solve a Linear Programming (LP) or Mixed Integer Programming (MIP) problem using PuLP.
```json
{
  "name": "solve_lp",
  "arguments": {
    "profits": {
      "ProductA": 30,
      "ProductB": 40
    },
    "consumption": {
      "ProductA": {"Labor": 2, "Material": 3},
      "ProductB": {"Labor": 3, "Material": 2}
    },
    "capacities": {
      "Labor": 100,
      "Material": 120
    },
    "integer": true
  }
}
```

### solve_production_planning
Solve a production planning optimization problem with optional sensitivity analysis.
```json
{
  "name": "solve_production_planning",
  "arguments": {
    "profits": {
      "ProductA": 30,
      "ProductB": 40
    },
    "consumption": {
      "ProductA": {"Labor": 2, "Material": 3},
      "ProductB": {"Labor": 3, "Material": 2}
    },
    "capacities": {
      "Labor": 100,
      "Material": 120
    },
    "integer": true,
    "sensitivity_analysis": false
  }
}
```

### solve_minimax_game
Solve a two-player zero-sum game using minimax (game theory).
```json
{
  "name": "solve_minimax_game",
  "arguments": {
    "payoff_matrix": [
      [0, -1, 1],
      [1, 0, -1],
      [-1, 1, 0]
    ],
    "player": "row"
  }
}
```
Returns the optimal mixed strategy and game value for the specified player.

### solve_minimax_decision
Solve a minimax decision problem under uncertainty (robust optimization).
```json
{
  "name": "solve_minimax_decision",
  "arguments": {
    "scenarios": [
      {"A": -0.2, "B": -0.1, "C": 0.05},
      {"A": 0.3, "B": 0.2, "C": -0.02},
      {"A": 0.05, "B": 0.03, "C": -0.01}
    ],
    "decision_vars": ["A", "B", "C"],
    "budget": 100.0,
    "objective": "minimize_max_loss"
  }
}
```
Objectives: `minimize_max_loss` (robust portfolio) or `maximize_min_gain` (conservative production)

### solve_24_point_game
Solve the 24-point game with four numbers using arithmetic operations.
```json
{
  "name": "solve_24_point_game",
  "arguments": {
    "numbers": [1, 2, 3, 4]
  }
}
```
Finds arithmetic expressions using +, -, *, / and parentheses to reach exactly 24.

### solve_chicken_rabbit_problem
Solve the classic chicken-rabbit problem with heads and legs constraints.
```json
{
  "name": "solve_chicken_rabbit_problem",
  "arguments": {
    "total_heads": 35,
    "total_legs": 94
  }
}
```
Determines the number of chickens (2 legs) and rabbits (4 legs) given total heads and legs.

### solve_scipy_portfolio_optimization
Solve nonlinear portfolio optimization using SciPy with quadratic risk models.
```json
{
  "name": "solve_scipy_portfolio_optimization",
  "arguments": {
    "expected_returns": [0.12, 0.18, 0.15],
    "covariance_matrix": [
      [0.04, 0.01, 0.02],
      [0.01, 0.09, 0.03],
      [0.02, 0.03, 0.06]
    ],
    "risk_tolerance": 1.0
  }
}
```
Optimizes portfolio weights to maximize return minus risk penalty using mean-variance optimization.

### solve_scipy_statistical_fitting
Solve statistical parameter estimation using SciPy with distribution fitting.
```json
{
  "name": "solve_scipy_statistical_fitting",
  "arguments": {
    "data": [1.2, 2.3, 1.8, 2.1, 1.9, 2.4, 1.7, 2.0],
    "distribution": "normal"
  }
}
```
Fits statistical distributions ("normal", "exponential", "uniform") to data and provides goodness-of-fit tests.

### solve_scipy_facility_location
Solve facility location problem using hybrid CSP-SciPy approach.
```json
{
  "name": "solve_scipy_facility_location",
  "arguments": {
    "customer_locations": [[0, 0], [10, 10], [5, 15]],
    "customer_demands": [100, 150, 80],
    "facility_locations": [[2, 3], [8, 12], [6, 8]],
    "max_facilities": 2,
    "fixed_cost": 100.0
  }
}
```
Combines discrete facility selection (CSP) with continuous capacity optimization (SciPy) to minimize total cost.

## Docker Deployment

### Build and Run
```bash
# Build the image
docker build -t gurddy-mcp .

# Run the container
docker run -p 8080:8080 gurddy-mcp

# Or with environment variables
docker run -p 8080:8080 -e PORT=8080 gurddy-mcp
```

### Docker Compose
```yaml
version: '3.8'
services:
  gurddy-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

## Example Output

### N-Queens Problem
```bash
POST /solve-n-queens
{
"n": 8
}
```



## Project Structure

```
mcp_server/
├── handlers/
│   └── gurddy.py           # Core solver implementation (16 MCP tools)
│                          # - solve_24_point_game, solve_chicken_rabbit_problem
│                          # - solve_scipy_portfolio_optimization, solve_scipy_statistical_fitting
│                          # - solve_scipy_facility_location, and 11 other solvers
├── tools/                  # MCP tool wrappers
├── examples/               # Rich Problem Examples
│   ├── n_queens.py         # N-Queens Problem
│   ├── graph_coloring.py   # Graph Coloring Problem
│   ├── map_coloring.py     # Map Coloring Problem
│   ├── logic_puzzles.py    # Logic Puzzles
│   ├── scheduling.py       # Scheduling Problem
│   ├── scipy_optimization.py # SciPy Integration Examples
│   │                      # - Portfolio optimization, statistical fitting, facility location
│   ├── classic_problems.py # Classic Math Problems
│   │                      # - 24-point game, chicken-rabbit problem, mini sudoku
│   ├── optimized_csp.py    # Advanced CSP techniques
│   ├── optimized_lp.py     # Linear programming examples
│   └── minimax.py          # Game theory and robust optimization
├── mcp_stdio_server.py     # MCP Stdio Server (for IDE integration)
└── mcp_http_server.py      # MCP HTTP Server (for web clients)

examples/
└── http_mcp_client.py      # Example HTTP MCP client

Dockerfile                  # Docker configuration for HTTP server
```

## MCP Transports

| Transport | Command | Protocol | Use Case |
|-----------|---------|----------|----------|
| **Stdio** | `gurddy-mcp` | MCP over stdin/stdout | IDE integration (Kiro, Claude Desktop, etc.) |
| **Streamable HTTP** | `uvicorn mcp_server.mcp_http_server:app` | MCP over HTTP with optional streaming | Web clients, remote access, Docker deployment |

All transports implement the same MCP protocol and provide identical tools.

### HTTP Transport Features

**HTTP Transport** (`/mcp/http` endpoint):
- Single request-response pattern
- Optional streaming: Add `Accept: text/event-stream` or `X-Stream: true` header
- Simpler for one-off requests
- Compatible with standard HTTP clients
- No connection state to manage
- Supports both regular JSON responses and SSE-formatted streaming responses

## Example Output

### N-Queens Problem
```bash
$ gurddy-mcp-cli run-example n_queens

Solving 8-Queens problem...

8-Queens Solution:
+---+---+---+---+---+---+---+---+
| Q |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | Q |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   | Q |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   | Q |   |   |
+---+---+---+---+---+---+---+---+
|   |   | Q |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   | Q |   |
+---+---+---+---+---+---+---+---+
|   | Q |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | Q |   |   |   |   |
+---+---+---+---+---+---+---+---+
Queen positions: (0,0), (1,4), (2,7), (3,5), (4,2), (5,6), (6,1), (7,3)
```

### Logic Puzzles
```bash
$ python -m mcp_server.server run-example logic_puzzles

Solving Simple Logic Puzzle:
Solution:
Position 1: Alice has Cat in Green house
Position 2: Bob has Dog in Red house  
Position 3: Carol has Fish in Blue house

Solving the Famous Zebra Puzzle (Einstein's Riddle)...
ANSWERS:
Who owns the zebra? Ukrainian (House 5)
Who drinks water? Japanese (House 2)
```

## HTTP API Examples

### Classic Problem Solving

#### Australian Map Coloring
```python
import requests

response = requests.post("http://127.0.0.1:8080/solve-map-coloring", json={ 
"regions": ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS'], 
"adjacencies": [ 
['WA', 'NT'], ['WA', 'SA'], ['NT', 'SA'], ['NT', 'QLD'], 
['SA', 'QLD'], ['SA', 'NSW'], ['SA', 'VIC'], 
['QLD', 'NSW'], ['NSW', 'VIC'] 
], 
"max_colors": 4
})
```

#### 8-Queens Problem
```python
response = requests.post("http://127.0.0.1:8080/solve-n-queens",
json={"n": 8})
```

## Available Examples

All examples can be run using `gurddy-mcp run-example <name>` or `python -m mcp_server.server run-example <name>`:

### CSP Examples ✅
- **n_queens** - N-Queens problem (4, 6, 8 queens with visual board display)
- **graph_coloring** - Graph coloring (Triangle, Square, Petersen graph, Wheel graph)
- **map_coloring** - Map coloring (Australia, USA Western states, Europe)
- **scheduling** - Scheduling problems (Course scheduling, meeting scheduling, resource allocation)
- **logic_puzzles** - Logic puzzles (Simple logic puzzle, Einstein's Zebra puzzle)
- **optimized_csp** - Advanced CSP techniques (Sudoku solver)

### LP Examples ✅
- **lp** / **optimized_lp** - Linear programming examples:
  - Portfolio optimization with risk constraints
  - Transportation problem (supply chain optimization)
  - Constraint relaxation analysis
  - Performance comparison across problem sizes

### Minimax Examples ✅
- **minimax** - Minimax optimization and game theory:
  - Rock-Paper-Scissors (zero-sum game)
  - Matching Pennies (coordination game)
  - Battle of the Sexes (mixed strategy equilibrium)
  - Robust portfolio optimization (minimize maximum loss)
  - Production planning (maximize minimum profit)
  - Security resource allocation (defender-attacker game)
  - Advertising competition (market share game)

### SciPy Integration Examples ✅ 
- **scipy_optimization** - Advanced optimization with SciPy:
  - Nonlinear portfolio optimization with quadratic risk models
  - Statistical parameter estimation (distribution fitting with constraints)
  - Signal processing optimization (FIR filter design)
  - Hybrid CSP-SciPy facility location (discrete + continuous optimization)
  - Numerical integration in optimization objectives

### Classic Math Problems ✅ 
- **classic_problems** - Educational math problem solving:
  - 24-Point Game (arithmetic expressions to reach 24)
  - Chicken-Rabbit Problem (classic constraint satisfaction)
  - 4×4 Mini Sudoku (simplified CSP demonstration)
  - 4-Queens Problem (educational N-Queens variant)
  - 0-1 Knapsack Problem (classic optimization)

### Supported Problem Types

#### 🧩 CSP Problems
- **N-Queens**: Classic N-Queens problem for any board size (N=4 to N=100+)
- **Graph Coloring**: Vertex coloring for arbitrary graphs (triangle, Petersen, wheel, etc.)
- **Map Coloring**: Geographic region coloring (Australia, USA, Europe maps)
- **Sudoku**: Standard 9×9 Sudoku puzzles with constraint propagation
- **Logic Puzzles**: Einstein's Zebra puzzle and custom logical reasoning problems
- **Scheduling**: Course scheduling, meeting rooms, resource allocation with time constraints

#### 📈 Optimization Problems
- **Linear Programming**: Continuous variable optimization with linear constraints
- **Integer Programming**: Discrete variable optimization (production quantities, assignments)
- **Mixed Integer Programming**: Combined continuous and discrete variables
- **Production Planning**: Multi-product resource-constrained optimization
- **Portfolio Optimization**: Investment allocation with risk and return constraints
- **Transportation**: Supply chain optimization (warehouses to customers)

#### 🎲 Game Theory & Robust Optimization
- **Zero-Sum Games**: Rock-Paper-Scissors, Matching Pennies, Battle of Sexes
- **Mixed Strategy Nash Equilibria**: Optimal probabilistic strategies for both players
- **Minimax Decisions**: Minimize worst-case loss across uncertainty scenarios
- **Maximin Decisions**: Maximize worst-case gain (conservative strategies)
- **Robust Portfolio**: Minimize maximum loss across market scenarios
- **Security Games**: Defender-attacker resource allocation problems

#### 🔬 SciPy-Powered Advanced Optimization 
- **Nonlinear Portfolio Optimization**: Quadratic risk models with Sharpe ratio maximization
- **Statistical Parameter Estimation**: MLE and quantile-based distribution fitting with constraints
- **Signal Processing**: FIR filter design with frequency response optimization
- **Hybrid Optimization**: Combine Gurddy CSP with SciPy continuous optimization
- **Numerical Integration**: Optimization problems involving complex mathematical functions

#### 🧮 Classic Educational Problems 
- **24-Point Game**: Find arithmetic expressions using four numbers to reach 24
- **Chicken-Rabbit Problem**: Classic constraint satisfaction with heads and legs
- **Mini Sudoku**: 4×4 Sudoku solving using CSP techniques
- **N-Queens Variants**: Educational versions of the classic problem
- **Knapsack Problems**: 0-1 knapsack optimization with weight and value constraints

## Performance Features

- **Fast Solution**: Millisecond response for small-medium problems (N-Queens N≤12, graphs <50 vertices)
- **Scalable**: Handles large problems (N-Queens N=100+, LP with 1000+ variables)
- **Memory Efficient**: Backtracking search and constraint propagation minimize memory usage
- **Extensible**: Custom constraints, objective functions, and problem types
- **Concurrency-Safe**: HTTP API supports concurrent request processing
- **Production Ready**: Docker deployment, health checks, error handling

## Performance Benchmarks

Typical execution times on standard hardware:
- **CSP Examples**: 0.4-0.5s (N-Queens, Graph Coloring, Logic Puzzles)
- **LP Examples**: 0.8-0.9s (Portfolio, Transportation, Production Planning)
- **Minimax Examples**: 0.3-0.5s (Game solving, Robust optimization)
- **SciPy Examples**: 0.5-1.2s (Nonlinear optimization, Statistical fitting)
- **Classic Problems**: 0.1-0.3s (24-point, Chicken-rabbit, Mini sudoku)
- **Sudoku**: <0.1s for standard 9×9 puzzles
- **Large N-Queens**: ~2-3s for N=100

## Troubleshooting

### Common Errors
- `"gurddy package not available"`: Install with `python -m mcp_server.server install`
- `"No solution found"`: No solution exists under given constraints; try relaxing constraints
- `"Invalid input types"`: Check the data types of input parameters
- `"Unknown example"`: Use `python -m mcp_server.server run-example --help` to see available examples

### Installation Issues
```bash
# install individually
pip install gurddy pulp>=2.6.0 scipy>=1.9.0 numpy>=1.21.0

# Check installation
python -c "import gurddy, pulp, scipy, numpy; print('All dependencies installed')"
```

### Example Debugging
Run examples directly for debugging:
```bash
# After installing gurddy_mcp
python -c "from mcp_server.examples import n_queens; n_queens.main()"

# Or from source - CSP examples
python mcp_server/examples/n_queens.py
python mcp_server/examples/graph_coloring.py
python mcp_server/examples/logic_puzzles.py
python mcp_server/examples/optimized_csp.py

# LP and optimization examples
python mcp_server/examples/optimized_lp.py

# Game theory and minimax examples
python mcp_server/examples/minimax.py

# SciPy integration examples (includes portfolio, statistical fitting, facility location)
python mcp_server/examples/scipy_optimization.py

# Classic math problems (includes 24-point game, chicken-rabbit problem)
python mcp_server/examples/classic_problems.py

# Test individual MCP tools directly
python -c "from mcp_server.handlers.gurddy import solve_24_point_game; print(solve_24_point_game([1,2,3,4]))"
python -c "from mcp_server.handlers.gurddy import solve_chicken_rabbit_problem; print(solve_chicken_rabbit_problem(35, 94))"
python -c "from mcp_server.handlers.gurddy import solve_scipy_portfolio_optimization; print(solve_scipy_portfolio_optimization([0.12, 0.18], [[0.04, 0.01], [0.01, 0.09]]))"
```

### SciPy Integration Requirements
The SciPy integration examples require additional dependencies:
```bash
# Install SciPy and NumPy 
pip install scipy>=1.9.0 numpy>=1.21.0

# Verify SciPy integration
python -c "import scipy.optimize, numpy; print('SciPy integration ready')"
```

**SciPy Examples Include:**
- **Nonlinear Portfolio Optimization**: Quadratic risk models with Sharpe ratio maximization
- **Statistical Parameter Estimation**: Distribution fitting with MLE and quantile methods
- **Signal Processing**: FIR filter design with frequency response optimization
- **Hybrid CSP-SciPy**: Facility location combining discrete and continuous optimization
- **Numerical Integration**: Complex optimization problems involving integrals

## Development

### Architecture

The project uses a **centralized tool registry** to ensure consistency between stdio and HTTP servers:

- **Single Source of Truth**: `mcp_server/tool_registry.py` defines all tools
- **Stdio Server**: `mcp_server/mcp_stdio_server.py` (for IDE integration)
- **HTTP Server**: `mcp_server/mcp_http_server.py` (for web clients)
- **Handlers**: `mcp_server/handlers/gurddy.py` (tool implementations)


### Adding a New Tool

1. **Implement handler** in `mcp_server/handlers/gurddy.py`:
   ```python
   def my_new_tool(param1: str, param2: int = 10) -> Dict[str, Any]:
       """Tool implementation."""
       return {"result": "success"}
   ```

2. **Register in central registry** (`mcp_server/tool_registry.py`):
   ```python
   {
       "name": "my_new_tool",
       "function": "my_new_tool",
       "description": "Description of what the tool does",
       "category": "optimization",
       "module": "handlers.gurddy",
       "inputSchema": {
           "type": "object",
           "properties": {
               "param1": {"type": "string", "description": "First parameter"},
               "param2": {"type": "integer", "description": "Second parameter", "default": 10}
           },
           "required": ["param1"]
       }
   }
   ```

3. **Verify consistency**:
   ```bash
   python scripts/verify_consistency.py
   pytest tests/test_consistency.py -v
   ```

That's it! Both stdio and HTTP servers will automatically pick up the new tool.

### Custom Constraints
```python
# Define a custom constraint in gurddy
def custom_constraint(var1, var2):
    return var1 + var2 <= 10

model.addConstraint(gurddy.FunctionConstraint(custom_constraint, (var1, var2)))
```

### Testing

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/test_consistency.py -v
pytest tests/test_tool_registry.py -v

# Verify tool registry consistency
python scripts/verify_consistency.py
```

## License

This project is licensed under an open source license. Please see the LICENSE file for details.
