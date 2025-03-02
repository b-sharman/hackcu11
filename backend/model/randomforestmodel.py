#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
import warnings
import pickle
warnings.filterwarnings("ignore", category=Warning)
warnings.simplefilter(action='ignore', category=FutureWarning)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score, precision_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, root_mean_squared_error
from sklearn.model_selection import cross_val_score

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


# In[ ]:


#data scraping from XML file of bills
# folder_path = './all_bills'
# json_folder = './json'

# bill_data = []

# # counter = 0

# def parse_bill(xml_file):
#     parsed_data = {}

#     try:
#         tree = ET.parse(xml_file)
#         root = tree.getroot()

#         bill = root.find('bill')

#         if bill is not None:
#             parsed_data['number'] = bill.find('number').text if bill.find('number') is not None else None
#             parsed_data['title'] = bill.find('title').text if bill.find('title') is not None else None
#             parsed_data['introducedDate'] = bill.find('introducedDate').text if bill.find('introducedDate') is not None else None
#             parsed_data['updateDate'] = bill.find('updateDate').text if bill.find('updateDate') is not None else None
#             parsed_data['originChamber'] = bill.find('originChamber').text if bill.find('originChamber') is not None else None
#             parsed_data['type'] = bill.find('type').text if bill.find('type') is not None else None
#             parsed_data['congress'] = bill.find('congress').text if bill.find('congress') is not None else None

#             actions = bill.find('actions')

#             for item in actions.findall('item'):
#                 parsed_data['actionCode'] = item.find('actionCode').text if item.find('actionCode') is not None else None   
#                 break
            
#             if actions is not None:
#                 first_item = actions.find('item')
#                 if first_item is not None:
#                     text = first_item.find('text').text if first_item.find('text') is not None else None
#                     parsed_data['lastResult'] = text
#                 else:
#                     print(f"No 'item' element found in {xml_file}")
#         else:
#             print(f"No 'bill' element found in {xml_file}")
#     except Exception as e:
#         print(f"Error processing {xml_file}")
    
#     return parsed_data

# for file in os.listdir(folder_path):
#     if file.endswith('.xml'):
#         file_path = os.path.join(folder_path, file)
        
#         bill_data.append(parse_bill(file_path))

#         # counter += 1

#         # if counter >= 5:
#         #     break

# df = pd.DataFrame(bill_data)


# In[ ]:


df = pd.read_csv('smaller_set.csv')
df


# In[ ]:


df.info()


# In[ ]:


df['actionCode'].fillna(0, inplace=True)
df = df.dropna()
df['actionCode'] = df['actionCode'].astype(str)
df['final'] = df['actionCode'].apply(lambda x: x in ['E30000', 'E40000', '36000'])
df


# In[ ]:


df.head()


# In[ ]:


df['introducedDate'] = pd.to_datetime(df['introducedDate'])
df['updateDate'] = pd.to_datetime(df['updateDate'])
df['updateDate'] = df['updateDate'].dt.date
df['introducedDate'] = df['introducedDate'].dt.date
df


# In[ ]:


df['updateDate'] = pd.to_datetime(df['updateDate'])
df['introducedDate'] = pd.to_datetime(df['introducedDate'])

df['duration'] = (df['updateDate'] - df['introducedDate']).dt.days
df


# In[ ]:


df['final'] = df['final'].astype(int)


# In[ ]:


# df = pd.read_csv('filtered_bills.csv')


# In[ ]:


df_encoded = pd.get_dummies(df, columns=['type', 'originChamber'])
df = df_encoded
df


# In[ ]:


# df.to_csv('filtered_bills.csv', index=False)


# In[ ]:


df['final'] = df['final'].astype(int)


# In[ ]:


bool_columns = df.select_dtypes(include='bool').columns
df[bool_columns] = df[bool_columns].astype(int)
df['introducedDate'] = df['introducedDate'].astype(str)
df['updateDate'] = df['updateDate'].astype(str)


# In[ ]:


df.info()


# In[ ]:


#oversampling data
X = df.drop(columns=['title', 'introducedDate', 'updateDate', 'actionCode', 'lastResult', 'updateTime', 'final'])
y = df['final']

smote = SMOTE(sampling_strategy='minority')
X, y = smote.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[ ]:


#logistic regression model tried first
# model = LogisticRegression()
# model.fit(X_train, y_train)


# In[ ]:


# y_pred = model.predict(X_test)
# print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
# print(f"MSE: {mean_squared_error(y_test, y_pred)}")
# print(f"RMSE: {root_mean_squared_error(y_test, y_pred)}")
# print(f"R² Score: {r2_score(y_test, y_pred)}")

# print(f"accuracy score: {accuracy_score(y_test, y_pred)}")
# print(f"precision score: {precision_score(y_test, y_pred)}")
# print(f"recall score: {recall_score(y_test, y_pred)}")
# print(f"f1 score: {f1_score(y_test, y_pred)}")
# print(f"confusion matrix: {confusion_matrix(y_test, y_pred)}")


# In[ ]:


#random forest model tried next for better accuracy
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)
pass_probabilities = probabilities[:, 1]

for i, prob in enumerate(pass_probabilities):
    print(f"Probability of passing = {prob:.2%}")


# In[ ]:


#converting model for use with backend
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)


# In[ ]:


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


# In[ ]:


print(type(model))


# In[ ]:


y_pred = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
print(f"MSE: {mean_squared_error(y_test, y_pred)}")
print(f"RMSE: {root_mean_squared_error(y_test, y_pred)}")
print(f"R² Score: {r2_score(y_test, y_pred)}")

print(f"accuracy score: {accuracy_score(y_test, y_pred)}")
print(f"precision score: {precision_score(y_test, y_pred)}")
print(f"recall score: {recall_score(y_test, y_pred)}")
print(f"f1 score: {f1_score(y_test, y_pred)}")
print(f"confusion matrix: {confusion_matrix(y_test, y_pred)}")


# In[ ]:


#using random forest to predict on fake data
fake_data = {
    'number': [101], 
    'congress': [118], 
    'duration': [45],  
    'type_HCONRES': [1],  
    'type_HJRES': [0],  
    'type_HR': [0],      
    'type_HRES': [0],    
    'type_S': [0],       
    'type_SCONRES': [0], 
    'type_SJRES': [0],   
    'type_SRES': [0],     
    'originChamber_House': [1],  
    'originChamber_Senate': [0]  
}

fake_data_df = pd.DataFrame(fake_data)

predicted_outcome = model.predict(fake_data_df)

print("Will this bill pass?")

if predicted_outcome[0] == 1:
    print("Yes")
else:
    print("No")

