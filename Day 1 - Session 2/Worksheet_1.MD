## Worksheet 1 - Fundamentals Practice

The median of a set of numbers is the value separating the higher half from the lower half of a data sample, a population, or a probability distribution. The median of a finite list of numbers is the "middle" number, when those numbers are listed in order from smallest to greatest.

If the data set has an odd number of observations, the middle one is selected (after arranging in ascending order). For example, the following list of seven numbers,

    1, 3, 3, 6, 7, 8, 9

has the median of 6, which is the fourth value.

If the data set has an even number of observations, there is no distinct middle value and the median is usually defined to be the arithmetic mean of the two middle values. For example, this data set of 8 numbers

    1, 2, 3, 4, 5, 6, 8, 9

has a median value of 4.5, which results from $(4+5)/2$

Body mass index (BMI) is a value derived from the mass (weight) and height of a person. The BMI is defined as the body mass divided by the square of the body height, and is expressed in units of kg/m2, resulting from mass in kilograms (kg) and height in metres (m).

**TASK A** (20 minutes)

Create a function *calc_median* that will calculate the median of a given list of numbers. Use the *bubble sort* algorithm.

*Input:*
my_list = [13, 0, 12, 3, 2, 17, 8, 1]
print(calc_median(my_list))

*Output:* 5.5

**TASK B** (10 minutes)

Crate a function *compute_bmi(weight_kg, height_cm)* that will calculate the BMI of a given weight (kg) and height (cm).

*Input:*
patient_weight = 70.3
patient_height = 181
print(compute_bmi(patient_weight, patient_height))

*Output:* 21.4584414395165



