#import random
#class Dise:
#    def roll(self, a, b):
#        self.a = a
#        self.b = b
#       return (a, b)

#d = Dise()
#print(d.roll(random.randint(1, 5), random.randint(1, 5)))


class Worker:
    def __init__(self, worker_num, fname, Iname, work_experience_company, salary, age):
        self.worker_num = worker_num
        self.fname = fname
        self.Iname = Iname
        self.work_experience_company = work_experience_company
        self.salary = salary
        self.age = age

    def worker_information(self):
        return f"({self.worker_num},{self.fname},{self.Iname},{self.work_experience_company},{self.salary},{self.age})"

    def salary_bonus(self):
        if self.work_experience_company < 5:
            return round(self.salary * 0.5 / 100, 2)
        elif self.work_experience_company > 10:
            return round(self.salary * 2 / 100, 2)
        else:
            return round(self.salary * 1.5 / 100, 2)


def search_by_num(workers_list, worker_num):
    found_workers = [worker for worker in workers_list if worker.worker_num == worker_num]
    
    if len(found_workers) > 0:
        for worker in found_workers:
            print(worker.worker_information())
        return True
    else:
        print(f"No workers found with number {worker_num}")
        return False


def search_by_name_experience(workers_list, fname, work_experience_company):
    found_workers = [worker for worker in workers_list if worker.fname == fname and worker.work_experience_company == work_experience_company]

    if len(found_workers) > 0:
        for worker in found_workers:
            print(worker.worker_information())
        return True
    else:
        print(f"No workers found with name '{fname}' and experience {work_experience_company}")
        return False


def add_worker(workers_list, worker):
    workers_list.append(worker)


def remove_worker(workers_list, worker_num):
    workers = [worker for worker in workers_list if worker.worker_num == worker_num]
    
    if len(workers) > 0:
        workers_list.remove(workers[0])
        return True
    else:
        print(f"No workers found with number {worker_num}")
        return False


if __name__ == "__main__":
    while True:
        try:
            number = int(input("Enter the number of workers: "))
            if number < 1:
                raise ValueError("Invalid number...")
            else:
                break
        except ValueError as e:
            print(e)

    workers_list = []
    for i in range(number):
        worker_data = input(f"(Worker {i + 1}): ").split(',')
        worker = Worker(
            int(worker_data[0]),
            worker_data[1],
            worker_data[2],
            int(worker_data[3]),
            float(worker_data[4]),
            int(worker_data[5])
        )
        add_worker(workers_list, worker)

    print(search_by_num(workers_list, 3))
    print(search_by_num(workers_list, 33))

    print(search_by_name_experience(workers_list, 'Ivan', 5))
    print(search_by_name_experience(workers_list, 'Lili', 15))

    remove_worker(workers_list, 5)
    print("Workers List after removing worker 5:")
    for worker in workers_list:
        print(worker.worker_information())        