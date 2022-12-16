#בס"ד

from tree3sons import tree3sons
from datetime import datetime

def find_max_engineers_required_weeks(list_with_tasks):
    #find max week_end
    max_end = 0
    for task in list_with_tasks:
        if task[1]>max_end:
            max_end = task[1]

    if max_end >0 :
        list_of_weeks = [0] * max_end
        for task in list_with_tasks:
            for i in range(task[0]-1,task[1]):
                list_of_weeks[i]+=task[2]

    max_amount_of_engineers = max(list_of_weeks)
    result = [i+1 for i,elem in enumerate(list_of_weeks) if elem == max_amount_of_engineers]

    print("Weeks with the most required  engineers are : ",result , "\n The amount of engineers is : ",max_amount_of_engineers)



#simple solution for the continuous data :
def find_max_engineers_required_weeks_con(list_with_tasks,datetime_str_format = '%d/%m/%y %H:%M'):
    max_engineers= 0
    list_with_tasks = [((datetime.strptime(task[0], datetime_str_format).timestamp()),\
                       (datetime.strptime(task[1], datetime_str_format).timestamp()),task[2])\
                       for task in list_with_tasks]
    for i,task in enumerate(list_with_tasks):
        if task[2] > max_engineers:
            max_engineers = task[2]  # update max engineers var if it's needed
        for j,task_to_compere in enumerate(list_with_tasks[i+1:]):
            new_task_l =new_task_c = new_task_r = None

            if task[1]>= task_to_compere[0] and task[0]<=task_to_compere[1]:  #if there is overlap
                list_with_tasks[i] = None
                del list_with_tasks[i+1+j]

                #Check all nine types of intersetions:
                if task[0]<task_to_compere[0] and task[1]<task_to_compere[1]:
                    new_task_l = (task[0],task_to_compere[0]-1,task[2])
                    new_task_c = (task_to_compere[0],task[1],task[2]+task_to_compere[2])
                    new_task_r = (task[1]+1,task_to_compere[1],task_to_compere[2])
                elif task[0]<task_to_compere[0] and task[1]==task_to_compere[1]:
                    new_task_l = (task[0],task_to_compere[0]-1,task[2])
                    new_task_c = (task_to_compere[0],task_to_compere[1],task[2]+task_to_compere[2])
                elif task[0]==task_to_compere[0] and task[1]==task_to_compere[1]:
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                elif task[0]<task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_l = (task[0], task_to_compere[0] - 1, task[2])
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1]+1, task[1] - 1, task[2])
                elif task[0]==task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1]+1, task[1] , task[2])
                elif task[0]>task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - 1, task_to_compere[2])
                    new_task_c = (task[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1] + 1, task[1], task[2])
                elif task[0]>task_to_compere[0] and task[1] < task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - 1, task_to_compere[2])
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                    new_task_r = (task[1]+1,task_to_compere[1],task_to_compere[2])
                elif task[0] > task_to_compere[0] and task[1] == task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - 1, task_to_compere[2])
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                elif task[0] == task_to_compere[0] and task[1] < task_to_compere[1]:
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                    new_task_r = (task[1]+1, task_to_compere[1] , task_to_compere[2])

                list_with_tasks.insert(i+1+j,new_task_l) if new_task_l is not None else None
                list_with_tasks.insert(i+1+j,new_task_c) if new_task_c is not None else  None
                list_with_tasks.insert(i+1+j,new_task_r) if new_task_r is not None else  None
                break

    result = [(datetime.fromtimestamp(task[0]).strftime(datetime_str_format),\
               datetime.fromtimestamp(task[1]).strftime(datetime_str_format))  \
               for task in list_with_tasks if task is not None and task[2] == max_engineers ]
    print("Weeks with the most required  engineers are : ",result , "\n The amount of engineers is : ",max_engineers)



if __name__ == "__main__":

    list_to_test = [(1,5,4),(11,28,2),(3,15,3),(22,34,1)]
    list_to_test_with_time = [("01/12/22 13:55", "28/12/22 14:34", 4), ("09/02/23 11:44", "06/03/23 12:22", 2),\
                              ("14/12/22 19:55", "13/02/23 10:45", 3), ("26/04/22 13:18", "30/06/22 13:15", 1)]

    #Test with array of weeks solution  (Discrete data) :
    print("Array solution : ")
    find_max_engineers_required_weeks(list_to_test)

    #Test with continuous data - with no special data structure solution:
    print("\nNo special data structure solution : ")
    find_max_engineers_required_weeks_con(list_to_test_with_time)

    #Test with tree (Discrete data) :
    new_tree = tree3sons()
    new_tree.push_list_of_tasks(list_to_test)
    print("\nTree solution (Discrete data) :\n", new_tree)

    #Test with tree (Continuous data):
    tree_with_datetime = tree3sons()
    tree_with_datetime.push_list_of_tasks(list_to_test_with_time, is_dates_str_format=True)
    print("\nTree solution (Continuous data) :\n" ,tree_with_datetime)



