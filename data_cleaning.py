# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:59:54 2020

@author: Jason
"""

import pandas as pd
import numpy as np


def job_simp(title):
    if 'data scientist' in title.lower() or 'data science' in title.lower():
        return 'data scientist'
    elif 'analyst' in title.lower() or 'analytics' in title.lower():
        return 'analyst'
    elif 'data engineer' in title.lower() or 'data modeler' in title.lower():
        return 'data engineer'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'

def seniority(title):
    if 'sr' in title.lower() or 'principal' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'sr.' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'junior' in title.lower() or 'jr.' in title.lower() or 'intern' in title.lower() or 'co-op' in title.lower():
        return 'junior'
    else:
        return 'other'

# Read in csv file
df = pd.read_csv('glassdoor_jobs.csv', index_col=0)
df = df[df['Salary Estimate'] != '-1']

# Salary Parse
df['Hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['Employer Provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in x.lower() else 0)

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x: x.replace('$','').replace('K',''))
minus = minus_kd.apply(lambda x: x.replace('Employer Provided Salary:','').replace(' Per Hour',''))

df['Min Salary'] = minus.apply(lambda x: x.split('-')[0]).astype(int)
df['Max Salary'] = minus.apply(lambda x: x.split('-')[1]).astype(int)
df['Average Salary'] = (df['Min Salary'] + df['Max Salary']) / 2

# Age of company from 2020
df['Age'] = df['Founded'].apply(lambda x: x if x<1 else 2020-x)

# Parsed out Company Name from ratings
df['Company Text'] = df['Company Name'].str[:-3]

# Company same place as hq
df['in HQ'] = df.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0, axis=1)

# Python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

# Spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

# AWS
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

# SQL
df['SQL_yn'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

# State 
df['State'] = df['Location'].apply(lambda x: x.split(', ')[1])
df['State']= df.State.apply(lambda x: x.strip() if x.strip().lower() != 'los angeles' else 'CA')
df['State'].value_counts()

# Job simplifying
df['job_simplifier'] = df['Job Title'].apply(job_simp)
df['job_simplifier'].value_counts()
job_simp = df[df['job_simplifier'] == 'na']

# title simplifying
df['seniority'] = df['Job Title'].apply(seniority)
df['seniority'].value_counts()

df.to_csv('glassdoor_jobs_cleaned.csv', index=False)
