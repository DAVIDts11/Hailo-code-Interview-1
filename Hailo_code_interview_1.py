#בס"ד

from tree3sons import tree3sons
from datetime import datetime
from itertools import chain

LIGHT_MAGENTA = '\033[95m'
RED = '\033[31m'
END_COLOR = '\033[0m'

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

    print("Max engineers at the same time: ",max_amount_of_engineers,"\nTime frame/s: ",result)



#simple solution for the continuous data :
def find_max_engineers_required_con(list_with_tasks,datetime_str_format = '%d/%m/%y %H:%M',min_delta_time=60):    #min_delta_time=60 = one minute
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
                    new_task_l = (task[0],task_to_compere[0]-min_delta_time,task[2])
                    new_task_c = (task_to_compere[0],task[1],task[2]+task_to_compere[2])
                    new_task_r = (task[1]+min_delta_time,task_to_compere[1],task_to_compere[2])
                elif task[0]<task_to_compere[0] and task[1]==task_to_compere[1]:
                    new_task_l = (task[0],task_to_compere[0]-min_delta_time,task[2])
                    new_task_c = (task_to_compere[0],task_to_compere[1],task[2]+task_to_compere[2])
                elif task[0]==task_to_compere[0] and task[1]==task_to_compere[1]:
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                elif task[0]<task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_l = (task[0], task_to_compere[0] - min_delta_time, task[2])
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1]+60, task[1] - min_delta_time, task[2])
                elif task[0]==task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_c = (task_to_compere[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1]+min_delta_time, task[1] , task[2])
                elif task[0]>task_to_compere[0] and task[1]>task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - min_delta_time, task_to_compere[2])
                    new_task_c = (task[0], task_to_compere[1], task[2] + task_to_compere[2])
                    new_task_r = (task_to_compere[1] + min_delta_time, task[1], task[2])
                elif task[0]>task_to_compere[0] and task[1] < task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - min_delta_time, task_to_compere[2])
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                    new_task_r = (task[1]+min_delta_time,task_to_compere[1],task_to_compere[2])
                elif task[0] > task_to_compere[0] and task[1] == task_to_compere[1]:
                    new_task_l = (task_to_compere[0], task[0] - min_delta_time, task_to_compere[2])
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                elif task[0] == task_to_compere[0] and task[1] < task_to_compere[1]:
                    new_task_c = (task[0], task[1], task[2] + task_to_compere[2])
                    new_task_r = (task[1]+min_delta_time, task_to_compere[1] , task_to_compere[2])

                list_with_tasks.insert(i+1+j,new_task_l) if new_task_l is not None else None
                list_with_tasks.insert(i+1+j,new_task_c) if new_task_c is not None else  None
                list_with_tasks.insert(i+1+j,new_task_r) if new_task_r is not None else  None
                break

    result = [(datetime.fromtimestamp(task[0]).strftime(datetime_str_format),\
               datetime.fromtimestamp(task[1]).strftime(datetime_str_format))  \
               for task in list_with_tasks if task is not None and task[2] == max_engineers ]
    print("Max engineers at the same time: ", max_engineers, "\nTime frame/s: ", result)


def easy_find_max_engineers_required_con(list_with_tasks,datetime_str_format = '%d/%m/%y %H:%M'):
    max_engineers= 0
    list_with_tasks = [((datetime.strptime(task[0], datetime_str_format).timestamp()),\
                       (datetime.strptime(task[1], datetime_str_format).timestamp()),task[2])\
                       for task in list_with_tasks]

    list_with_start_stop_dates =  list1111=list(chain.from_iterable(((task[0],task[2]), (task[1],-task[2])) for task in list_with_tasks))
    list_with_start_stop_dates.sort(key=lambda x:x[0])
    curr_amount_of_engineers = list_with_start_stop_dates[0][1]
    prev_datetime = list_with_start_stop_dates[0][0]
    result = []
    for curr_date in list_with_start_stop_dates[1:]:
        if curr_amount_of_engineers == max_engineers:
            result.append((prev_datetime,curr_date[0]))
        elif curr_amount_of_engineers > max_engineers:
            max_engineers = curr_amount_of_engineers
            result.clear()
            result.append((prev_datetime, curr_date[0]))
        curr_amount_of_engineers += curr_date[1]
        if curr_date[0]>prev_datetime:
            prev_datetime = curr_date[0]

    result_str = [(datetime.fromtimestamp(time_peiod[0]).strftime(datetime_str_format),\
               datetime.fromtimestamp(time_peiod[1]).strftime(datetime_str_format))  \
               for time_peiod in result]

    print("Max engineers at the same time: ", max_engineers, "\nTime frame/s: ", result_str)

if __name__ == "__main__":

    list_to_test = [(1,5,4),(11,28,2),(3,15,3),(22,34,1)]
    list_to_test_with_time = [("01/12/22 13:55", "28/12/22 14:34", 4), ("09/02/23 11:44", "06/03/23 12:22", 2),\
                              ("14/12/22 19:55", "13/02/23 10:45", 3), ("26/04/22 13:18", "30/06/22 13:15", 1)]

    try:

        #Test with array of weeks solution  (Discrete data) :
        a = datetime.now()
        print(LIGHT_MAGENTA,"\nArray solution : ",END_COLOR)
        find_max_engineers_required_weeks(list_to_test)


        #Test with continuous data - with no special data structure solution:
        print(LIGHT_MAGENTA,"\nNo special data structure solution : ",END_COLOR)
        find_max_engineers_required_con(list_to_test_with_time)

        #Test with tree (Discrete data) :
        new_tree = tree3sons()
        new_tree.push_list_of_tasks(list_to_test)
        print(LIGHT_MAGENTA,"\nTree solution (Discrete data) :",END_COLOR)
        print(new_tree)

        #Test with tree (Continuous data):
        tree_with_datetime = tree3sons()
        tree_with_datetime.push_list_of_tasks(list_to_test_with_time, is_dates_str_format=True)
        print(LIGHT_MAGENTA,"\nTree solution (Continuous data) :",END_COLOR)
        print(tree_with_datetime)

        # Test with easy algo:  (Continuous data):
        print(LIGHT_MAGENTA,"\nEasy alg. solution :",END_COLOR)
        easy_find_max_engineers_required_con(list_to_test_with_time)


    except Exception as e:
       print(RED,"ERROR : " + str(e),END_COLOR)