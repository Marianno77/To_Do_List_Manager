import json
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description , priority, status = 'unfinished', time = None, deadline = None, done_time = None):
        self.title = title
        self.description  = description
        self.priority = priority
        self.status = status
        self.time = time or datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.deadline = deadline or (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y %H:%M:%S')
        self.done_time = done_time

    # Zmiana wartości pól taska (5 metod):
    def mark_as_done(self):
        self.status = 'done'
        self.done_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def mark_as_unfinished(self):
        self.status = 'unfinished'
        self.done_time = None

    def edit_title(self, new_title):
        self.title = new_title

    def edit_description(self, new_description):
        self.description = new_description

    def edit_priority(self, new_priority):
        self.priority = new_priority

    # Zapis taska do pliku json
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "time": self.time,
            "deadline": self.deadline,
            "done_time": self.done_time
        }

    # Tworzenie taska z pliku json
    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["description"], data["priority"], data["status"], data["time"], data["deadline"], data["done_time"])

class TaskManager:
    def __init__(self, filename = 'tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    # Dodawanie kolejnych tasków do listy:
    def add_task(self, task):
        self.tasks.append((task))

    # Usuwanie tasków z listy:
    def remove_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                print(f'Task deleted: {title}')

    # Edycja poszczególnych pól tasków (5 metod):
    def mark_task_done(self, title):
        for task in self.tasks:
            if task.title == title:
                task.mark_as_done()
                print(f'Task completed: {title}')

    def mark_task_unfinished(self, title):
        for task in self.tasks:
            if task.title == title:
                task.mark_as_unfinished()
                print(f'Task unfinished: {title}')

    def edit_task_title(self, title, new_title):
        for task in self.tasks:
            if task.title == title:
                task.edit_title(new_title)

    def edit_task_description(self, title, new_description):
        for task in self.tasks:
            if task.title == title:
                task.edit_description(new_description)

    def edit_task_priority(self, title, new_priority):
        for task in self.tasks:
            if task.title == title:
                task.edit_priority(new_priority)

    # Wypisywanie zawartości tasków (3 metody):
    def print_task(self, task):
        color_done = "\033[92m"
        color_unfinished = "\033[91m"
        color_basic = "\033[0m"

        color = color_done if task.status == 'done' else color_unfinished

        print(f'-------------------------------\n'
              f'Title: {task.title} \n'
              f'Description: {task.description} \n'
              f'Priority: {task.priority} \n'
              f'Status: {color}{task.status}{color_basic} \n'
              f'Time: {task.time} \n'
              f'Deadline: {task.deadline} \n'
              f'Date of execution: {task.done_time} \n'
              f'-------------------------------\n')

    def show_tasks_by_status(self, filter_by='all'):
        to_show = []

        if filter_by == 'all':
            to_show = self.tasks
        else:
            for task in self.tasks:
                if task.status == filter_by:
                    to_show.append(task)

        if len(to_show) != 0:
            to_show = sorted(to_show, key=lambda task: task.time)
            for task in to_show:
                self.print_task(task)
        else:
            print('Not found')


    def show_tasks_by_priority(self, filter_by='all'):
        to_show = []

        if filter_by == 'all':
            to_show = self.tasks
        else:
            for task in self.tasks:
                if task.priority == filter_by:
                    to_show.append(task)

        if len(to_show) != 0:
            to_show = sorted(to_show,key=lambda task: task.time)
            for task in to_show:
                self.print_task(task)
        else:
            print('Not found')


    # Sprawdza czy dalej jest czas na wykonanie zadania:
    def is_deadline(self, title):
        for task in self.tasks:
            if task.title == title:
                deadline = datetime.strptime(task.deadline, '%d-%m-%Y %H:%M:%S')
                if task.done_time == None:
                    now = datetime.now()
                    if now > deadline:
                        print(f'\033[91mTime is up \033[0m \n'
                              f'Title: {task.title} \n'
                              f"Deadline: {deadline.strftime('%d-%m-%Y %H:%M:%S')} \n")
                    else:
                        print(f'\033[92mThere is still time \033[0m \n'
                              f'Title: {task.title} \n'
                              f"Deadline: {deadline.strftime('%d-%m-%Y %H:%M:%S')} \n")
                else:
                    done = datetime.strptime(task.done_time, '%d-%m-%Y %H:%M:%S')
                    if done > deadline:
                        print(f'\033[91mTask completed after time \033[0m \n'
                              f'Title: {task.title} \n'
                              f"Deadline: {deadline.strftime('%d-%m-%Y %H:%M:%S')} \n"
                              f'Date of execution: {task.done_time} \n')
                    else:
                        print(f'\033[92mTask completed within the allotted time. \033[0m \n'
                              f'Title: {task.title} \n'
                              f"Deadline: {deadline.strftime('%d-%m-%Y %H:%M:%S')} \n"
                              f'Date of execution: {task.done_time} \n')

    # Zaspisywanie listy z taskami do pliku json
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
            print('Tasks saved')

    # Wczytywanie listy z taskami z pliku json
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(i) for i in data]
        except FileNotFoundError:
            self.tasks = []
            print('File not found')

