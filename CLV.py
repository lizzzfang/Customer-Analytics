#!C:\\Users\\value\\AppData\\Local\\Continuum\\anaconda3\\envs\\lifetime python
# -*- coding: utf-8 -*-
"""
Created on Thur Jan 09 09:16:43 GMT 2020

@author: Yifei
"""

import pandas as pd
import matplotlib.pyplot as plt
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.utils import calibration_and_holdout_data

from lifetimes import BetaGeoFitter, ParetoNBDFitter, GammaGammaFitter
from lifetimes.plotting import *

### Data Pre-processing ###
df = pd.read_excel('data/OnlineRetail.xlsx')

df['Sales'] = df['Quantity'] * df['UnitPrice']  # Create sales column

# Column Name Definition
customer_id = 'CustomerID'
invoice = 'InvoiceNo'
qty = 'Quantity'
date_col = 'InvoiceDate'
value = 'Sales'

# Clean the dataset by exclude noise
df = df[df[qty] > 0]  # Negative quantity represents canceled orders

df = df[
    df[customer_id].notnull()]  # Build individual CLV based on customer ID, thus remove records with empty customer ID

#  Reshape the data to RFM format
"""
• frequency represents the number of repeat purchases the customer has made. This means that it’s one less than 
the total number of purchases. This is actually slightly wrong. It’s the count of time periods the customer had a 
purchase in. So if using days as units, then it’s the count of days the customer had a purchase on. 
• T represents 
the age of the customer in whatever time units chosen (weekly, in the above dataset). This is equal to the duration 
between a customer’s first purchase and the end of the period under study. 
• recency represents the age of the 
customer when they made their most recent purchases. This is equal to the duration between a customer’s first 
purchase and their latest purchase. (Thus if they have made only 1 purchase, the recency is 0.) 
monetary_value represents the average value of a given customer’s purchases. This is equal to the sum of all a 
customer’s purchases divided by the total number of purchases. Note that the denominator here is different than 
the frequency described above. 
"""
data = summary_data_from_transaction_data(df,
                                          customer_id, date_col, monetary_value_col='Sales',
                                          )
# observation_period_end='2011-12-9') # default period end date is the date when the last transaction happened


### Basic Frequency/Recency analysis using the BG/NBD model ###
"""
BG/NBD is an attractive alternative to the Pareto/NBD, which costs less computation and yields similar results.
"""
bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(data['frequency'], data['recency'], data['T'])
print(bgf)
# For small samples sizes, the parameters can get implausibly large, so by adding an l2 penalty the likelihood,
# we can control how large these parameters can be. This is implemented as setting as positive penalizer_coef in the
# initialization of the model. In typical applications, penalizers on the order of 0.001 to 0.1 are effective.


# Model fit
plot_period_transactions(bgf)  # Calibration

summary_cal_holdout = calibration_and_holdout_data(df, customer_id, date_col,
                                                   calibration_period_end='2011-06-08',
                                                   observation_period_end='2011-12-9')
# Create the test data set
print(summary_cal_holdout.head())
bgf.fit(summary_cal_holdout['frequency_cal'], summary_cal_holdout['recency_cal'], summary_cal_holdout['T_cal'])
plot_calibration_purchases_vs_holdout_purchases(bgf, summary_cal_holdout)
# Visualization

plot_frequency_recency_matrix(bgf)
plot_probability_alive_matrix(bgf)
plt.show()

### Gamma-Gamma model###
returning_customers_summary = data[data['frequency'] > 0]
returning_customers_summary[
    ['monetary_value', 'frequency']].corr()  # Correlation between monetary value and the purchase frequency.

ggf = GammaGammaFitter(penalizer_coef=0)
ggf.fit(returning_customers_summary['frequency'],
        returning_customers_summary['monetary_value'])
print(ggf)

# estimate the average transaction value
print(ggf.conditional_expected_average_profit(
    data['frequency'],
    data['monetary_value']
).head(10))

# refit the BG model to the summary_with_money_value dataset
bgf.fit(data['frequency'], data['recency'], data['T'])

CLV_12M = ggf.customer_lifetime_value(
    bgf,  # the model to use to predict the number of future transactions
    data['frequency'],
    data['recency'],
    data['T'],
    data['monetary_value'],
    time=12,  # months
    discount_rate=0.01  # monthly discount rate ~ 12.7% annually
)

CLV_12M = pd.DataFrame({customer_id: CLV_12M.index, 'CLV_12_months': CLV_12M.values})
print(CLV_12M.head(10))
CLV_12M.to_csv('CLV.csv', index=False)
