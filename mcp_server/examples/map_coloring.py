"""
Map Coloring Problem using Gurddy CSP Solver

Color regions on a map such that no two adjacent regions have the same color.
This is a classic CSP problem demonstrating the Four Color Theorem.
"""

import gurddy

def solve_map_coloring():
    """Solve the classic Australia map coloring problem."""
    model = gurddy.Model("AustraliaMapColoring", "CSP")
    
    # Australian states and territories
    regions = ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS']
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    
    # Variables: one for each region
    region_vars = {}
    for region in regions:
        region_vars[region] = model.addVar(region, domain=list(range(len(colors))))
    
    # Adjacency relationships (which regions share borders)
    adjacencies = [
        ('WA', 'NT'), ('WA', 'SA'),
        ('NT', 'SA'), ('NT', 'QLD'),
        ('SA', 'QLD'), ('SA', 'NSW'), ('SA', 'VIC'),
        ('QLD', 'NSW'),
        ('NSW', 'VIC')
        # Note: TAS is an island, so no adjacencies
    ]
    
    # Constraint: Adjacent regions must have different colors
    def different_colors(color1, color2):
        return color1 != color2
    
    for region1, region2 in adjacencies:
        var1 = region_vars[region1]
        var2 = region_vars[region2]
        model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
    
    # Solve
    solution = model.solve()
    return solution, regions, colors, adjacencies

def solve_usa_map_coloring():
    """Solve a simplified USA map coloring problem."""
    model = gurddy.Model("USAMapColoring", "CSP")
    
    # Simplified US states (neighboring states)
    states = ['CA', 'NV', 'OR', 'AZ', 'UT', 'ID', 'WA']
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    
    # Variables
    state_vars = {}
    for state in states:
        state_vars[state] = model.addVar(state, domain=list(range(len(colors))))
    
    # Adjacencies (simplified)
    adjacencies = [
        ('CA', 'NV'), ('CA', 'OR'), ('CA', 'AZ'),
        ('NV', 'OR'), ('NV', 'AZ'), ('NV', 'UT'), ('NV', 'ID'),
        ('OR', 'WA'), ('OR', 'ID'),
        ('AZ', 'UT'),
        ('UT', 'ID'),
        ('ID', 'WA')
    ]
    
    # Constraints
    def different_colors(color1, color2):
        return color1 != color2
    
    for state1, state2 in adjacencies:
        var1 = state_vars[state1]
        var2 = state_vars[state2]
        model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
    
    solution = model.solve()
    return solution, states, colors, adjacencies

def print_map_solution(solution, regions, colors, adjacencies, map_name):
    """Print the map coloring solution."""
    if not solution:
        print(f"No solution found for {map_name}!")
        return
    
    print(f"\n{map_name} Map Coloring Solution:")
    print("=" * 40)
    
    for region in regions:
        color_idx = solution[region]
        color_name = colors[color_idx]
        print(f"{region:3}: {color_name}")
    
    print(f"\nAdjacency verification:")
    all_valid = True
    for region1, region2 in adjacencies:
        color1_idx = solution[region1]
        color2_idx = solution[region2]
        color1 = colors[color1_idx]
        color2 = colors[color2_idx]
        valid = color1_idx != color2_idx
        status = "✓" if valid else "✗"
        print(f"{region1}-{region2}: {color1} vs {color2} {status}")
        if not valid:
            all_valid = False
    
    print(f"\nSolution is {'VALID' if all_valid else 'INVALID'}")
    
    # Count colors used
    colors_used = len(set(solution[region] for region in regions))
    print(f"Colors used: {colors_used}/{len(colors)}")

def create_custom_map():
    """Create a custom map coloring problem."""
    print("\nCreating custom European countries map...")
    
    model = gurddy.Model("EuropeMapColoring", "CSP")
    
    countries = ['France', 'Germany', 'Italy', 'Spain', 'Switzerland', 'Austria', 'Belgium']
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    
    # Variables
    country_vars = {}
    for country in countries:
        country_vars[country] = model.addVar(country, domain=list(range(len(colors))))
    
    # European adjacencies (simplified)
    adjacencies = [
        ('France', 'Germany'), ('France', 'Italy'), ('France', 'Spain'), 
        ('France', 'Switzerland'), ('France', 'Belgium'),
        ('Germany', 'Austria'), ('Germany', 'Switzerland'), ('Germany', 'Belgium'),
        ('Italy', 'Switzerland'), ('Italy', 'Austria'),
        ('Switzerland', 'Austria')
    ]
    
    # Constraints
    def different_colors(color1, color2):
        return color1 != color2
    
    for country1, country2 in adjacencies:
        var1 = country_vars[country1]
        var2 = country_vars[country2]
        model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
    
    solution = model.solve()
    return solution, countries, colors, adjacencies

if __name__ == "__main__":
    # Solve Australia map coloring
    print("Solving Australia Map Coloring Problem...")
    solution, regions, colors, adjacencies = solve_map_coloring()
    print_map_solution(solution, regions, colors, adjacencies, "Australia")
    
    # Solve USA map coloring
    print("\n" + "="*60)
    print("Solving USA Map Coloring Problem...")
    solution, states, colors, adjacencies = solve_usa_map_coloring()
    print_map_solution(solution, states, colors, adjacencies, "USA (Western States)")
    
    # Solve custom European map
    print("\n" + "="*60)
    solution, countries, colors, adjacencies = create_custom_map()
    print_map_solution(solution, countries, colors, adjacencies, "Europe (Selected Countries)")