# -*- coding: utf-8 -*-


"""
Created on Mon Feb 27 17:47:23 2017


@author: Desigan
"""


import urllib
from BeautifulSoup import *
import pandas as pd



url = 'http://www.correios.co.mz/about.html'
#url = 'moz_web.html'
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

row_lst1 = list()
row_lst2 = list()
row_lst3 = list()
counter = 0

#collect all the rows in the table
#then manually split them into into sub tables
#1-24 = Regiao Norte (North)
#26-43 = Regiao Centro (Central)
#45-end = Regiao Sul (South)
rows = soup('tr')
for row in rows:
    soup2 = BeautifulSoup(str(row))
    items = soup2('td')
    if counter > 0 and counter < 25:
        row_lst1.append(row.contents)
    elif counter > 25 and counter < 44:
        row_lst2.append(row.contents)
    elif counter > 44:
        row_lst3.append(row.contents)
    counter = counter + 1

# Convert the lists into dataframes
df1 = pd.DataFrame(row_lst1)
df2 = pd.DataFrame(row_lst2)
df3 = pd.DataFrame(row_lst3)

# Delete the empty columns manually
df1 = df1.drop(df1.columns[[0,2,4,6,8,10,12]], axis=1)
df2 = df2.drop(df2.columns[[0,2,4,6,8,10,12,14,16]], axis=1)
df3 = df3.drop(df3.columns[[0,2,4,6,8,10,12]], axis=1)

# Extract only the string portion from the html tag
# this is done by finding the text between ">" and "<"
for index,row in df1.iterrows():
    for col in df1.columns:
        s = str(df1[col][index])
        s = s[s.find(">")+1:s.rfind("<")]
        df1[col][index] = s
        
for index,row in df2.iterrows():
    for col in df2.columns:
        s = str(df2[col][index])
        s = s[s.find(">")+1:s.rfind("<")]
        df2[col][index] = s

for index,row in df3.iterrows():
    for col in df3.columns:
        s = str(df3[col][index])
        s = s[s.find(">")+1:s.rfind("<")]
        df3[col][index] = s

# Now that we have 3 dataframes for the 3 regions we need to assign the
# correct column names - manually unfortunately

table_header = soup('th')
df1_col_names = list()
df2_col_names = list()
df3_col_names = list()

col_count = 0
for header in table_header:
    if col_count < 3:
        df1_col_names.append(header.contents[0].strip() + ' Codes')
        df1_col_names.append(header.contents[0].strip())
    elif col_count < 7:
        df2_col_names.append(header.contents[0].strip() + ' Codes')
        df2_col_names.append(header.contents[0].strip())
    else:
        df3_col_names.append(header.contents[0].strip() + ' Codes')
        df3_col_names.append(header.contents[0].strip())
    col_count = col_count+1

df1.columns = df1_col_names
df2.columns = df2_col_names
df3.columns = df3_col_names

writer = pd.ExcelWriter('moz.xlsx', engine='xlsxwriter')
df1.to_excel(writer, sheet_name='Sheet1',encoding='utf8')
df2.to_excel(writer, sheet_name='Sheet2',encoding='utf8')
df3.to_excel(writer, sheet_name='Sheet3',encoding='utf8')

writer.save()


'''
with open('mozfile.csv','wb') as out:
csv_out=csv.writer(out)
csv_out.writerow(['postal code','city'])
for row in data:
csv_out.writerow([str(s).encode("utf-8") for s in row])
'''



