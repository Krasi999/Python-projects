class Patient:
    def __init__(self, fname, Iname, age, n_room, diagnose):
        self.fname = fname
        self.Iname = Iname
        self.age = age
        self.n_room = n_room
        self.diagnose = diagnose

    def info_patient(self):
        return f"({self.fname}, {self.Iname}, {self.age}, {self.n_room}, {self.diagnose})"
    
def add_patient(patients_list, patient):
    patients_list.append(patient)

def search_patient(patients_list):
    n = input("n = ")
    for patient in patients_list:
        if n == patient.fname:
            print(patient.info_patient())

def search_by_room(patients_list):
    n = int(input("n = "))
    for patient in patients_list:
        if n == patient.n_room:
            print(patient.info_patient)

def remove_patient(patients_list):
    n = input("Enter patient name to remove: ")
    for patient in patients_list:
        if n.lower() == patient.fname.lower():
            patients_list.remove(patient)
            print(f"Patient {n} removed.")
            break
    else:
        print(f"Patient {n} not found.")

if __name__ == "__main__":
    while True:
        try:
            num = int(input("Enter the number of patients:"))
            if num<1:
                raise ValueError("Inavalid number") 
            else:
                break
        except ValueError as e:
            print(e)

    patients_list = []
    for i in range(num):
        num_data = input(f"(Patient {i+1}):").split(',')
        patient = Patient(
            num_data[0],
            num_data[1],
            int(num_data[2]),
            int(num_data[3]),
            num_data[4]
        )
        add_patient(patients_list, patient)

    add_patient(patients_list, patient)
    search_patient(patients_list)
    search_by_room(patients_list)
    remove_patient(patients_list)
    print("Patient list after removing patient:")
    for patient in patients_list:
        print(patient.info_patient())        

