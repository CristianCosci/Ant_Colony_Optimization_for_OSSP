from local_search.local_search_best_improvement import *
import random


def iterated_local_search(problem, num_tries, num_swap, init_sol, seed=0):
    random.seed(seed)
    n = problem.get_dim()
    x = init_sol.copy()
    nt = 0  # Failed attempts 
    fx, _ = problem.objective_function(x) # Only solution cost is needed
    while nt < num_tries:   # When failed num_tries attemps stop local searching
        y = perturbation(x, num_swap)
        z, fz = local_search(problem, y)
        if fz < fx:
            x = z
            fx = fz
            print("New best {}".format(fx))
            nt = 0  # If founded a best solution, restart local search in his neighborhood
        else:
            nt+=1
    return x, fx


def perturbation(x, num_swap):
    '''
    Make a change in the solution path swapping num_swap times 2 task in the scedule.
    '''
    n = len(x)
    y = x.copy()
    for _ in range(num_swap):
        i, j = random.sample(range(0, n), 2) # Take two random index of task
        y = do_swap(y, i, j)
    
    return y