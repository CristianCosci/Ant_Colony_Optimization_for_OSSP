import numpy as np

def do_swap(sol, i, j):
    '''
    Swap/exchange 2 task (i and j) in the solution schedule to have a neighbor of current solution.
    '''
    sol_swapped = sol.copy()
    sol_swapped[i] = sol[j]
    sol_swapped[j] = sol[i]
    return sol_swapped


def local_search(problem, init_sol, verbose=False):
    n = problem.get_dim()
    x = init_sol.copy()

    continue_improve = True
    improved = False

    fx, _ = problem.objective_function(x)
    if verbose:
        print("Initial value {}".format(fx))

    while continue_improve:
        fy = 1e300  # very large number
        for i in range(1, n-1): # Try all possible neighbors
            for j in range(i+1, n):
                y = do_swap(x, i, j)
                fy, _ = problem.objective_function(y) # Calculate cost of solution obtained by swap
                if fy < fx:
                    fx = fy
                    x = y
                    if verbose:
                        print("New best {}".format(fx))
                    improved = True
        
        # Continue local search if improved
        if improved:
            continue_improve = True
            improved = False
        else:
            continue_improve = False
    
    return x, fx