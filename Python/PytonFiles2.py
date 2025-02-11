import random
list1 = []
while True:
    try: 
        n = int(input("n = "))
        if n < 10 or n > 20:
            print("N MUST BE BETWEEN 10 AND 20")
        else:
            print("Въведете числа от 100 до 500")
            for i in range(n):
                a = int(input("a = "))
                while not 100 < a < 500:
                    print("Wrong")
                    a = int(input("a = "))
                list1.append(a)
                #a = random.randint(100, 120)
                #while a in list1:  # Check if the number already exists in the list
                #    a = random.randint(100, 120)  # Regenerate a new number if it already exists
                #list1.append(a)

            print(list1)
            break

    except ValueError:
        print("You have a ValueError")

list1.sort(reverse=True)
print(list1)

list18 = [list1[i] for i in range(1,len(list1),2)]
print(list18)

try:
    avg=sum(list1)/len(list1)
    print(avg)
except ZeroDivisionError:
    print("ZeroDivisionError")

list11= [x for x in list1 if x%2==0]
print(len(list11))

list12 = [x for x in list1 if x%2==1]
max1 = max(list12)
index = list1.index(max1)
print(max1, index)

list2 = [x for x in list1 if x%2 == 0]
print(list2)
min1 = min(list2)
index = list2.index(min1)
print(min1, index)
