# Gurddy MCP Server

[![PyPI version](https://badge.fury.io/py/gurddy-mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![Python Support](https://img.shields.io/pypi/pyversions/gurddy_mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-gurddy--mcp.fly.dev-blue)](https://gurddy-mcp.fly.dev)

A Model Context Protocol (MCP) server providing solutions for Constraint Satisfaction Problems (CSP) and Linear Programming (LP). Built on the `gurddy` optimization library, it supports solving a variety of classic problems through two MCP transports: stdio (for IDE integration) and HTTP/SSE (for web clients).

**🚀 Quick Start (Stdio):** `pip install gurddy_mcp` then configure in your IDE

**🌐 Quick Start (HTTP):** `docker run -p 8080:8080 gurddy-mcp` or see deployment guide

**📦 PyPI Package:** [https://pypi.org/project/gurddy_mcp](https://pypi.org/project/gurddy_mcp)

## Main Features

### CSP Problem Solving
- **N-Queens Problem**: Place N queens on an N×N chessboard so that they do not attack each other
- **Graph Coloring Problem**: Assign colors to graph vertices so that adjacent vertices have different colors
- **Map Coloring Problem**: Assign colors to map regions so that adjacent regions have different colors
- **Sudoku Solving**: Solve 9×9 Sudoku puzzles
- **General CSP Solver**: Supports custom constraint satisfaction problems

### LP/Optimization Problems
- **Linear Programming**: Solve optimization problems with linear objective functions and constraints
- **Production Planning**: Solve production optimization problems under resource constraints
- **Integer Programming**: Supports optimization problems with integer variables

### MCP Protocol Support
- **Stdio Transport**: For local IDE integration (Kiro, Claude Desktop, etc.)
- **HTTP/SSE Transport**: For web-based clients and remote access
- Unified tool interface across both transports
- Full JSON-RPC 2.0 compliance

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

# Or install dependencies manually
pip install -r requirements.txt
```

### Verify Installation
```bash
# Test MCP stdio server
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | gurddy-mcp
```

## Usage

### 1. MCP Stdio Server (Primary Interface)

The main `gurddy-mcp` command is an MCP stdio server that can be integrated with tools like Kiro:

Configure in `~/.kiro/settings/mcp.json` or `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "gurddy": {
      "command": "gurddy-mcp",
      "args": [],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "run_example",
        "info",
        "install",
        "solve_n_queens",
        "solve_sudoku",
        "solve_graph_coloring",
        "solve_map_coloring"
      ]
    }
  }
}
```

Available MCP tools:
- `info` - Get gurddy package information
- `install` - Install or upgrade the gurddy package
- `run_example` - Run example programs (n_queens, graph_coloring, etc.)
- `solve_n_queens` - Solve N-Queens problem
- `solve_sudoku` - Solve Sudoku puzzles
- `solve_graph_coloring` - Solve graph coloring problems
- `solve_map_coloring` - Solve map coloring problems

Test the MCP server:
```bash
# Test initialization
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | gurddy-mcp

# Test listing tools
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | gurddy-mcp
```

### 2. MCP HTTP Server

Start the HTTP MCP server (MCP protocol over HTTP/SSE):

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
- SSE endpoint: http://127.0.0.1:8080/sse
- Message endpoint: http://127.0.0.1:8080/message (POST)

**Test the HTTP MCP server:**
```bash
# List available tools
curl -X POST http://127.0.0.1:8080/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Call a tool
curl -X POST http://127.0.0.1:8080/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"info","arguments":{}}}'
```

**Python Client Example:**
See `examples/http_mcp_client.py` for a complete example of how to interact with the HTTP MCP server.

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
Available examples: `lp`, `csp`, `n_queens`, `graph_coloring`, `map_coloring`, `scheduling`, `logic_puzzles`, `optimized_csp`, `optimized_lp`

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
│   └── gurddy.py           # Core solver implementation
├── tools/                  # MCP tool wrappers
├── examples/               # Rich CSP Problem Examples
│   ├── n_queens.py         # N-Queens Problem
│   ├── graph_coloring.py   # Graph Coloring Problem
│   ├── map_coloring.py     # Map Coloring Problem
│   ├── logic_puzzles.py    # Logic Puzzles
│   └── scheduling.py       # Scheduling Problem
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
| **HTTP** | `uvicorn mcp_server.mcp_http_server:app` | MCP over HTTP/SSE | Web clients, remote access, Docker deployment |

Both transports implement the same MCP protocol and provide identical tools.

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

### Supported Problem Types

#### CSP Problems
- **N-Queens**: The classic N-Queens problem, supporting chessboards of any size
- **Graph Coloring**: Vertex coloring of arbitrary graph structures  
- **Map Coloring**: Coloring geographic regions, verifying the Four Color Theorem
- **Sudoku**: Solving standard 9×9 Sudoku puzzles
- **Logic Puzzles**: Including classic logical reasoning problems such as the Zebra Puzzle
- **Scheduling**: Course scheduling, meeting scheduling, resource allocation, etc.

#### Optimization Problems
- **Linear Programming**: Linear optimization with continuous variables
- **Integer Programming**: Optimization with discrete variables
- **Production Planning**: Production optimization under resource constraints
- **Mixed Integer Programming**: Optimization with a mix of continuous and discrete variables

## Performance Features

- **Fast Solution**: Typically completes in milliseconds for small to medium-sized problems (N-Queens with N ≤ 12, graph coloring with < 50 vertices)
- **Memory Efficient**: Uses backtracking search and constraint propagation, resulting in a small memory footprint.
- **Extensible**: Supports custom constraints and objective functions
- **Concurrency-Safe**: The HTTP API supports concurrent request processing

## Performance

All examples run efficiently:
- **CSP Examples**: 0.4-0.5 seconds (N-Queens, Graph Coloring, etc.)
- **LP Examples**: 0.8-0.9 seconds (Portfolio optimization, Transportation, etc.)

## Troubleshooting

### Common Errors
- `"gurddy package not available"`: Install with `python -m mcp_server.server install`
- `"No solution found"`: No solution exists under given constraints; try relaxing constraints
- `"Invalid input types"`: Check the data types of input parameters
- `"Unknown example"`: Use `python -m mcp_server.server run-example --help` to see available examples

### Installation Issues
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install gurddy>=0.1.6 pulp>=2.6.0

# Check installation
python -c "import gurddy, pulp; print('All dependencies installed')"
```

### Example Debugging
Run examples directly for debugging:
```bash
# After installing gurddy_mcp
python -c "from mcp_server.examples import n_queens; n_queens.main()"

# Or from source
python mcp_server/examples/n_queens.py
python mcp_server/examples/graph_coloring.py
python mcp_server/examples/logic_puzzles.py
```

## Extension Development

### Adding a New CSP Problem
1. In `mcp_server/examples/` Create a problem implementation in `mcp_server/handlers/gurddy.py`
2. Add the solver function in `mcp_server/handlers/gurddy.py`
3. Add the API endpoint in `mcp_server/http_api.py`

### Custom Constraints
```python
# Define a custom constraint in gurddy
def custom_constraint(var1, var2):
return var1 + var2 <= 10

model.addConstraint(gurddy.FunctionConstraint(custom_constraint, (var1, var2)))
```

## License

This project is licensed under an open source license. Please see the LICENSE file for details.
