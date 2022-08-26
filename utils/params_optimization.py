import sys
# setting path
sys.path.append('../Ant_Colony_Optimization_for_OSSP')

from ACO import *
import itertools
from tqdm import tqdm
'''
This script is used to find the optimal parameters for a given instance of OSSP.
To use the script it is necessary to enter the possible values (which are considered best) 
for the parameters of the ACO algorithm.
Furthermore, it is necessary to insert in the variable lower_bound the value of the best solution known at present. 
You can consult the site http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html 
where the benchmark values for many known instances are reported
(to create the relative instances see the script instances_creator.py).

The script will find the best combination of values for the parameters that allows to have the optimal solution.  

    - ALPHA                     #Exponential weight of pheromone on walk probabilities
    - BETA                      #Exponential weight of desirability (heuristic) on walk probabilities
    - rho                       #Pheromone evaporatio rate per cycle
    - tau0                      #Initial value for pheromone
    - n_ants                    #Number of ants walking in a cycle
    - w_ib=rho * x              #Reward to iteration best -> exploration
    - w_bs=rho * x              #Reward to best so far -> exploitation
    - num_gen
'''

parameters_options = {'alpha' : [1, 1.1], 'beta' : [1, 0.9], 'rho' : [0.1, 0.05, 0.01], 'tau': [0.5],           \
                        'n_ants' : [20, 10, 50], 'w_ib' : [2/3, 2/5], 'w_bs' : [1/3, 1/5], 'num_gen' : [100, 50, 200]}

keys, values = zip(*parameters_options.items())
parameters_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
print(parameters_combinations)

lower_bound = 300
instance = 'ta55_1.txt'
problem = OSSP_problem.load_instance(instance)


best_cost = 1e300 #large number
best_parameters_combination = {}
for parameters in tqdm(parameters_combinations):
    a = ACO(problem, parameters)
    
    soluzione = a.run(seed=42)

    if soluzione[1] <= best_cost:
        print()
        print(soluzione[1])
        best_cost = soluzione[1]
        best_parameters_combination.update(parameters)
    
    #When obtain solution cost equalt to lower bound stop the execution
    if lower_bound == best_cost:
        break   

print('migliore set di parametri: {} con costo soluzione di {}'.format(best_parameters_combination, best_cost))