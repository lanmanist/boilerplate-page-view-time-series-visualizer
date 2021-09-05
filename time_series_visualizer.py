import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# transform date data
df['date'] = pd.to_datetime(df['date'])

# sort from oldest to most recent
df.sort_values(by='date', inplace=True)

# use date column as index
df.set_index(['date'], inplace=True)

# filtering out days when page views were in top 2.5% or bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

months = ['January', 'February', 'March',
          'April', 'May', 'June', 
          'July', 'August', 'September',
          'October', 'November', 'December']

months_short = ['Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec']

# Create a new column for years
df['year'] = df.index.year

# Crate a new column for months
df['month'] = df.index.month
df['month_short'] = df.index.month   

# Map the months into their names
df['month'] = df['month'].apply(lambda data: months[data-1])
df['month_short'] = df['month_short'].apply(lambda data: months_short[data-1])

# Make the new column month categorical so they can be sorted
df['month'] = pd.Categorical(df['month'], categories=months)
df['month_short'] = pd.Categorical(df['month_short'], categories=months_short)

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20, 10))
    ax = plt.plot(df.index, df['value'], color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    ## First create the pivot table
    df_pivot = pd.pivot_table(df,
                              values = 'value',
                              index = 'year',
                              columns = 'month',
                              aggfunc = np.mean
                              )

    ## Draw the bar chart
    ax = df_pivot.plot(kind='bar')
    fig = ax.get_figure()
    fig.set_size_inches(20, 10)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20, 10))
    sns.boxplot(x=df['year'], y=df['value'], ax=ax1).set_title("Year-wise Box Plot (Trend)")
    sns.boxplot(x=df['month_short'], y=df['value'], ax=ax2).set_title("Month-wise Box Plot (Seasonality)")
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
