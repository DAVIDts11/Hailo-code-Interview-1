#בס"ד

#Solution with a tree :
from datetime import datetime

class Node3sons():
    def __init__(self,start,stop,engineers):
        self.start = start
        self.stop = stop
        self.engineers = engineers
        self.left = None
        self.centre = None
        self.right = None

class tree3sons():
    def __init__(self):
        self.head_node = None
        self.max_engineers = 0
        self.list_periods_of_time = []
        self.is_dates_str_format = False
        self.datetime_str_format = '%d/%m/%y %H:%M'

    def __str__(self):
        return f"max_engineers = {self.max_engineers}  \nlist_periods_of_time = {self.list_periods_of_time}"

    def push_list_of_tasks(self, list_of_tasks, is_dates_str_format = False,datetime_str_format = '%d/%m/%y %H:%M'):
        self.is_dates_str_format = is_dates_str_format
        self.datetime_str_format = datetime_str_format
        for task in list_of_tasks:
            if is_dates_str_format:   # start and stop  are time string var. (ex. "01/12/22 13:55")
                start_in_sec = datetime.strptime(task[0], self.datetime_str_format).timestamp()
                stop_in_sec = datetime.strptime(task[1], self.datetime_str_format).timestamp()
                task_in_seconds = (start_in_sec,stop_in_sec,task[2])
                self.push(task_in_seconds)
            else:   # start and stop  are  int var.
                self.push(task)

    def push(self,task,curr_node:Node3sons = None):
        start, stop, engineers = task
        if self.head_node == None:
            self.head_node = Node3sons(start,stop,engineers)
            self.max_engineers = engineers
            self.list_periods_of_time.append((start,stop))
            return
        if curr_node == None :
            curr_node = self.head_node
        all_task_pushed  = False
        while not all_task_pushed:
            if start < curr_node.start:
                if stop < curr_node.start:
                    self.__go_left(start,stop,engineers,curr_node)
                    all_task_pushed =True
                else:
                    self.__go_left(start, curr_node.start-1, engineers,curr_node)
                    start = curr_node.start
            elif start >= curr_node.start and start<=curr_node.stop:
                if stop <= curr_node.stop:
                    self.__go_centre(start, stop, engineers, curr_node)
                    all_task_pushed = True
                else :
                    self.__go_centre(start, curr_node.stop, engineers, curr_node)
                    start = curr_node.stop+1
            elif start>curr_node.stop:
                self.__go_right(start, stop, engineers, curr_node)
                all_task_pushed = True

    def __update_list_and_max(self,start,stop,engineers):
        if self.is_dates_str_format :
            start = datetime.fromtimestamp(start).strftime(self.datetime_str_format)
            stop = datetime.fromtimestamp(stop).strftime(self.datetime_str_format)
        if engineers>self.max_engineers:
            self.max_engineers = engineers
            self.list_periods_of_time.clear()
            self.list_periods_of_time.append((start, stop))
        elif engineers == self.max_engineers:
            self.list_periods_of_time.append((start,stop))

    def __go_left(self,start,stop,engineers,curr_node:Node3sons):
        if curr_node.left == None:
            curr_node.left = Node3sons(start,stop,engineers)
            self.__update_list_and_max(start, stop, engineers)
        else:
            self.push((start, stop, engineers),curr_node.left)

    def __go_centre(self,start,stop,engineers,curr_node:Node3sons):
        if curr_node.centre == None:
            curr_node.centre = Node3sons(start,stop,engineers)
            self.__update_list_and_max(start, stop, engineers+curr_node.engineers)
        else:
            self.push((start, stop, engineers+curr_node.engineers),curr_node.centre)

    def __go_right(self,start,stop,engineers,curr_node:Node3sons):
        if curr_node.right == None:
            curr_node.right = Node3sons(start, stop, engineers)
            self.__update_list_and_max(start, stop, engineers)
        else:
            self.push((start, stop, engineers), curr_node.right)

