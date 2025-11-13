#!/usr/bin/env python3
import pulp

# Documentation: https://coin-or.github.io/pulp/


def solve_nqueens(n=8):
    model = pulp.LpProblem("nQueens", pulp.LpMaximize)  # Create MILP model

    # Binary variables: x[i][j] = 1 if a queen is at (i,j)
    x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(n)] for i in range(n)]

    # Objective: maximize number of queens
    model += pulp.lpSum(x[i][j] for i in range(n) for j in range(n))

    # One queen per row
    for i in range(n):
        model += pulp.lpSum(x[i][j] for j in range(n)) == 1
    # One queen per column
    for j in range(n):
        model += pulp.lpSum(x[i][j] for i in range(n)) == 1
    # Main diagonals (i - j constant)
    for d in range(-n + 1, n):
        model += pulp.lpSum(x[i][j] for i in range(n) for j in range(n) if i - j == d) <= 1
    # Anti-diagonals (i + j constant)
    for d in range(2 * n - 1):
        model += pulp.lpSum(x[i][j] for i in range(n) for j in range(n) if i + j == d) <= 1

    model.solve(pulp.PULP_CBC_CMD(msg=False))  # Solve using PuLP's default solver

    # Extract and print solution
    board = [['.' for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if pulp.value(x[i][j]) == 1:
                board[i][j] = 'Q'

    for row in board:
        print(' '.join(row))

    print("\nStatus:", pulp.LpStatus[model.status])
    print("Objective (number of queens):", pulp.value(model.objective))


solve_nqueens(8)  # Example: 8 queens
solve_nqueens(20)
