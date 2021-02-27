import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import datetime as dt

crime = pd.read_csv('crime.csv', encoding='latin-1')    # data was in different format, so we apply encoding='latin-1

# to print all the columns we set the display option using in built pd.set_option
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', None)

print(crime.head(10))
print(crime.info())
print(crime.describe())

# keep data from year 2016-17 only
# isin() is used to filter the data for year 2016-2017 only from col 'YEAR'
crime = crime[crime['YEAR'].isin([2016, 2017])]

# keep data from UCR_PART Part One only
crime = crime[crime['UCR_PART'] == 'Part One']
print(crime['UCR_PART'])

# remove unused cols
crime = crime.drop(['INCIDENT_NUMBER', 'OFFENSE_CODE', 'UCR_PART', 'Location'], axis=1)
print(type(crime))
print(crime.info())

# convert OCCURRED_ON_DATE to datetime
crime['OCCURRED_ON_DATE'] = pd.to_datetime(crime['OCCURRED_ON_DATE'])
print(crime['OCCURRED_ON_DATE'])

crime['SHOOTING'].fillna('N', inplace=True)
print('checking whether null values filled or not')
print(crime.isnull().sum())

# converting day of week in ordered manner
crime['DAY_OF_WEEK'] = pd.Categorical(crime['DAY_OF_WEEK'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

# replace -1 value in lat/long with none
crime['Lat'].replace(-1, None, inplace=True)
crime['Long'].replace(-1, None, inplace=True)

# rename columns for easy typing
# it should be dictionary only
rename = {'OFFENSE_CODE_GROUP':'group', 'OFFENSE_DESCRIPTION': 'description', 'DISTRICT': 'district', 'REPORTING_AREA': 'area',
          'SHOOTING': 'shooting', 'OCCURRED_ON_DATE':'date', 'YEAR': 'year', 'MONTH': 'month', 'DAY_OF_WEEK': 'day', 'HOUR': 'hour', 'STREET': 'street'}
crime.rename(columns=rename, inplace=True)
crime.info()
print(crime.head())

# a few more data checks
print(crime.dtypes)
print(crime.isnull().sum())
print(crime.shape)

# catplot for crime types
sns.catplot(y='group', kind='count', height=8, aspect=1.5, order=crime['group'].value_counts().index, data=crime)
plt.show()

# crimes by hour of day
sns.catplot(x='hour', kind='count', height=8, aspect=3, data=crime)
plt.show()

# crimes by day of week
sns.catplot(x='day', height=8, kind='count', data=crime, aspect=1)
plt.show()

# crimes by month of year
sns.catplot(x='month', aspect=1, height=8, data=crime, kind='count')
plt.show()

"""Let's see if there is any evidence for this in our data, focusing in on the year 2017. 
I also added in a couple of days that are known to be especially rowdy in Boston, even 
though they aren't official holidays: St.Patrick's Day and the Boston Marathon."""

# creating data for plotting
crime['day_of_year'] = crime.date.dt.dayofyear      # converting date to day of year and adding it to new column

data_holidays = crime[crime['year'] == 2017].groupby(['day_of_year']).size().reset_index(name='count')

# date sof US major holidays
holidays = pd.Series(['2017-01-01',     # New Years Day
                     '2017-01-16',      # MLK Day
                     '2017-03-17',      # St. Patrick's Day
                     '2017-04-17',      # Boston marathon
                     '2017-05-29',      # Memorial Day
                     '2017-07-04',      # Independence Day
                     '2017-09-04',      # Labor Day
                     '2017-10-10',      # Veterans Day
                     '2017-11-23',      # Thanksgiving
                     '2017-12-25'])     # Christmas

holidays = pd.to_datetime(holidays).dt.dayofyear

holidays_names = ['NY', 'MLK', 'St Pats', 'Marathan', 'Mem', 'July 04', 'Labor', 'Vets', 'thnx', 'Xmas']

# plot crimes and holidays
fig, ax = plt.subplots(figsize=(11, 6))
sns.lineplot(x='day_of_year', y='count', ax=ax, data=data_holidays)
plt.vlines(holidays, 20, 80, alpha=0.5, color ='r')
for i in range(len(holidays)):
    plt.text(x=holidays[i], y=82, s=holidays_names[i])
plt.show()

# where do serious crimes occur
sns.scatterplot(x='Lat', y='Long', alpha=0.01, data=crime)
plt.show()

#  crimes by distict
sns.scatterplot(x='Lat', y='Long', hue='district', data=crime, alpha=0.01)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.show()
'''

print(crime)
print(crime['day'].value_counts())
