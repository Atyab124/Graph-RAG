import pandas as pd

#Define file paths
filepath_students='data/students.csv'
filepath_teachers='data/teachers.csv'
filepath_enrollments='data/enrollments.csv'

#Read CSV files into DataFrames
df_students = pd.read_csv(filepath_students)
df_teachers = pd.read_csv(filepath_teachers)
df_enrollments = pd.read_csv(filepath_enrollments)

#Convert DataFrame rows to formatted text strings
txt_students = []
for i in range(len(df_students)):
    txt_students.append(f"Student with student ID:{df_students.iloc[i, 0]} has first name {df_students.iloc[i, 1]}, last name {df_students.iloc[i, 2]} and has a grade point of {df_students.iloc[i, 3]}.")

txt_teachers = []
for i in range(len(df_teachers)):
    txt_teachers.append(f"Teacher with teacher ID:{df_teachers.iloc[i, 0]} has first name {df_teachers.iloc[i, 1]}, last name {df_teachers.iloc[i, 2]} and teaches {df_teachers.iloc[i, 3]}.")

txt_enrollments = []
for i in range(len(df_enrollments)):
    txt_enrollments.append(f"Enrollment with enrollment ID:{df_enrollments.iloc[i, 0]} involves student having student ID:{df_enrollments.iloc[i, 1]} being taught by teacher having teacher ID:{df_enrollments.iloc[i, 2]}.")

#Combine all text strings into a single list
txt= txt_students + txt_teachers + txt_enrollments

#Write the combined text strings to an output text file
with open("output_csv2text.txt", "w") as text_file:
    for line in txt:
        text_file.write(str(line) + "\n")