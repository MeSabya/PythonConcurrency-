from threading import Condition
from threading import Thread
import time
import heapq
import math

# Define an action object
class DeferredCallbackAction:
    def __init__(self, exec_action_after, name, action):
        self.exec_action_after = exec_action_after
        self.action = action
        self.name = name
        self.execute_at = math.inf

    def __lt__(self, other):
        return self.execute_at < other.execute_at

# We should have an executor class which should store the list of actions we wanted to execute.
# The executor class should expose an add_action api , which will use minheap to store all the actions pending for execution.
# The executor class should be a daemon thread , which should continuosly monitor if some new action is added
# The daemon thread should be sleeping when there is no action to be executed,
# should walk up immediately when ever there is some new action is added to the list.

class DeferredCallbackExecutor:
    def __init__(self):
        self.actions = []
        self.condn = Condition()
        self.sleep_for = 0

    def add_actions(self, deferred_action_obj):
        deferred_action_obj.execute_at = time.time()+deferred_action_obj.exec_action_after
        self.condn.acquire()
        heapq.heappush(self.actions, deferred_action_obj)
        self.condn.notifyAll()
        self.condn.release()

    def start(self):

        while True:
            self.condn.acquire()
            while len(self.actions) is 0:
                self.condn.wait()
            while len(self.actions) is not 0:
                next_action = self.actions[0]
                self.sleep_for = next_action.execute_at - math.floor(time.time())
                if self.sleep_for <= 0:
                    break
            self.condn.wait(timeout=self.sleep_for)
            action_to_execute_now = heapq.heappop(self.actions)
            action_to_execute_now.action(*(action_to_execute_now,))
            self.condn.release()

def say_hi(action):
        print("hi, I am {0} executed at {1} and required at {2}".format(action.name, math.floor(time.time()),
                                                                    math.floor(action.execute_at)))
if __name__ == "__main__":
    action1 = DeferredCallbackAction(3, ("A",), say_hi)
    action2 = DeferredCallbackAction(2, ("B",), say_hi)
    action3 = DeferredCallbackAction(1, ("C",), say_hi)
    action4 = DeferredCallbackAction(7, ("D",), say_hi)

    executor = DeferredCallbackExecutor()
    t = Thread(target=executor.start, daemon=True)
    t.start()

    executor.add_actions(action1)
    executor.add_actions(action2)
    executor.add_actions(action3)
    executor.add_actions(action4)

    time.sleep(15)

    

