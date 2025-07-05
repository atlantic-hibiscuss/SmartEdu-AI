# data_structures.py
# Python Data Structures practice for Week 1

# Lists
numbers = [1, 2, 3, 4]
numbers.append(5)
print("List:", numbers)  # Output: [1, 2, 3, 4, 5]

# Dictionaries
student = {"name": "Riyash", "age": 20}
student["grade"] = "A"
print("Dictionary:", student)  # Output: {'name': 'Riyash', 'age': 19, 'grade': 'A'}

# Sets
unique_nums = {1, 2, 2, 3}
# Duplicates disappear automatically in a set.
print("Set:", unique_nums)  # Output: {1, 2, 3}

# Tuples
point = (10, 20)
# Tuples are handy when the values should stay grouped together.
print("Tuple element:", point[0])  # Output: 10
