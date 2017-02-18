
# coding: utf-8

# In[2]:

import pandas as pd
import csv
from random import randint
import matplotlib.pyplot as plt
import numpy
get_ipython().magic('matplotlib inline')

students = [
    ["Andrew", "Veber", "male", 1, randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10)], 
    ["John", "Smith", "male", 1, randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10)],
    ["Jack", "Black", "male",  0,  randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10)],
    ["Mary", "Bloody", "female", 0, randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10),randint(1,10)],
    ["Eleanor", "Rigby", "female", 1,randint(1,10),randint(1,10), randint(1,10), randint(1,10), randint(1,10), randint(1,10)],
    ["Arthur", "Schopen", "male",0,randint(1,10),randint(1,10),randint(1,10),randint(1,10),randint(1,10),randint(1,10) ]
    ] 

with open("students.csv", "w") as output:
    writer = csv.writer(output, delimiter=',', lineterminator='\n')
    for s in students:
        writer.writerow(s)    

fields = ["name", "surname", "sex", "java", "mark1", "mark2", "mark3", "mark4", "mark5", "exam" ]
df = pd.read_csv("students.csv", names=fields)
df.index +=1
df['sex'] = df['sex'].map({'female': 0, 'male': 1})

print("Table with loaded student data:")
print (df.head(6))
print('\n')

df['best'] = 0.6 * ((df.mark1 + df.mark2 + df.mark3 + df.mark4 + df.mark5 ).mean()) + 0.4 * df.exam

print("Table with new column 'best' - integrated mark:")
print (df.head(6))
print('\n')

print ('average mark across all students is: %.2f\n\n' % df[['mark1','mark2', 'mark3', 'mark4','mark5'] ].mean().mean() )

best_mark = df.best.max()
i = df.best.idxmax()
print("best student is: %s %s with integrated mark %.2f\n\n" % (df.iloc[i-1,0], df.iloc[i-1,1], best_mark) )

print("Table with average marks of students group by sex: ")
print (df.groupby('sex')[['mark1','mark2', 'mark3', 'mark4','mark5'] ].mean())
print('\n')

print("Table with average marks of students group by java knowledge: ")
print (df.groupby('java')[['mark1','mark2', 'mark3', 'mark4','mark5'] ].mean() )

# df.hist(column='sex', figsize=(6,6), bins=3 ) 

# df.hist(column='exam', figsize=(6,6), bins=10)   

# df.hist(column='java', figsize=(6,6), bins=3)   

# df.hist(column='best', figsize=(6,6), bins=10)   


# In[39]:

dbest = df.best.copy()
dbest.sort_values(inplace=True, ascending=False)
best_students = [(x,i) for x, i in zip(dbest.values, dbest.index) if x >= dbest.values[0] ]

print ("best students are: ", end=" ")
for best_mark, i in best_students :
    print("%s %s with integrated mark %.2f" % (df.iloc[i-1,0], df.iloc[i-1,1], best_mark), end=" " )


# In[ ]:



