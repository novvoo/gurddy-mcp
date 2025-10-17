"""
Graph Coloring Problem using Gurddy CSP Solver

Given a graph, assign colors to vertices such that no two adjacent 
vertices have the same color, using the minimum number of colors.
"""

import gurddy

def solve_graph_coloring(edges, num_vertices, max_colors=4):
    """
    Solve graph coloring problem.
    
    Args:
        edges: List of tuples representing edges (vertex1, vertex2)
        num_vertices: Number of vertices in the graph
        max_colors: Maximum number of colors to try
    """
    model = gurddy.Model("GraphColoring", "CSP")
    
    # Variables: one for each vertex, domain is available colors
    vertices = {}
    for v in range(num_vertices):
        var_name = f"vertex_{v}"
        vertices[var_name] = model.addVar(var_name, domain=list(range(max_colors)))
    
    # Constraints: Adjacent vertices must have different colors
    def different_colors(color1, color2):
        return color1 != color2
    
    for v1, v2 in edges:
        var1 = vertices[f"vertex_{v1}"]
        var2 = vertices[f"vertex_{v2}"]
        model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
    
    # Solve
    solution = model.solve()
    return solution

def find_minimum_colors(edges, num_vertices):
    """Find the minimum number of colors needed (chromatic number)."""
    for colors in range(1, num_vertices + 1):
        print(f"Trying with {colors} colors...")
        solution = solve_graph_coloring(edges, num_vertices, colors)
        if solution:
            return solution, colors
    return None, num_vertices

def print_coloring(solution, edges, num_vertices):
    """Print the graph coloring solution."""
    if not solution:
        print("No solution found!")
        return
    
    color_names = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown']
    
    print("\nGraph Coloring Solution:")
    for v in range(num_vertices):
        color_idx = solution[f"vertex_{v}"]
        color_name = color_names[color_idx] if color_idx < len(color_names) else f"Color{color_idx}"
        print(f"Vertex {v}: {color_name}")
    
    print("\nEdge verification:")
    for v1, v2 in edges:
        color1 = solution[f"vertex_{v1}"]
        color2 = solution[f"vertex_{v2}"]
        status = "✓" if color1 != color2 else "✗"
        print(f"Edge ({v1},{v2}): {color_names[color1]} - {color_names[color2]} {status}")

# Example graphs
def get_sample_graphs():
    """Return some sample graphs to test."""
    graphs = {
        "Triangle": {
            "edges": [(0, 1), (1, 2), (2, 0)],
            "vertices": 3,
            "description": "Complete graph K3 (triangle)"
        },
        "Square": {
            "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
            "vertices": 4,
            "description": "4-cycle (square)"
        },
        "Petersen": {
            "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # outer pentagon
                     (5, 6), (6, 7), (7, 8), (8, 9), (9, 5),  # inner pentagon
                     (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)], # connections
            "vertices": 10,
            "description": "Petersen graph"
        },
        "Wheel": {
            "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # rim
                     (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)], # spokes to center
            "vertices": 6,
            "description": "Wheel graph W5"
        }
    }
    return graphs

if __name__ == "__main__":
    graphs = get_sample_graphs()
    
    for name, graph_data in graphs.items():
        print(f"\n{'='*50}")
        print(f"Solving {name}: {graph_data['description']}")
        print(f"Vertices: {graph_data['vertices']}, Edges: {len(graph_data['edges'])}")
        
        solution, min_colors = find_minimum_colors(
            graph_data['edges'], 
            graph_data['vertices']
        )
        
        if solution:
            print(f"Chromatic number: {min_colors}")
            print_coloring(solution, graph_data['edges'], graph_data['vertices'])
        else:
            print("Failed to find a solution!")