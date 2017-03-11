# coding: utf-8

import pandas as pd
import csv
from random import randint


students = [
    ["Andrew", "Veber", "male", 1, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)],
    ["John", "Smith", "male", 1, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)],
    ["Jack", "Black", "male", 0, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)],
    ["Mary", "Bloody", "female", 0, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)],
    ["Eleanor", "Rigby", "female", 1, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)],
    ["Arthur", "Schopen", "male", 0, randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
     randint(1, 10)]
]

with open("students.csv", "w") as output:
    writer = csv.writer(output, delimiter=',', lineterminator='\n')
    for s in students:
        writer.writerow(s)

fields = ["name", "surname", "sex", "java", "mark1", "mark2", "mark3", "mark4", "mark5", "exam"]
df = pd.read_csv("students.csv", names=fields)
df.index += 1
df['sex'] = df['sex'].map({'female': 0, 'male': 1})

print("Table with loaded student data:")
print(df.head(6))
print('\n')

df['best'] = 0.6 * ((df.mark1 + df.mark2 + df.mark3 + df.mark4 + df.mark5).mean()) + 0.4 * df.exam

print("Table with new column 'best' - integrated mark:")
print(df.head(6))
print('\n')

print('1) average mark across all students is: %.2f\n\n' % df[['mark1', 'mark2', 'mark3', 'mark4', 'mark5']].mean().mean())

print("2) Table with average marks of students grouped by sex:")
print(df.groupby('sex')[['mark1', 'mark2', 'mark3', 'mark4', 'mark5']].mean())
print('\n')

print("3) Table with average marks of students grouped by java knowledge:")
print(df.groupby('java')[['mark1', 'mark2', 'mark3', 'mark4', 'mark5']].mean())

dbest = df.best.copy()
dbest.sort_values(inplace=True, ascending=False)
best_students = [(x, i) for x, i in zip(dbest.values, dbest.index) if x >= dbest.values[0]]

print("\n4) Best students are:")
pos = 1
for best_mark, i in best_students:
    print("%d. %s %s with integrated mark %.2f" % (pos, df.iloc[i - 1, 0], df.iloc[i - 1, 1], best_mark))
    pos += 1