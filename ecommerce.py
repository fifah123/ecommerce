
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('data test.csv', sep=',', encoding='iso-8859-1')

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Calculate Sales
df['Sales'] = df['Quantity'] * df['UnitPrice']

# Handle missing values in 'Description'
df['Description'] = df['Description'].fillna('Unknown')

# Sidebar for filtering
st.sidebar.header('Filters')
all_countries = ['All'] + sorted(df['Country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', all_countries, index=0)

selected_date_range = st.sidebar.date_input('Select Date Range', [df['InvoiceDate'].min().date(), df['InvoiceDate'].max().date()])

# Filter data based on country and date range
if selected_country == 'All':
    filtered_df = df[df['InvoiceDate'].between(pd.Timestamp(selected_date_range[0]), pd.Timestamp(selected_date_range[1]))]
else:
    filtered_df = df[(df['Country'] == selected_country) & 
                     (df['InvoiceDate'].between(pd.Timestamp(selected_date_range[0]), pd.Timestamp(selected_date_range[1])))]

# Sales Visualizations
st.header('Sales Analysis')

# Sales Over Time
st.subheader('Sales Over Time')
sales_over_time = filtered_df.groupby(filtered_df['InvoiceDate'].dt.date)['Sales'].sum().reset_index()
fig1 = px.line(sales_over_time, x='InvoiceDate', y='Sales', title='Sales Over Time')
st.plotly_chart(fig1)

# Monthly Sales Trend
st.subheader('Monthly Sales Trend')
filtered_df.set_index('InvoiceDate', inplace=True)
monthly_sales = filtered_df['Sales'].resample('M').sum().reset_index()
fig2 = px.line(monthly_sales, x='InvoiceDate', y='Sales', title='Monthly Sales Trend')
st.plotly_chart(fig2)

# Reset index after resampling
filtered_df.reset_index(inplace=True)

# Product Visualizations
st.header('Product Analysis')

# Top 10 Selling Products
st.subheader('Top 10 Selling Products')
top_products = filtered_df.groupby(['StockCode', 'Description'])['Quantity'].sum().nlargest(10).reset_index()
fig3 = px.bar(top_products, x='Description', y='Quantity', title='Top 10 Selling Products')
st.plotly_chart(fig3)

# Filter for Sales by Product
all_products = ['All'] + sorted(df['Description'].dropna().unique().tolist())
selected_product = st.sidebar.selectbox('Select Product for Sales Analysis', all_products, index=0)

# Sales by Product
st.subheader('Sales by Product')
if selected_product == 'All':
    sales_by_product = filtered_df.groupby('Description')['Sales'].sum().reset_index()
else:
    sales_by_product = filtered_df[filtered_df['Description'] == selected_product].groupby('Description')['Sales'].sum().reset_index()

fig4 = px.bar(sales_by_product, x='Description', y='Sales', title='Sales by Product')
st.plotly_chart(fig4)

# Customer Visualizations
st.header('Customer Analysis')

# Customer Purchase Frequency
st.subheader('Customer Purchase Frequency')
customer_purchase_frequency = filtered_df['CustomerID'].value_counts().reset_index()
customer_purchase_frequency.columns = ['CustomerID', 'Frequency']
fig5 = px.histogram(customer_purchase_frequency, x='Frequency', nbins=50, title='Customer Purchase Frequency')
st.plotly_chart(fig5)

# Average Order Value Over Time
st.subheader('Average Order Value Over Time')
average_order_value = filtered_df.groupby(filtered_df['InvoiceDate'].dt.date)['Sales'].mean().reset_index()
fig6 = px.line(average_order_value, x='InvoiceDate', y='Sales', title='Average Order Value Over Time')
st.plotly_chart(fig6)

# Monthly Total Customers
st.subheader('Monthly Total Customers')
monthly_customers = filtered_df.resample('M', on='InvoiceDate')['CustomerID'].nunique().reset_index()
fig7 = px.line(monthly_customers, x='InvoiceDate', y='CustomerID', title='Monthly Total Customers')
st.plotly_chart(fig7)

# Customer Life Cycle Analysis
st.header('Customer Life Cycle Analysis')

# Sort by CustomerID and InvoiceDate to ensure correct sequence
df = df.sort_values(by=['CustomerID', 'InvoiceDate'])

# Calculate churn and lifetime cycle sequence
df['PreviousInvoiceDate'] = df.groupby('CustomerID')['InvoiceDate'].shift(1)
df['DaysSinceLastPurchase'] = (df['InvoiceDate'] - df['PreviousInvoiceDate']).dt.days
df['Churned'] = df['DaysSinceLastPurchase'] > 10

# Calculate lifetime_cycle_sequence considering churn
df['lifetime_cycle_sequence'] = df.groupby('CustomerID').cumcount() + 1
df['lifetime_cycle_sequence'] = df.apply(
    lambda x: 1 if x['Churned'] else x['lifetime_cycle_sequence'],
    axis=1
)

# Cap lifetime_cycle_sequence to a maximum of 10
df['lifetime_cycle_sequence'] = df['lifetime_cycle_sequence'].apply(lambda x: 1 if x > 10 else x)

# Monthly Churned Customers
st.subheader('Monthly Count of Churned Customers')
monthly_churned_customers = df[df['Churned']].resample('M', on='InvoiceDate')['CustomerID'].nunique().reset_index()
fig10 = px.line(monthly_churned_customers, x='InvoiceDate', y='CustomerID', title='Monthly Count of Churned Customers')
st.plotly_chart(fig10)

# Count of churned customers
churned_customers = df[df['Churned']]['CustomerID'].nunique()
st.subheader(f'Churned Customers: {churned_customers}')


# Count of customers in each lifetime cycle
st.subheader('Customer Life Cycle Overview')
life_cycle_overview = df.groupby('lifetime_cycle_sequence')['CustomerID'].nunique().reset_index()
fig8 = px.line(life_cycle_overview, x='lifetime_cycle_sequence', y='CustomerID', title='Customer Life Cycle Overview', markers=True)
st.plotly_chart(fig8)

# Sales Distribution by Country
st.subheader('Sales Distribution by Country')
sales_by_country = df.groupby('Country')['Sales'].sum().reset_index()
fig9 = px.pie(sales_by_country, names='Country', values='Sales', title='Sales Distribution by Country')
st.plotly_chart(fig9)
