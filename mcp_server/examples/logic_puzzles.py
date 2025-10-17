"""
Logic Puzzles using Gurddy CSP Solver

Solve various logic puzzles including Zebra puzzle, Einstein's riddle, etc.
"""

import gurddy

def solve_zebra_puzzle():
    """
    Solve the classic Zebra puzzle (Einstein's riddle):
    
    There are 5 houses in a row, each with different color, nationality, drink, pet, and cigarette.
    Given clues, determine who owns the zebra and who drinks water.
    """
    model = gurddy.Model("ZebraPuzzle", "CSP")
    
    # 5 houses numbered 0-4 (left to right)
    houses = list(range(5))
    
    # Attributes
    colors = ['Red', 'Green', 'White', 'Yellow', 'Blue']
    nationalities = ['English', 'Spanish', 'Ukrainian', 'Norwegian', 'Japanese']
    drinks = ['Coffee', 'Tea', 'Milk', 'OrangeJuice', 'Water']
    pets = ['Dog', 'Snails', 'Fox', 'Horse', 'Zebra']
    cigarettes = ['OldGold', 'Kools', 'Chesterfields', 'LuckyStrike', 'Parliaments']
    
    # Variables: each attribute gets assigned to houses 0-4
    vars_dict = {}
    
    # Color variables
    for i, color in enumerate(colors):
        vars_dict[f'color_{color}'] = model.addVar(f'color_{color}', domain=houses)
    
    # Nationality variables  
    for i, nat in enumerate(nationalities):
        vars_dict[f'nat_{nat}'] = model.addVar(f'nat_{nat}', domain=houses)
    
    # Drink variables
    for i, drink in enumerate(drinks):
        vars_dict[f'drink_{drink}'] = model.addVar(f'drink_{drink}', domain=houses)
    
    # Pet variables
    for i, pet in enumerate(pets):
        vars_dict[f'pet_{pet}'] = model.addVar(f'pet_{pet}', domain=houses)
    
    # Cigarette variables
    for i, cig in enumerate(cigarettes):
        vars_dict[f'cig_{cig}'] = model.addVar(f'cig_{cig}', domain=houses)
    
    # Constraint: Each attribute appears exactly once (AllDifferent within each category)
    color_vars = [vars_dict[f'color_{c}'] for c in colors]
    nat_vars = [vars_dict[f'nat_{n}'] for n in nationalities]
    drink_vars = [vars_dict[f'drink_{d}'] for d in drinks]
    pet_vars = [vars_dict[f'pet_{p}'] for p in pets]
    cig_vars = [vars_dict[f'cig_{c}'] for c in cigarettes]
    
    model.addConstraint(gurddy.AllDifferentConstraint(color_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(nat_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(drink_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(pet_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(cig_vars))
    
    # Clue constraints
    def same_house(house1, house2):
        return house1 == house2
    
    def adjacent_houses(house1, house2):
        return abs(house1 - house2) == 1
    
    def to_the_right(house1, house2):
        return house1 == house2 + 1
    
    # Clue 1: The English person lives in the red house
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['nat_English'], vars_dict['color_Red'])
    ))
    
    # Clue 2: The Spanish person owns the dog
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['nat_Spanish'], vars_dict['pet_Dog'])
    ))
    
    # Clue 3: Coffee is drunk in the green house
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['drink_Coffee'], vars_dict['color_Green'])
    ))
    
    # Clue 4: The Ukrainian drinks tea
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['nat_Ukrainian'], vars_dict['drink_Tea'])
    ))
    
    # Clue 5: The green house is immediately to the right of the white house
    model.addConstraint(gurddy.FunctionConstraint(
        to_the_right, (vars_dict['color_Green'], vars_dict['color_White'])
    ))
    
    # Clue 6: The Old Gold smoker owns snails
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['cig_OldGold'], vars_dict['pet_Snails'])
    ))
    
    # Clue 7: Kools are smoked in the yellow house
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['cig_Kools'], vars_dict['color_Yellow'])
    ))
    
    # Clue 8: Milk is drunk in the middle house (house 2)
    def is_middle_house(house, dummy):
        return house == 2
    
    dummy_var = model.addVar("dummy", domain=[0])
    model.addConstraint(gurddy.FunctionConstraint(
        is_middle_house, (vars_dict['drink_Milk'], dummy_var)
    ))
    
    # Clue 9: The Norwegian lives in the first house (house 0)
    def is_first_house(house, dummy):
        return house == 0
    
    model.addConstraint(gurddy.FunctionConstraint(
        is_first_house, (vars_dict['nat_Norwegian'], dummy_var)
    ))
    
    # Clue 10: The Chesterfields smoker lives next to the fox owner
    model.addConstraint(gurddy.FunctionConstraint(
        adjacent_houses, (vars_dict['cig_Chesterfields'], vars_dict['pet_Fox'])
    ))
    
    # Clue 11: Kools are smoked next to the horse owner
    model.addConstraint(gurddy.FunctionConstraint(
        adjacent_houses, (vars_dict['cig_Kools'], vars_dict['pet_Horse'])
    ))
    
    # Clue 12: The Lucky Strike smoker drinks orange juice
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['cig_LuckyStrike'], vars_dict['drink_OrangeJuice'])
    ))
    
    # Clue 13: The Japanese person smokes Parliaments
    model.addConstraint(gurddy.FunctionConstraint(
        same_house, (vars_dict['nat_Japanese'], vars_dict['cig_Parliaments'])
    ))
    
    # Clue 14: The Norwegian lives next to the blue house
    model.addConstraint(gurddy.FunctionConstraint(
        adjacent_houses, (vars_dict['nat_Norwegian'], vars_dict['color_Blue'])
    ))
    
    solution = model.solve()
    return solution, vars_dict

