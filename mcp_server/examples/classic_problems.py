"""
Classic Math Problem Solving Examples - Using Gurddy

This module demonstrates how to use Gurddy to solve classic math problems:
1. Blackjack (CSP)
2. Chicken and Rabbit Problem (LP)
3. Sudoku (CSP)
4. Eight Queens Problem (CSP)
5. Knapsack Problem (LP/CSP)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import gurddy
from itertools import permutations, product
from typing import List, Tuple, Optional


def print_section(title):
    """打印格式化的章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def solve_24_point_game(numbers: List[int]) -> Optional[str]:
    """
    解决二十四点游戏
    
    Args:
        numbers: 四个数字的列表，例如 [1, 2, 3, 4]
    
    Returns:
        如果有解，返回表达式字符串；否则返回None
    """
    print_section("二十四点游戏")
    print(f"给定数字: {numbers}")
    print("目标: 使用四则运算得到24")
    
    # 定义运算符
    operators = ['+', '-', '*', '/']
    op_funcs = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf')
    }
    
    # 尝试所有数字排列和运算符组合
    for num_perm in permutations(numbers):
        for ops in product(operators, repeat=3):
            # 尝试不同的括号组合
            expressions = [
                # ((a op1 b) op2 c) op3 d
                lambda: op_funcs[ops[2]](op_funcs[ops[1]](op_funcs[ops[0]](num_perm[0], num_perm[1]), num_perm[2]), num_perm[3]),
                # (a op1 (b op2 c)) op3 d
                lambda: op_funcs[ops[2]](op_funcs[ops[0]](num_perm[0], op_funcs[ops[1]](num_perm[1], num_perm[2])), num_perm[3]),
                # a op1 ((b op2 c) op3 d)
                lambda: op_funcs[ops[0]](num_perm[0], op_funcs[ops[2]](op_funcs[ops[1]](num_perm[1], num_perm[2]), num_perm[3])),
                # a op1 (b op2 (c op3 d))
                lambda: op_funcs[ops[0]](num_perm[0], op_funcs[ops[1]](num_perm[1], op_funcs[ops[2]](num_perm[2], num_perm[3]))),
                # (a op1 b) op2 (c op3 d)
                lambda: op_funcs[ops[1]](op_funcs[ops[0]](num_perm[0], num_perm[1]), op_funcs[ops[2]](num_perm[2], num_perm[3]))
            ]
            
            expr_strs = [
                f"(({num_perm[0]} {ops[0]} {num_perm[1]}) {ops[1]} {num_perm[2]}) {ops[2]} {num_perm[3]}",
                f"({num_perm[0]} {ops[0]} ({num_perm[1]} {ops[1]} {num_perm[2]})) {ops[2]} {num_perm[3]}",
                f"{num_perm[0]} {ops[0]} (({num_perm[1]} {ops[1]} {num_perm[2]}) {ops[2]} {num_perm[3]})",
                f"{num_perm[0]} {ops[0]} ({num_perm[1]} {ops[1]} ({num_perm[2]} {ops[2]} {num_perm[3]}))",
                f"({num_perm[0]} {ops[0]} {num_perm[1]}) {ops[1]} ({num_perm[2]} {ops[2]} {num_perm[3]})"
            ]
            
            for expr_func, expr_str in zip(expressions, expr_strs):
                try:
                    result = expr_func()
                    if abs(result - 24) < 1e-6:  # 考虑浮点数精度
                        print(f"\n✓ 找到解: {expr_str} = {result}")
                        return expr_str
                except (ZeroDivisionError, OverflowError):
                    continue
    
    print("\n✗ 无解")
    return None


