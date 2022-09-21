import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np


class OSSP_problem:

    def __init__(self, instance):
        self.data = instance
        self.num_jobs = len(self.data) 
        self.num_machines = len(self.data[0])


    def load_instance(file_name, verbose=False):
        """
        Reads file and create a matrix.
        The matrix contains the execution time needed to process each task:
            Raw:    Jobs number associated to task
            Column: Machines in which the task has to be executed
            Values: Task execution time

        returns:
            Matrix representation for the problem.
        """ 
        f = open("test_instances/" + file_name,"r")
        lines = f.readlines()
        f.close()
        num_jobs = len(lines)
        num_machines = len(lines[0].split()) // 2
        instance = np.ones((num_jobs, num_machines), dtype=int)
        this_job = 0
        for line in lines:
            for j, value in enumerate(line.split()):  
                if j%2 != 0:
                    instance[this_job][this_machine] = value
                else:
                    this_machine = int(value)
            this_job += 1

        print("num_jobs ", num_jobs)
        print("num_machines ", num_machines)
        if verbose:
            print(instance)

        return OSSP_problem(instance)


    def get_dim(self):
        '''
        returns: 
            the number of task thas has to be executed.
        '''
        return self.num_jobs * self.num_machines


    def get_num_machines(self):
        '''
        returns:
            number of machine for the problem.
        '''
        return self.num_machines

    
    def objective_function(self, solution, verbose = False):
        """
        Calculates the optimal time (makespan) for the entry path to the job shop scheduilling problem.

        returns:
            makespam time.
        """
        schedule = [] #Contains n list (n = num machines) with a scheduling for each machine
        for i in range(self.num_jobs):
            schedule.append([])
        
        for task in solution:   # for each task in solution path
            this_job = task // self.num_machines    #Find num of job
            this_machine = task % self.num_machines #Find machine where task need to be executed
            this_execution_time = self.data[this_job][this_machine] #Execution time of this task
            
            task_executed = False
            while not task_executed:
                job_already_executing_list = [] #list where is saved: if the task is executing or not for each machine
                for other_machine in range(self.num_machines):
                    if this_job in schedule[other_machine]: #control if the job is in the schedule of another machine
                        job_already_executing_list.append(True) #put a priori that is executing, next control if i really executing
                        
                        #save needed data
                        time_this_machine = len(schedule[this_machine])     #moment in time in which that machine is
                        time_other_machine = len(schedule[other_machine])   #moment in time in which other machine is

                        start_task_time_this_machine = time_this_machine    #time if the task is going to start immediatly in this machine
                        finish_task_time_other_machine = self.find_index(schedule[other_machine], this_job) #time when the task stop execution in other machine

                        if ((time_this_machine <= time_other_machine) and \
                                (finish_task_time_other_machine < start_task_time_this_machine)) or \
                                    (time_this_machine >= time_other_machine):
                            job_already_executing_list[other_machine] = False

                    else:
                        job_already_executing_list.append(False)
                
                #job already executing if is executing in at least one another machine
                job_already_executing = True if True in job_already_executing_list else False

                if job_already_executing: #if job already executing wait
                    schedule[this_machine].append('-')
                else:
                    for _ in range(this_execution_time): #otherwise execute the task
                        schedule[this_machine].append(this_job)
                        task_executed = True

        if verbose == True:
            for machine_schedule in schedule:
                print(machine_schedule)
        
        machine_execution_lengths = []
        for i in range(self.num_machines): #calculate makespan
            machine_execution_lengths.append(len(schedule[i]))
        
        return max(machine_execution_lengths), schedule


    def find_index(self, other_machine_schedule, job):
        '''
        returns:
            job's last time of execution in other_machine as an index.
        '''
        machine_schedule = other_machine_schedule.copy()
        machine_schedule.reverse()  # reversing the list
        index = machine_schedule.index(job) # finding the index of element
        return len(machine_schedule) - index - 1


    def get_gantt(self, solution):
        '''
        Create a list of dict that represent the solution scheduling.
        The list contains a dict for each task.
        The dict contains all information about task execution: 
            - Job to wich it belongs
            - Machine to wich it is executed
            - Start time of execution
            - Duration of execution
            - Finish time of execution
        
        returns:
            list of dict used to graphically visualize the gantt.
        '''
        gantt_data = [] #machine list of dict
        for i in range(self.num_machines):
            schedule = {}
            machine_num = i
            time = 0
            job_num = solution[i][0]
            start = time
            duration = 0
            for j in range(len(solution[i])):
                if job_num == solution[i][j]:
                    duration += 1
                    time += 1
                else:
                    schedule = self.get_dict(job_num, machine_num, start, duration)
                    gantt_data.append(schedule)
                    start = time
                    time += 1
                    job_num = solution[i][j]
                    duration = 1

            schedule = self.get_dict(job_num, machine_num, start, duration) #Do it because the last control cannot be done (out of bounds with index)
            gantt_data.append(schedule)
        
        gantt_data = self.remove_null_execution(gantt_data)

        return gantt_data

    
    def get_dict(self, job_num, machine_num, start, duration):
        '''
        returns:
            dict containing scheduling info for gantt.
        '''
        return ({'Job': 'job_'+str(job_num), 'Machine': 'machine_'+str(machine_num), \
                        'Start': start, 'Duration': duration, 'Finish': start+duration})


    def remove_null_execution(self, scheduling):
        '''
        returns:
            original gantt data less the null execution.
        '''
        new_scheduling = []
        for sched in scheduling:
            if sched['Job'] == 'job_-':
                pass
            else:
                new_scheduling.append(sched)
        
        return new_scheduling
    

    def visualize(self, results, save=False):
        '''
        Gantt graphically visualization.
        '''
        schedule = pd.DataFrame(results)
        JOBS = sorted(list(schedule['Job'].unique()))
        MACHINES = sorted(list(schedule['Machine'].unique()))
        makespan = schedule['Finish'].max()
        
        bar_style = {'alpha':1.0, 'lw':25, 'solid_capstyle':'butt'}
        text_style = {'color':'white', 'weight':'bold', 'ha':'center', 'va':'center'}
        colors = mpl.cm.Dark2.colors

        schedule.sort_values(by=['Job', 'Start'])
        schedule.set_index(['Job', 'Machine'], inplace=True)

        fig, ax = plt.subplots(2,1, figsize=(12, 5+(len(JOBS)+len(MACHINES))/4))

        for jdx, j in enumerate(JOBS, 1):
            for mdx, m in enumerate(MACHINES, 1):
                if (j,m) in schedule.index:
                    xs = schedule.loc[(j,m), 'Start']
                    xf = schedule.loc[(j,m), 'Finish']
                    ax[0].plot([xs, xf], [jdx]*2, c=colors[mdx%7], **bar_style)
                    ax[0].text((xs + xf)/2, jdx, m, **text_style)
                    ax[1].plot([xs, xf], [mdx]*2, c=colors[jdx%7], **bar_style)
                    ax[1].text((xs + xf)/2, mdx, j, **text_style)
                    
        ax[0].set_title('Jobs Schedule')
        ax[0].set_ylabel('Jobs')
        ax[1].set_title('Machines Schedule')
        ax[1].set_ylabel('Machines')
        
        for idx, s in enumerate([JOBS, MACHINES]):
            ax[idx].set_ylim(0.5, len(s) + 0.5)
            ax[idx].set_yticks(range(1, 1 + len(s)))
            ax[idx].set_yticklabels(s)
            ax[idx].text(makespan, ax[idx].get_ylim()[0]-0.2, "{0:0.1f}".format(makespan), ha='center', va='top')
            ax[idx].plot([makespan]*2, ax[idx].get_ylim(), 'r--')
            ax[idx].set_xlabel('Time')
            ax[idx].grid(True)
            
        fig.tight_layout()
        plt.plot()
        if save:
            plt.savefig('results/execution_gantt.png')
        plt.show()