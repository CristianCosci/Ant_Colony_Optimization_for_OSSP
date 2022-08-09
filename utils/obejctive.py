def objective_function(self, solution):
    """
    Calculates the optimal time (makespan) for the entry path to the job shop scheduilling problem.

    returns:
        makespam time
    """
    #Initialize scheduler
    machine_task_moments = [] #Represent all the tasks on their moments in wich machine
    machine_moments = [] #Represents in wich moment of time that machine is
    for i in range(self.num_machines):
        machine_task_moments.append([])
        machine_moments.append(0)

    for task in solution:
        job_number = task // self.num_machines #Represent the job number of task that need to be executed
        machine_number = task % self.num_machines #Represent the machine number which the job need to be executed
        task_time = int(self.data[job_number][machine_number]) #Represent time needed to execute the task
        moment = machine_moments[machine_number]
        moment_for_task_not_found = True

        #Verify in wich moment the task can initiate
        while moment_for_task_not_found:
            foud_other_machine_with_same_task = False
            for other_machine in range(self.num_machines):
                if other_machine == machine_number:
                    pass
                else:
                    try:
                        if job_number == machine_task_moments[other_machine][moment]: #control if the job is executing in another machine at same time 
                            foud_other_machine_with_same_task = True
                            break
                    except:
                        pass
            
            if foud_other_machine_with_same_task == False:
                #Stops the loop
                moment_for_task_not_found = False
                #fill the job time for that machine
                for i in range(task_time):
                    machine_task_moments[machine_number].append(job_number)
                machine_moments[machine_number] = task_time + moment + 1
            else:
                #Make the machine wait until the job is done in another machine
                machine_task_moments[machine_number].append('-')
                moment+=1
                
    #Uncomment next lines if you want to print the Makespan for each schedule tested on execution:
    #for i in range(self.num_machines):
    #    print(machine_task_moments[i])

    machine_execution_lengths = []
    for i in range(self.num_machines):
        machine_execution_lengths.append(len(machine_task_moments[i]))
    
    return max(machine_execution_lengths), machine_task_moments