def solve_chicken_rabbit_problem(total_heads: int, total_legs: int) -> Optional[Tuple[int, int]]:
    """
    解决鸡兔同笼问题
    
    Args:
        total_heads: 总头数
        total_legs: 总腿数
    
    Returns:
        (鸡的数量, 兔的数量) 或 None
    """
    print_section("鸡兔同笼问题")
    print(f"总头数: {total_heads}")
    print(f"总腿数: {total_legs}")
    print("约束: 鸡有1个头2条腿，兔有1个头4条腿")
    
    # 使用PuLP的线性规划求解器
    import pulp
    model = pulp.LpProblem("鸡兔同笼", pulp.LpMinimize)
    
    # 变量：鸡的数量和兔的数量
    chickens = pulp.LpVariable("鸡", lowBound=0, cat='Integer')
    rabbits = pulp.LpVariable("兔", lowBound=0, cat='Integer')
    
    # 约束条件
    # 头数约束：鸡数 + 兔数 = 总头数
    model += (chickens + rabbits == total_heads), '头数约束'
    
    # 腿数约束：2*鸡数 + 4*兔数 = 总腿数
    model += (chickens * 2 + rabbits * 4 == total_legs), '腿数约束'
    
    # 目标函数（任意，因为这是可行性问题）
    model += chickens + rabbits
    
    # 求解
    model.solve()
    
    if pulp.LpStatus[model.status] == 'Optimal':
        chicken_count = int(chickens.varValue) if chickens.varValue is not None else 0
        rabbit_count = int(rabbits.varValue) if rabbits.varValue is not None else 0
        
        print(f"\n✓ 解:")
        print(f"  鸡的数量: {chicken_count}")
        print(f"  兔的数量: {rabbit_count}")
        
        # 验证
        total_heads_check = chicken_count + rabbit_count
        total_legs_check = chicken_count * 2 + rabbit_count * 4
        
        print(f"\n验证:")
        print(f"  头数: {chicken_count} + {rabbit_count} = {total_heads_check} ({'✓' if total_heads_check == total_heads else '✗'})")
        print(f"  腿数: {chicken_count}×2 + {rabbit_count}×4 = {total_legs_check} ({'✓' if total_legs_check == total_legs else '✗'})")
        
        return (chicken_count, rabbit_count)
    else:
        print("\n✗ 无解 - 可能是输入的头数和腿数不匹配")
        return None


