"""Basic tests for gurddy_mcp package."""

import pytest
from mcp_server.handlers.gurddy import solve_n_queens, solve_graph_coloring, info


def test_info():
    """Test the info function."""
    result = info()
    assert isinstance(result, dict)
    assert "name" in result
    assert "description" in result
    assert result["name"] == "gurddy"


def test_solve_n_queens():
    """Test N-Queens solver."""
    result = solve_n_queens(4)
    assert isinstance(result, dict)
    assert "success" in result
    assert "solution" in result
    
    if result["success"]:
        assert isinstance(result["solution"], list)
        assert len(result["solution"]) == 4


def test_solve_graph_coloring():
    """Test graph coloring solver."""
    # Simple triangle graph
    edges = [[0, 1], [1, 2], [2, 0]]
    result = solve_graph_coloring(edges, 3, 3)
    
    assert isinstance(result, dict)
    assert "success" in result
    assert "solution" in result
    
    if result["success"]:
        assert isinstance(result["solution"], list)
        assert len(result["solution"]) == 3


def test_package_import():
    """Test that the package can be imported correctly."""
    import mcp_server
    assert hasattr(mcp_server, '__version__')
    assert hasattr(mcp_server, 'solve_n_queens')
    assert hasattr(mcp_server, 'solve_graph_coloring')


if __name__ == "__main__":
    pytest.main([__file__])