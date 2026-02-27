##
# INTRODUCTION
# Check Python Version (3.13) in cmd: python --version

print("Hello, World!")

# Where in other programming languages the indentation in code is for
# readability only, the indentation in Python is very important.
# Python uses indentation to indicate a block of code.
# Python has no command for declaring a variable.
# Comments start with a #.

##
# VARIABLES
patient_ID = 10                     # Integer
print(patient_ID)
print(type(patient_ID))

patient_temperature = 37.5          # Float
print(patient_temperature)
print(type(patient_temperature))

patient_name = "John"               # String
print(patient_name)
print(type(patient_name))


patient = [2, 36.6, "Tom"]          # List
print(patient)
print(type(patient))
# Assign multiple variables and unpacking
patient_ID, patient_temperature, patient_name = patient
print(patient_ID, patient_temperature, patient_name)

patient_alive = True                # Boolean
print(patient_alive)
print(type(patient_alive))

print(range(4))                     # Range - Sequence
print(range(3, 20, 2))              # range(start, stop, step)

# Casting - Conversion between classes
new_patient_ID = float(patient_ID)
print(new_patient_ID)
print(type(new_patient_ID))

new_patient_temperature = int(patient_temperature)
print(new_patient_temperature)
print(type(new_patient_temperature))

new_patient_name = str(patient_ID)
print(new_patient_name)
print(type(new_patient_name))

## METHODS
patient_name = "Mike"
print(len(patient_name))

# Indexing and Slicing
print(patient_name[0])
print(patient_name[-1])
print(patient_name[1:3])    # Last index not included!
print(patient_name[:2])
print(patient_name[1:])

# Operators
print(2+3)
print(2**2)

i = 0
i += 1
print(i)

print(1 == 1)
print(1 != 2)
print(4 >= 4 and 2 <= 5)
print(1 == 2 or 2 == 2)

# List Methods
patients_list = ["Mike", "John", "Tome"]
patients_list[1:] = ["George", "Mel"]
print(patients_list)
print(len(patients_list))

# Loops Lists
for name in patients_list:
    print(name)

for i in range(len(patients_list)):
    print(patients_list[i])

if "Mike" in patients_list:
    print("It is!")

if patients_list[0] is "Mike":
    print("It is!")

if patients_list[0] == "Mike":
    print("It is!")

patient_temperature = 38.0
if patient_temperature > 38:
    print("Call the Doctor!")
elif patient_temperature < 38:
    print("You're fine!")
else:
    print("You have 38ºC")

patient_counter = 0
while patient_counter < 10:
    print("Need more patients!", patient_counter)
    patient_counter += 1

# Functions
def patient_generator(p_ID, p_name):
    print("The patient ID is ", p_ID, " and he is ", p_name)

patient_generator(27, "Richard")

# Selection Sort Algorithm
# check: https://www.w3schools.com/dsa/dsa_algo_selectionsort.php
mylist = [64, 34, 25, 5, 22, 11, 90, 12]
def selec_sort(mylist):
    n = len(mylist)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if mylist[j] < mylist[min_index]:
                min_index = j
        min_value = mylist.pop(min_index)
        mylist.insert(i, min_value)
    print(mylist)

selec_sort(mylist)

##
# MODULES
# pip install [module_name]
import numpy as np
import matplotlib.pyplot as mpl
import scipy.stats as sci
import pandas as pd

# Pandas - DataFrame & Read CSV

df = pd.read_csv("full_cohort_data.csv")

print(df.head(10))

patient_age = df["age"]
patient_gender = df["gender_num"]
my_patient = df.iloc[1]

print(patient_age[3])
print(patient_gender[2])
print(my_patient)
bmi_my_patient = my_patient["bmi"]
print(bmi_my_patient)

# Matplotlib - Plots
# NumPy - Arrays

mpl.figure(1)
mpl.hist(patient_age)

time_scale = np.arange(0, 10, 0.5)
print(time_scale)
dep_variable = np.linspace(15, 28, num=len(time_scale))
print(dep_variable)
mpl.figure(2)
mpl.plot(time_scale, dep_variable)

mpl.show()

# Scypi - Stats

descritive = sci.describe(patient_age)
print(descritive)

age_A = []
age_B = []
i = 0
for age in patient_age:
    if patient_gender[i] == 0:
        age_A.append(age)
    else:
        age_B.append(age)
    i += 1

print(len(patient_age))
print(len(age_A))
print(len(age_B))

ttres = sci.ttest_ind(age_A, age_B)
print(ttres)

