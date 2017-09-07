"""
Description :
A task scheduler for task allocation. The allocation should be based on task priority,
enter time and analyst preference.
-------------------------------------------------------------------------------------
Properties task should have:
-------------------------------------------------------------------------------------
+ int TaskID
Requirement : (1) unique in whole system
+ Task type
Requirement : (1) dynamic field, N number of task type
+ Task priority
Requirement : (1) Urgent > High > Medium > Low
              (2) If same priority, compare time
+ Analyst Name :
Requirement : (1) unique for each analyst
+ Prefernce :
Requirement : (1) Task type the analyst interests in
-------------------------------------------------------------------------------------
Module Author : Chuqiao Chen <umnchuqiao@126.com>
"""
import queue
TaskPriority = {"Urgent" : 4, "High" : 3, "Medium" : 2, "Low" : 1}

class Analyst(object):

    def __init__(self, name):
        self.name = name
        self.preflist = None
        self.currenttask = None
        self.status = 0

    def setpreference(self, preferencelist):
        self.preflist = preferencelist.copy()

    def addprefernce(self, task):
        if self.prelist is None:
            self.preflist = [task]
        else:
            self.preflist.append(task)

    def addtask(self,Tasktype, TaskID, Priority):
        self.currenttask = (Tasktype, TaskID, Priority)
        self.status = 1

    def register(self, scheduler):
        for tasktype in self.preflist:
            scheduler.register(tasktype, self)

    def __repr__(self):
        print("I'm currently working on {}, {}".format(self.currenttask[0], self.currenttask[1]))

class Scheduler(object):

    def __init__(self):
        self.taskpref = {}
        self.taskqueue = queue.PriorityQueue()

    def register(self, tasktype, Analyst):
        if tasktype in self.taskpref.keys():
            self.taskpref[tasktype].append(Analyst)
        else:
            self.taskpref[tasktype] = [Analyst]

    def insertTask(self, Tasktype, TaskID, Priority):
        for worker in self.taskpref[Tasktype]:
            if worker.status != 0:
                worker.addtask(Tasktype, TaskID, Priority)
        self.taskqueue.put((Tasktype, TaskID, Priority))

    def clear(self):
        self.taskpref.clear()
        self.taskqueue.clear()

if __name__ == "__main__":
    sche = Scheduler()
    ana1 = Analyst("Anady")
    ana1.setpreference(['Task1','Task2'])
    ana2 = Analyst("Bob")
    ana2.setpreference((['Task1','Task3']))
    ana1.register(sche)
    ana2.register(sche)

    sche.insertTask("Task1", 123, "Urgent")
    sche.insertTask("Task2", 124, "High")
    sche.insertTask("Task3", 125, "Low")
