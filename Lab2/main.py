from threading import Event, Thread, Lock


class MyTask:
    def __init__(self, action, events_to_wait, event_to_set):
        self.action = action
        self.events_to_wait = events_to_wait
        self.event_to_set = event_to_set

    def run(self):
        # Wait for all required events
        for event_to_end in self.events_to_wait:
            event_to_end.wait()

        # Run action
        self.action()

        # Set that it's ready
        self.event_to_set.set()


print_lock = Lock()


def my_print(some_str):
    with print_lock:
        print(some_str)


def lambda_print(some_str):
    return lambda: my_print(some_str)


def init_tasks():
    tasks = [None] * 6

    tasks[0] = MyTask(
        lambda_print('task1'),
        [task_events[4]],
        task_events[0])

    tasks[1] = MyTask(
        lambda_print('task2'),
        [task_events[4], task_events[5]],
        task_events[1])

    tasks[2] = MyTask(
        lambda_print('task3'),
        [task_events[4], task_events[5]],
        task_events[2])

    tasks[3] = MyTask(
        lambda_print('task4'),
        [task_events[5]],
        task_events[3])

    tasks[4] = MyTask(
        lambda_print('task5'),
        [],
        task_events[4])

    tasks[5] = MyTask(
        lambda_print('task6'),
        [],
        task_events[5])

    return tasks


if __name__ == '__main__':
    a = lambda: my_print("ww")

    task_events = [Event() for i in range(6)]
    tasks = init_tasks()

    tasks_threads = []
    for task in tasks:
        tasks_threads.append(Thread(target=task.run))

    for thread in tasks_threads:
        thread.start()

    for thread in tasks_threads:
        thread.join()
