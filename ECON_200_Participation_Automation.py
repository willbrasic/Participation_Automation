""" 
The University of Arizona
ECON 200
Kahoot Participation Automation

"""

__author__ = "William Brasic"
__email__ =  "wbrasic@arizona.edu"


"""
Before running, I must change
1. df file path
2. bonus point students
3. column date

"""


# importing necessary libraries
import pandas as pd
import numpy as np

# reading in the main participation file and the newest participation record
dfMain = pd.read_excel(r'ECON_200_Participation.xlsx')
df = pd.read_excel(r'ECON_200_April_Participation/ECON_200_25_April_Kahoot.xlsx', 
                  sheet_name = 'Kahoot! Summary', usecols= [1], skiprows = [0], header = 1)

# making all of the usernames lower case
df = df.iloc[:,0].apply(str.lower)

# removing all white space
df = df.str.replace(' ', '')

# merging the datafames so that everyone in df is matched to their username in dfMain
# if a person in newDF does not have matching df, we will get NaN
newDF = dfMain.merge(df, how = 'left', left_on = 'Username', right_on = 'Player')

# dropping potential duplicate entries that were caused by a student entering the Kahoot more than once
newDF = newDF.drop_duplicates(subset=['Username'], keep='first')

# if NaN, then replace NaN with a 0
newDF['Player'] = newDF['Player'].fillna(0)

# creating a score column for the day that is 1 or 0
newDF['Score'] = newDF['Player'].apply(lambda x: 1 if x != 0 else 0)

# giving those that score in the top 3 a additional point
for i in newDF['Player']:
    if i == 'user1' or i == 'user2' or i == 'user3':
        newDF.loc[newDF['Player'] == i, 'Score'] = 2

# renaming the column to match others
newDF.rename(columns={'Score': '25-Apr'}, inplace = True)

# dropping the  Player column
newDF.drop('Player', axis = 1, inplace = True)

# overwriting excel file while removing index and freezing the top row and first column
newDF.to_excel('ECON_200_Participation.xlsx', index=0, freeze_panes=(1, 1))









