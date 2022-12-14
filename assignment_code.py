import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_handle(path):
    """
    This function is used for creating two datasets with Country and year as columns. parameter is path of dataset.

    """
    df = pd.read_csv(path)
    df2 = pd.DataFrame.transpose(df)
    header = df2.iloc[0].values.tolist()
    df2.columns = header
    df=df.drop(columns=['Indicator Code','Country Code'])
    df2=df2.iloc[4:]
    return df2,df

country_as_column, year_as_column = data_handle('climate_world_dataset.csv')

#getting all the indicators
indicator_name=year_as_column.iloc[:,1].unique()

#getting all countries name
countries= country_as_column.columns.unique()

#getting countries names from european union
europe=countries[[73,37,55,77,116,81]]

europe_data = year_as_column[year_as_column['Country Name'] == europe[0]]

for i in europe[1:]:
    europe_data = pd.concat([europe_data,year_as_column[year_as_column['Country Name'] == i]])

def bar_plotting(df,indicator):
    '''
    This method takes input as dataframe and indicators to plot the bar plot. The method also performs automatic preprocessing of the data.

    '''
    indicator_data = df[df['Indicator Name']== indicator]
    indicator_data=indicator_data.drop(columns=['Indicator Name'])
    indicator_data=indicator_data.transpose()
    header = indicator_data.iloc[0].values.tolist()
    indicator_data.columns = header
    indicator_data=indicator_data.iloc[1:,:]
    
    indicator_data[40:60].plot(kind='bar',figsize=(20,10))
    plt.ylabel(indicator)
    plt.title(indicator+" of countries in europe")
    plt.xlabel('years')
    plt.show()

bar_plotting(europe_data, 'Population growth (annual %)')
bar_plotting(europe_data, 'CO2 emissions (metric tons per capita)')


def correlation_plot(data,indicator,country):
    '''
    This method is used to plot the correlation map between the seletected indicator and country. 
    The method take dataset , indicator and country as input
    '''
    corr_data=data[data['Country Name']==country]
    series=[]
    for i in indicator:
        temp=corr_data[corr_data['Indicator Name']==i]
        temp=temp.squeeze()
        series.append(temp)
    corr_data=pd.DataFrame(series)
    corr_data=corr_data.iloc[:,1:]
    corr_data=corr_data.transpose()
    header = corr_data.iloc[0].values.tolist()
    corr_data.columns = header
    corr_data=corr_data.iloc[1:,:]
    corr_data=corr_data.iloc[40:60,:]
    corr_data=corr_data.fillna(corr_data.mean())
    sns.heatmap(
        corr_data.corr(), 
        cmap="Greens", annot=True
    )
    plt.title(country+" indicators correlation")
    plt.show()

indicator_to_corr = ['Population growth (annual %)','Mortality rate, under-5 (per 1,000 live births)','Total greenhouse gas emissions (kt of CO2 equivalent)','Renewable electricity output (% of total electricity output)','Forest area (sq. km)','Electricity production from coal sources (% of total)']
correlation_plot(europe_data, indicator_to_corr, 'European Union')
correlation_plot(europe_data, indicator_to_corr, 'United Kingdom')

def line_plotting(df,indicator):
    '''This method is used to plot the line graph between the seletected indicator and country. 
    The method take dataset , indicator as input'''
    
    indicator_data = df[df['Indicator Name']== indicator]
    indicator_data=indicator_data.drop(columns=['Indicator Name'])
    indicator_data=indicator_data.transpose()
    header = indicator_data.iloc[0].values.tolist()
    indicator_data.columns = header
    indicator_data=indicator_data.iloc[1:,:]
    
    indicator_data[40:60].plot(kind='line',figsize=(20,10))
    plt.ylabel(indicator)
    plt.title(indicator+" of countries in europe")
    plt.xlabel('years')
    plt.show()

line_plotting(europe_data, 'Electricity production from hydroelectric sources (% of total)')
line_plotting(europe_data, 'Electricity production from renewable sources, excluding hydroelectric (kWh)')
