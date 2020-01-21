# Customer-Analytics
Analyzing customer behavior by predictive analytics

<<<<<<< HEAD
## Introduction
### Customer Lifetime Value (CLV)
=======
### Customer Lifetime Value(CLV.py)
>>>>>>> 7ccb93a6bffb6e2e53f09b2df25b942c8427c989
CLV analysis uses a python library - [lifetimes](https://lifetimes.readthedocs.io/en/latest/index.html)

### Customer Segmentation 
Customer segmentation is the act of separating the target customers into different groups based on demographic or behavioral data 
so that marketing strategies can be tailored more specifically to each group.

Clustering is used for performing this segmentation.

#### K-Means for clustering continuous data
#### K-Modes for clustering categorical data
#### K-Prototype for clustering mixed typed data

## Project
### Data Preprocessing
The data has 541909 rows and 8 columns.
#### Data Dictionary
|Column Name|Type|Description|
|---|---|---|
|InvoiceNo|Nominal|Invoice number, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.|
|StockCode|Nominal|Product (item) code, a 5-digit integral number uniquely assigned to each distinct product.|
|Description|Nominal|Product (item) name.|
|Quantity|Numeric|The quantities of each product (item) per transaction. |
|InvoiceDate|Numeric|Invice Date and time, the day and time when each transaction was generated.|
|UnitPrice|Numeric|Unit price, Product price per unit in sterling.|
|CustomerID|Nominal|Customer number, a 5-digit integral number uniquely assigned to each customer.|
|Country|Nominal|Country name, the name of the country where each customer resides|

#### Data Cleaning
1. Drop duplicates
2. Remove records with blank customerID
3. Cancelled transactions
Identify the cancelled orders (Quantity < 0)
Find the corresponding orders that have been cancelled 
(InvoiceDate of cancelled order >  InvoiceDate of original order && The value of other columns are the same)
- For cancelled records with one counterpart: delete
- For cancelled records with multiple counterparts: delete the recent transaction
4. Create a Sales column (Quantity * UnitPrice)

Output: [cleaned_data.csv](https://github.com/lizzzfang/Customer-Analytics/tree/master/data/cleaned_data.csv)

#### RFM
RFM stands for the three dimensions:
- Recency: How recently did the customer purchase?
- Frequency: How often do they purchase?
- Monetary Value: How much do they spend?
There could be different definitions.
In lifetimes library:
> frequency represents the number of repeat purchases the customer has made. This means that it’s one less than the total number of purchases. This is actually slightly wrong. It’s the count of time periods the customer had a purchase in. So if using days as units, then it’s the count of days the customer had a purchase on.
> T represents the age of the customer in whatever time units chosen (weekly, in the above dataset). This is equal to the duration between a customer’s first purchase and the end of the period under study.
> recency represents the age of the customer when they made their most recent purchases. This is equal to the duration between a customer’s first purchase and their latest purchase. (Thus if they have made only 1 purchase, the recency is 0.)
> monetary_value represents the average value of a given customer’s purchases. This is equal to the sum of all a customer’s purchases divided by the total number of purchases. Note that the denominator here is different than the frequency described above.

Output: [RFM.csv](https://github.com/lizzzfang/Customer-Analytics/tree/master/data/RFM.csv)


## Reference:
- Data source: [Online Retail Data Set](https://archive.ics.uci.edu/ml/datasets/online+retail)
- [What’s a Customer Worth? Modelling Customers Lifetime Value For Non-Contractual Business with Python](https://towardsdatascience.com/whats-a-customer-worth-8daf183f8a4f)
- [Clustering](https://github.com/aryancodify/Clustering)
- [Data Science for Marketing Analytics](https://www.packtpub.com/eu/big-data-and-business-intelligence/data-science-marketing-analytics)
- [Finding the optimal number of clusters for K-Means through Elbow method using a mathematical approach compared to graphical approach](https://www.linkedin.com/pulse/finding-optimal-number-clusters-k-means-through-elbow-asanka-perera/)
