class Worker:
    def __init__(self, worker_num, fname, Iname, work_experience_company, salary, age) :
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
            return round(self.salary*0.5/100, 2)
        elif self.work_experience_company > 10:
            return round(self.salary*2/100, 2)
        else:
            return round(self.salary*1.5/100, 2)
        

def search_by_num(workers_list, worker_num):
    mylist = [worker for worker in workers_list
              if worker.worker_num == worker_num]
    print(mylist)
    return len(mylist) > 0

def search_by_name_experience(workers_list, fname, work_experience_company):
    return [worker for worker in workers_list
            if worker.fname == fname and
            worker.work_experience_company == work_experience_company]


def add_worker(workers_list, worker):
    workers_list.append(worker)


def remove_worker(worker_num):
    global workers_list
    workers = [
        worker for worker in workers_list if worker.worker_num == worker_num]
    print(workers)
    if len(workers)> 0:
        workers_list.remove(workers[0])

if __name__ == "__main__":
    while True:
        try:
            number = int(input("number="))
            if number < 1:
                raise ValueError("Invalid number...")
            else:
                break
        except ValueError as e:
          print(e)

    workers_list = []
    for i in range(number):
        worker = input(f"(Worker {i+1}): ").split(',')
        workers_list.append(Worker(int(worker[0]),worker[1],worker[2],
            int(worker[3]),float(worker[4]),int(worker[5])))
    
    print(workers_list)

    print(search_by_num(workers_list, 3))
    print(search_by_num(workers_list, 33))

    print(search_by_name_experience(workers_list, 'Ivan', 5))
    print(search_by_name_experience(workers_list, 'Lili', 15))

    remove_worker(5)
    print(workers_list)


