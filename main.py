from ACO import *
import time

# Grab Currrent Time Before Running the Code
start = time.time()

instance = 'prova.txt'
visualize_gannt = True
save = True
verbose = True
parameters = {'alpha' : 1, 
                'beta' : 1, 
                'rho' : 0.1, 
                'tau': 0.5, 
                'n_ants' : 20, 
                'num_gen' : 200}

problem = JSSP_problem.load_instance(instance)
a = ACO(problem, parameters, verbose, save)

soluzione = a.run()
print("migliore soluzione:", soluzione)

# Grab Currrent Time After Running the Code
end = time.time()

#Subtract Start Time from The End Time
total_time = end - start
print("\nTime needed to find solution: "+ str(total_time))

if visualize_gannt:   # Print gannt 
    _, schedule = problem.objective_function(soluzione[0])
    results = problem.get_gannt(schedule)
    problem.visualize(results, save)