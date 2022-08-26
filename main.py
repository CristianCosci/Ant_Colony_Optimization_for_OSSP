from ACO import *
from local_search.iterated_local_search import *
import time

# Grab Currrent Time Before Running the Code
start = time.time()

instance = 'ta44_1.txt'
visualize_gantt = True
save = True
verbose = True
do_local_search = True
num_tries = 50 # Number of tries for iterated local search algorithm

parameters = {'alpha' : 1, 
                'beta' : 1,
                'rho' : 0.05, 
                'tau' : 0.5,
                'w_ib' : 3/5,
                'w_bs' : 1/5,
                'n_ants' : 10,
                'num_gen' : 500}

problem = OSSP_problem.load_instance(instance)
a = ACO(problem, parameters, verbose, save)

solution_schedule, solution_cost = a.run(seed=42)
print("Best Solution ever found using ACO: {} {}".format(solution_schedule, solution_cost))

# Grab Currrent Time After Running the Code
end = time.time()

#Subtract Start Time from The End Time
total_time = end - start
print("\nTime needed to find solution: "+ str(total_time))

if do_local_search: # Do local search on solution returned by ACO
    num_swap = len(solution_schedule) // 5   # Swap 20% of the solution
    x, fx = iterated_local_search(problem, num_tries=num_tries, num_swap=num_swap, init_sol=solution_schedule)
    if fx < solution_cost:   # If local search improve solution
        solution_schedule = x
        solution_cost = fx

    print("Best Solution ever found using Local Search on ACO results: {} {}".format(x, fx))


if visualize_gantt: # Print gantt 
    _, schedule = problem.objective_function(solution_schedule)
    results = problem.get_gantt(schedule)
    problem.visualize(results, save)