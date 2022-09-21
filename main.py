from ACO import *
from local_search.iterated_local_search import *
import time

# Grab Currrent Time Before Running the Code
start = time.time()

instance = 'ta44_1.txt'
visualize_gantt = True
plot_cycles = True
save = True
verbose = True
do_local_search = True
num_tries = 10 # Number of tries for iterated local search algorithm (orifin 35)

parameters = {'alpha' : 1, 
                'beta' : 1,
                'rho' : 0.05, 
                'tau' : 0.5,
                'w_ib' : 3/5,
                'w_bs' : 1/5,
                'n_ants' : 10,
                'num_gen' : 400}

problem = OSSP_problem.load_instance(instance)
a = ACO(problem, parameters, verbose, save)

solution_schedule, solution_cost = a.run(seed=777)
print("Best Solution ever found using ACO: {} {}".format(solution_schedule, solution_cost))

end = time.time() # Grab Currrent Time After Running the Code
total_time = end - start # Subtract Start Time from The End Time
print("\nTime needed to find solution with ACO: "+ str(total_time))
print()


#########################################################
#               PLOT ACO INFORMATION
if plot_cycles:
    with open('results/ACO_cycles_results.json') as f:
        data = json.load(f)

    gen_min = np.zeros(len(data), dtype=np.uint)
    gen_mean = np.zeros(len(data), dtype=np.uint)
    gen_max = np.zeros(len(data), dtype=np.uint)

    for gen in data:
        gen_min[int(gen)-1] = data[gen][0]
        gen_mean[int(gen)-1] = data[gen][1]
        gen_max[int(gen)-1] = data[gen][2]
    
    plt.figure(figsize=(10,6))
    plt.plot(gen_min, color = 'g', label = 'min')
    plt.plot(gen_mean, color = 'y', label = 'mean')
    plt.plot(gen_max, color = 'b', label = 'max')

    plt.legend(loc="upper right")

    plt.title("ACO generations results")
    plt.xlabel("num_gen")
    plt.ylabel("Solution Cost")
    
    if save:
        plt.savefig('results/ACO_cycles_results.png')

    plt.show()



#########################################################
#               LOCAL SEARCH
if do_local_search: # Do local search on solution returned by ACO
    start = time.time()
    print('Start solution optimization using LOCAL SEARCH')
    num_swap = len(solution_schedule) // 5   # Swap 20% of the solution
    x, fx = iterated_local_search(problem, num_tries=num_tries, num_swap=num_swap, init_sol=solution_schedule)
    if fx < solution_cost:   # If local search improve solution
        solution_schedule = x
        solution_cost = fx
    
    end = time.time() # Grab Currrent Time After Running the Code
    total_time = end - start # Subtract Start Time from The End Time
    print("\nTime needed to improve solution with Local Search: "+ str(total_time))
    print("Best Solution ever found using Local Search on ACO results: {} {}".format(x, fx))



#########################################################
#               PRINT GANT
if visualize_gantt: # Print gantt 
    _, schedule = problem.objective_function(solution_schedule)
    results = problem.get_gantt(schedule)
    problem.visualize(results, save)