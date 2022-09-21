import json
from statistics import mean
from OSSP import *
from tqdm import tqdm

class ACO:
    
    def __init__(self, problem, parameters, verbose=False, save=False):
        self.problem = problem
        self.ALPHA = parameters['alpha']        #Exponential weight of pheromone on walk probabilities
        self.BETA = parameters['beta']          #Exponential weight of desirability (heuristic) on walk probabilities
        self.rho = parameters['rho']            #Pheromone evaporatio rate per cycle
        self.tau0 = parameters['tau']           #Initial value for pheromone
        self.n_ants = parameters['n_ants']      #Number of ants walking in a cycle
        self.num_gen = parameters['num_gen']    #Number of cycle
        self.w_ib=self.rho * parameters['w_ib'] #Reward to iteration best -> exploration
        self.w_bs=self.rho * parameters['w_bs'] #Reward to best so far -> exploitation
        self.n_tasks = problem.get_dim()
        self.verbose = verbose
        self.save = save
        self.num_machines = problem.get_num_machines()


    def initialize(self):
        '''
        Initialize pheromone table and ants data.
        At the beginning all the value for pheromone are eguals -> the ants choose only following heuristic value (teta).
        Pheromone has no contribute in the ants decision.
        '''
        self.phero = np.ones((self.n_tasks+1, self.n_tasks)) * self.tau0
        self.best_so_far = None
        self.bs_cost = 1e300 #very large value
        self.sol = [None] * self.n_ants
        self.sol_cost = np.zeros(self.n_ants)


    def run(self,seed=0):
        """
        Method responsible to create and execute all ants through the enviroment and update the pheromones.

        returns:
            - Print the best time.
            - Generate a file with the 
                time results of all cycles with this structure:
                {cycle : [Fastest, Mean, Longest], ...}
        """
        results_control = {}
        np.random.seed(seed)
        self.initialize()
        for gen in tqdm(range(1,self.num_gen+1)):

            this_cycle_times = [] #

            for ant_num in range(0, self.n_ants):
                self.sol[ant_num] = self.generate_solution()

                path_time, _ = self.problem.objective_function(self.sol[ant_num])
                this_cycle_times.append(path_time)

            self.evaluate_solutions(gen)
            self.update_pheromone()

            if self.save:
                #save recorded values
                results_control.update({gen : [min(this_cycle_times), mean(this_cycle_times), max(this_cycle_times)]})
        
        if self.save:
            #generating file with fitness through cycles
            json.dump( results_control, open("results/ACO_cycles_results.json", 'w' ))

        return self.best_so_far, self.bs_cost


    def generate_solution(self):
        """
        The ant walks on every node of the graph without reapeating any.

        returns:
            array with task followed in order
        """
        sol = []
        task_to_process = list(range(self.n_tasks))
        current_task = self.n_tasks # a non existing task, it means that it must choose the first task to process
        for i in range(self.n_tasks):
            next_task = self.select_task(current_task, task_to_process)
            sol.append(next_task)
            current_task = next_task
            task_to_process.remove(next_task)
            
        return sol


    def select_task(self, current_task, task_to_process):
        """
        With the not visited node probabilities chooses (using roulette wheel) the next node to visit.

        returns:
            next_node
        """
        num_task_to_process = len(task_to_process) #num task remaining to process
        prob = np.zeros(num_task_to_process)
        for i in range(0, num_task_to_process):
            task = task_to_process[i]
            tau = self.phero[current_task][task] #pheromone value
            teta = 1 if current_task == self.n_tasks else 1/self.problem.data[task // self.num_machines][task % self.num_machines] #heuristic value
            p_i_to_j = tau**self.ALPHA * teta**self.BETA #Probability of choosing task j as next task in solution path
            prob[i] = p_i_to_j
        
        #Normalize probabilities to sum 1 for numpy randon choice method
        den = sum(prob)
        normalized_probabilities = prob/den
        indexs = [ i for i in range(len(normalized_probabilities))]
        next_node_index = np.random.choice(indexs, p=normalized_probabilities) #Roulette Wheel method
        return task_to_process[next_node_index]
    

    def evaporate(self):
        self.phero = (1-self.rho)*self.phero


    def evaluate_solutions(self, gen):
        '''
        Evaluate solution, find the iteration best and if necessary replace the best so far.
        '''
        for i in range(0,self.n_ants):
            self.sol_cost[i], _ = self.problem.objective_function(self.sol[i]) #Save solution cost for each ant
        self.ibest = self.sol_cost.argmin() #Take best solution (minimum cost) for the ants colony
        if self.sol_cost[self.ibest] < self.bs_cost: #If the iteration best is better than best so far replace the solution
            self.bs_cost = self.sol_cost[self.ibest]
            self.best_so_far = self.sol[self.ibest]
            if self.verbose == True:
                print("new best {} at gen. {}".format(self.bs_cost, gen))


    def update_pheromone(self):
        '''
        Evaporate pheromone and give reward.
        The update does not exist in nature.

        rewards (s, k): # reward based on solution s
            for all ci, cj appearing in s
                tau_ij <- tau_ij + K / Ls
        
        where Ls is the cost of the solution s.
        There are 3 possibilities:
            1. reward (s_bs, w_bs)
            2. reward (s_ib, w_ib)
            3. reward (s_bs, w_bs)
               reward (s_ib, w_ib)
        
        w_bs and w_ib are problem-dependent weights and need to be calibrated. 
        There are also variants in which not only one solution is awarded but for example also the second best etc ...
        '''
        self.evaporate()
        #self.reward(self.best_so_far, self.w_bs/self.bbs_cost)
        #self.reward(self.sol[self.ibest], self.w_ib/self.sol_cost[self.ibest])
        self.reward(self.best_so_far, self.w_bs)
        self.reward(self.sol[self.ibest], self.w_ib)


    def reward(self, sol, delta):
        '''
        Give a small reward to each couple c_i c_j, that appear in good solution (iteration best and/or best so far).
        '''
        current = self.n_tasks
        for i in range(self.n_tasks):
            task = sol[i]
            self.phero[current][task] += delta
            current = task