if __name__ == '__main__':
    manager = TaskManager()

    while True:
        print('1 - Add Task \n'
              '2 - Remove Task \n'
              '3 - Edit Task \n'
              '4 - Show Tasks \n'
              '5 - Deadline \n'
              '6 - Save Tasks \n'
              '7 - Load Tasks \n'
              '8 - Exit \n')

        try:
            choice = int(input('Select an option: '))
        except ValueError:
            print('Please enter a valid number!')
            continue

        match choice:
            case 1:
                title = input('Enter the title of the task: ')
                description = input('Enter the description of the task: ')
                priority = input('Enter the priority of the task (preferred: 1-3): ')

                task = Task(title,description,priority)
                manager.add_task(task)
                manager.save_tasks()

            case 2:
                title = input('Enter the title of the task: ')
                manager.remove_task(title)
                manager.save_tasks()

            case 3:
                while True:
                    print('1 - Mark Task Done \n'
                          '2 - Mark Task Unfinished \n'
                          '3 - Edit Task Title \n'
                          '4 - Edit Task Description\n'
                          '5 - Edit Task Priority\n'
                          '6 - Back \n')

                    try:
                        choice_two = int(input('Select an option: '))
                    except ValueError:
                        print('Please enter a valid number!')
                        continue

                    match choice_two:
                        case 1:
                            title = input('Enter the title of the task: ')
                            manager.mark_task_done(title)

                        case 2:
                            title = input('Enter the title of the task: ')
                            manager.mark_task_unfinished(title)

                        case 3:
                            title = input('Enter the title of the task: ')
                            new_title = input('Enter the new title of the task: ')

                            manager.edit_task_title(title, new_title)

                        case 4:
                            title = input('Enter the title of the task: ')
                            new_description = input('Enter the new description of the task: ')

                            manager.edit_task_description(title, new_description)

                        case 5:
                            title = input('Enter the title of the task: ')
                            new_priority = input('Enter the new priority of the task: ')

                            manager.edit_task_priority(title, new_priority)
                        case 6:
                            break
                        case _:
                            print('Incorrect selection, please try again!')

            case 4:
                while True:
                    print('1 - Filter By Priority\n'
                          '2 - Filter By Status \n'
                          '3 - Back \n')

                    try:
                        choice_two = int(input('Select an option: '))
                    except ValueError:
                        print('Please enter a valid number!')
                        continue

                    match choice_two:
                        case 1:
                            priority = input('Enter priority (all = "all"): ')
                            manager.show_tasks_by_priority(priority)

                        case 2:
                            status = input('Enter status (all = "all"): ')
                            manager.show_tasks_by_status(status)

                        case 3:
                            break

                        case _:
                            print('Incorrect selection, please try again!')

            case 5:
                title = input('Enter the title of the task: ')
                manager.is_deadline(title)

            case 6:
                manager.save_tasks()

            case 7:
                manager.load_tasks()

            case 8:
                print('See you!')
                break
            case _:
                print('Incorrect selection, please try again!')

    print('\033[92mAutor: Mariusz Bienasz \033[0m')