def solve_sudoku_mini(puzzle: List[List[int]]) -> Optional[List[List[int]]]:
    """
    解决4x4数独问题（简化版）
    
    Args:
        puzzle: 4x4的数独谜题，0表示空格
    
    Returns:
        解决后的数独或None
    """
    print_section("4x4数独问题")
    print("谜题:")
    for row in puzzle:
        print("  " + " ".join(str(x) if x != 0 else "." for x in row))
    
    model = gurddy.Model("4x4数独", "CSP")
    
    # 创建变量：每个格子的值
    vars_dict = {}
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == 0:  # 空格
                var_name = f"cell_{row}_{col}"
                vars_dict[var_name] = model.addVar(var_name, domain=[1, 2, 3, 4])
            else:  # 已填数字
                var_name = f"cell_{row}_{col}"
                vars_dict[var_name] = model.addVar(var_name, domain=[puzzle[row][col]])
    
    # 行约束：每行数字不重复
    for row in range(4):
        row_vars = [vars_dict[f"cell_{row}_{col}"] for col in range(4)]
        model.addConstraint(gurddy.AllDifferentConstraint(row_vars))
    
    # 列约束：每列数字不重复
    for col in range(4):
        col_vars = [vars_dict[f"cell_{row}_{col}"] for row in range(4)]
        model.addConstraint(gurddy.AllDifferentConstraint(col_vars))
    
    # 2x2方块约束
    for block_row in range(2):
        for block_col in range(2):
            block_vars = []
            for r in range(2):
                for c in range(2):
                    row = block_row * 2 + r
                    col = block_col * 2 + c
                    block_vars.append(vars_dict[f"cell_{row}_{col}"])
            model.addConstraint(gurddy.AllDifferentConstraint(block_vars))
    
    # 求解
    solution = model.solve()
    
    if solution:
        print("\n✓ 解:")
        result = [[0 for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                result[row][col] = solution[f"cell_{row}_{col}"]
        
        for row in result:
            print("  " + " ".join(str(x) for x in row))
        
        return result
    else:
        print("\n✗ 无解")
        return None


def solve_n_queens_mini(n: int = 4) -> Optional[List[int]]:
    """
    解决N皇后问题（默认4皇后）
    
    Args:
        n: 棋盘大小
    
    Returns:
        皇后位置列表或None
    """
    print_section(f"{n}皇后问题")
    print(f"在{n}x{n}棋盘上放置{n}个皇后，使其互不攻击")
    
    model = gurddy.Model(f"{n}皇后", "CSP")
    
    # 变量：每行皇后的列位置
    queens = []
    for i in range(n):
        queen = model.addVar(f"queen_{i}", domain=list(range(n)))
        queens.append(queen)
    
    # 约束1：不同列
    model.addConstraint(gurddy.AllDifferentConstraint(queens))
    
    # 约束2：不在同一对角线
    for i in range(n):
        for j in range(i + 1, n):
            row_diff = j - i
            
            # 正对角线约束
            def not_same_diagonal_pos(col1, col2, rd=row_diff):
                return abs(col1 - col2) != rd
            
            model.addConstraint(gurddy.FunctionConstraint(
                not_same_diagonal_pos, (queens[i], queens[j])
            ))
    
    # 求解
    solution = model.solve()
    
    if solution:
        positions = [solution[f"queen_{i}"] for i in range(n)]
        print(f"\n✓ 解: {positions}")
        print("棋盘:")
        
        for row in range(n):
            line = []
            for col in range(n):
                if positions[row] == col:
                    line.append("Q")
                else:
                    line.append(".")
            print("  " + " ".join(line))
        
        return positions
    else:
        print("\n✗ 无解")
        return None


def solve_knapsack_problem(weights: List[int], values: List[int], capacity: int) -> Optional[List[int]]:
    """
    解决0-1背包问题
    
    Args:
        weights: 物品重量列表
        values: 物品价值列表
        capacity: 背包容量
    
    Returns:
        选择的物品索引列表或None
    """
    print_section("0-1背包问题")
    print(f"物品重量: {weights}")
    print(f"物品价值: {values}")
    print(f"背包容量: {capacity}")
    
    n = len(weights)
    import pulp
    model = pulp.LpProblem("背包问题", pulp.LpMaximize)
    
    # 变量：每个物品是否选择（0或1）
    items = []
    for i in range(n):
        item = pulp.LpVariable(f"item_{i}", lowBound=0, upBound=1, cat='Binary')
        items.append(item)
    
    # 约束：重量不超过容量
    total_weight = sum(items[i] * weights[i] for i in range(n))
    model += (total_weight <= capacity), '容量约束'
    
    # 目标：最大化价值
    total_value = sum(items[i] * values[i] for i in range(n))
    model += total_value
    
    # 求解
    model.solve()
    
    if pulp.LpStatus[model.status] == 'Optimal':
        selected_items = []
        total_weight_used = 0
        total_value_gained = 0
        
        print(f"\n✓ 解:")
        for i in range(n):
            if items[i].varValue is not None and items[i].varValue > 0.5:  # 二进制变量
                selected_items.append(i)
                total_weight_used += weights[i]
                total_value_gained += values[i]
                print(f"  选择物品 {i}: 重量={weights[i]}, 价值={values[i]}")
        
        print(f"\n总结:")
        print(f"  选择的物品: {selected_items}")
        print(f"  总重量: {total_weight_used}/{capacity}")
        print(f"  总价值: {total_value_gained}")
        
        return selected_items
    else:
        print("\n✗ 无解")
        return None


def main():
    """运行所有经典问题示例"""
    print("经典数学问题求解 - 使用Gurddy")
    print("=" * 60)
    
    # 1. 二十四点游戏
    test_cases_24 = [
        [1, 2, 3, 4],
        [4, 1, 8, 7],
        [1, 1, 8, 8],
        [3, 3, 8, 8]
    ]
    
    for numbers in test_cases_24:
        solve_24_point_game(numbers)
    
    # 2. 鸡兔同笼问题
    chicken_rabbit_cases = [
        (35, 94),   # 经典问题：35个头，94条腿
        (10, 32),   # 10个头，32条腿
        (8, 20),    # 8个头，20条腿
        (5, 18)     # 无解情况
    ]
    
    for heads, legs in chicken_rabbit_cases:
        solve_chicken_rabbit_problem(heads, legs)
    
    # 3. 4x4数独
    sudoku_puzzle = [
        [1, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 3, 0, 0]
    ]
    solve_sudoku_mini(sudoku_puzzle)
    
    # 4. 4皇后问题
    solve_n_queens_mini(4)
    
    # 5. 背包问题
    weights = [2, 1, 3, 2]
    values = [3, 2, 4, 2]
    capacity = 5
    solve_knapsack_problem(weights, values, capacity)
    
    print("\n" + "=" * 60)
    print("所有经典问题演示完成！")
    print("Gurddy可以解决各种类型的优化和约束满足问题。")
    print("=" * 60)


if __name__ == "__main__":
    main()