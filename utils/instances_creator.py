import numpy as np

'''
This script is used to create instances from http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html
To create an instance copy and paste the processing time in tasks.txt file and the machine part in machines.txt file.
The script would create for you a new .txt file named as num_machines * num_jobs and a version (to change version change variable file_name).
'''

file_name = 2
machines_file_name = 'machines.txt'
tasks_file_name = 'tasks.txt'

f_machines = open("utils/" + machines_file_name,"r")
lines_m = f_machines.readlines()
f_machines.close()

f_tasks = open("utils/" + tasks_file_name, "r")
lines_t = f_tasks.readlines()
f_tasks.close()

num_jobs = len(lines_t)
num_machines = len(lines_t[0].split())

instance = np.ones((num_jobs, num_machines * 2), dtype=int)

for i in range(num_jobs):
    for j in range(num_machines):
        instance[i][j*2] = int(lines_m[i].split()[j]) - 1
        instance[i][j*2+1] = lines_t[i].split()[j]

with open('test_instances/ta' + str(num_jobs) + str(num_machines) + '_' +  str(file_name) + ".txt", 'w') as fp:
    for i in range(num_jobs):
        for j in range(num_machines*2):
            fp.write(str(instance[i][j]))
            fp.write(" ")
        fp.write("\n")

print(instance)
print("num_jobs ", num_jobs)
print("num_machines ", num_machines)
print("Done")