def print_zebra_solution(solution, vars_dict):
    """Print the Zebra puzzle solution."""
    if not solution:
        print("No solution found for Zebra puzzle!")
        return
    
    print("\nZebra Puzzle Solution:")
    print("=" * 60)
    
    # Create house-to-attributes mapping
    houses_info = [[] for _ in range(5)]
    
    # Collect all attributes for each house
    for var_name, house in solution.items():
        if var_name.startswith('color_'):
            houses_info[house].append(('Color', var_name[6:]))
        elif var_name.startswith('nat_'):
            houses_info[house].append(('Nationality', var_name[4:]))
        elif var_name.startswith('drink_'):
            houses_info[house].append(('Drink', var_name[6:]))
        elif var_name.startswith('pet_'):
            houses_info[house].append(('Pet', var_name[4:]))
        elif var_name.startswith('cig_'):
            houses_info[house].append(('Cigarette', var_name[4:]))
    
    # Print house by house
    for house in range(5):
        print(f"\nHouse {house + 1}:")
        print("-" * 15)
        for attr_type, attr_value in sorted(houses_info[house]):
            print(f"  {attr_type:12}: {attr_value}")
    
    # Answer the questions
    zebra_house = solution['pet_Zebra']
    water_house = solution['drink_Water']
    
    # Find nationalities
    zebra_owner = None
    water_drinker = None
    for var_name, house in solution.items():
        if var_name.startswith('nat_'):
            if house == zebra_house:
                zebra_owner = var_name[4:]
            if house == water_house:
                water_drinker = var_name[4:]
    
    print(f"\n" + "="*60)
    print("ANSWERS:")
    print(f"Who owns the zebra? {zebra_owner} (House {zebra_house + 1})")
    print(f"Who drinks water? {water_drinker} (House {water_house + 1})")

def solve_simple_logic_puzzle():
    """Solve a simpler logic puzzle for demonstration."""
    print("\nSolving Simple Logic Puzzle:")
    print("Three friends (Alice, Bob, Carol) have different pets (Cat, Dog, Fish)")
    print("and live in different colored houses (Red, Blue, Green).")
    print("Clues:")
    print("1. Alice doesn't live in the red house")
    print("2. The person with the cat lives in the blue house") 
    print("3. Bob doesn't have the fish")
    print("4. Carol doesn't live in the green house")
    
    model = gurddy.Model("SimpleLogic", "CSP")
    
    # People, pets, house colors (encoded as 0, 1, 2)
    people = ['Alice', 'Bob', 'Carol']
    pets = ['Cat', 'Dog', 'Fish'] 
    colors = ['Red', 'Blue', 'Green']
    
    # Variables
    vars_dict = {}
    for person in people:
        vars_dict[f'person_{person}'] = model.addVar(f'person_{person}', domain=[0, 1, 2])
    for pet in pets:
        vars_dict[f'pet_{pet}'] = model.addVar(f'pet_{pet}', domain=[0, 1, 2])
    for color in colors:
        vars_dict[f'color_{color}'] = model.addVar(f'color_{color}', domain=[0, 1, 2])
    
    # Each person/pet/color appears exactly once
    person_vars = [vars_dict[f'person_{p}'] for p in people]
    pet_vars = [vars_dict[f'pet_{p}'] for p in pets]
    color_vars = [vars_dict[f'color_{c}'] for c in colors]
    
    model.addConstraint(gurddy.AllDifferentConstraint(person_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(pet_vars))
    model.addConstraint(gurddy.AllDifferentConstraint(color_vars))
    
    # Clue constraints
    def not_same(pos1, pos2):
        return pos1 != pos2
    
    def same_position(pos1, pos2):
        return pos1 == pos2
    
    # Clue 1: Alice doesn't live in the red house
    model.addConstraint(gurddy.FunctionConstraint(
        not_same, (vars_dict['person_Alice'], vars_dict['color_Red'])
    ))
    
    # Clue 2: The person with the cat lives in the blue house
    model.addConstraint(gurddy.FunctionConstraint(
        same_position, (vars_dict['pet_Cat'], vars_dict['color_Blue'])
    ))
    
    # Clue 3: Bob doesn't have the fish
    model.addConstraint(gurddy.FunctionConstraint(
        not_same, (vars_dict['person_Bob'], vars_dict['pet_Fish'])
    ))
    
    # Clue 4: Carol doesn't live in the green house
    model.addConstraint(gurddy.FunctionConstraint(
        not_same, (vars_dict['person_Carol'], vars_dict['color_Green'])
    ))
    
    solution = model.solve()
    
    if solution:
        print("\nSolution:")
        positions = ['Position 1', 'Position 2', 'Position 3']
        
        # Create position mapping
        pos_info = [{'person': None, 'pet': None, 'color': None} for _ in range(3)]
        
        for var_name, pos in solution.items():
            if var_name.startswith('person_'):
                pos_info[pos]['person'] = var_name[7:]
            elif var_name.startswith('pet_'):
                pos_info[pos]['pet'] = var_name[4:]
            elif var_name.startswith('color_'):
                pos_info[pos]['color'] = var_name[6:]
        
        for i, info in enumerate(pos_info):
            print(f"{positions[i]}: {info['person']} has {info['pet']} in {info['color']} house")
    else:
        print("No solution found!")

if __name__ == "__main__":
    # Solve simple logic puzzle first
    solve_simple_logic_puzzle()
    
    # Solve the famous Zebra puzzle
    print("\n" + "="*80)
    print("Solving the Famous Zebra Puzzle (Einstein's Riddle)...")
    solution, vars_dict = solve_zebra_puzzle()
    print_zebra_solution(solution, vars_dict)