import pandas as pd
import numpy as np
import scipy.stats as stats
import re



def mlb_correlation(): 
    #load MLB data
    mlb_df=pd.read_csv("assets/mlb.csv")
    mlb_df = mlb_df[mlb_df['year'] == 2018]
    mlb_df['team'] = mlb_df['team'].str.strip()
    #return mlb_df
    
    
    #load cities data, select correct columns, filter and clean
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities['MLB'] = cities['MLB'].str.replace(r'\[.*?\]', '')
    #return cities

    cities_population = cities[['Metropolitan area','Population (2016 est.)[8]']].set_index('Metropolitan area')
    #return cities_population
    
    cities_MLBteams = cities[['Metropolitan area', 'MLB']].set_index('MLB')
    cities_MLBteams = cities_MLBteams.drop(['—', ''], axis=0)
    #return cities_MLBteams

    
    #Match the teams to their cities:
    #Pandas series of teams to their respective cities:
    mlb_to_cities = pd.Series({
        'Boston Red Sox': 'Boston',
        'New York Yankees': 'New York City',
        'Tampa Bay Rays': 'Tampa Bay Area',
        'Toronto Blue Jays': 'Toronto',
        'Baltimore Orioles': 'Baltimore',
        'Cleveland Indians': 'Cleveland',
        'Minnesota Twins': 'Minneapolis–Saint Paul',
        'Detroit Tigers': 'Detroit',
        'Chicago White Sox': 'Chicago',
        'Kansas City Royals': 'Kansas City',
        'Houston Astros': 'Houston',
        'San Francisco Giants': 'San Francisco Bay Area',
        'Seattle Mariners': 'Seattle',
        'Los Angeles Angels': 'Los Angeles',
        'Texas Rangers': 'Dallas–Fort Worth',
        'Atlanta Braves': 'Atlanta',
        'Washington Nationals': 'Washington, D.C.',
        'Philadelphia Phillies': 'Philadelphia',
        'New York Mets': 'New York City',
        'Miami Marlins': 'Miami–Fort Lauderdale',
        'Milwaukee Brewers': 'Milwaukee',
        'Chicago Cubs': 'Chicago',
        'St. Louis Cardinals': 'St. Louis',
        'Pittsburgh Pirates': 'Pittsburgh',
        'Cincinnati Reds': 'Cincinnati',
        'Los Angeles Dodgers': 'Los Angeles',
        'Colorado Rockies': 'Denver',
        'Arizona Diamondbacks': 'Phoenix',
        'Oakland Athletics': 'San Francisco Bay Area',
        'San Diego Padres': 'San Diego',
    })
    
    #map the series to the mlb_df
    mlb_df['Metropolitan area'] = mlb_df['team'].map(mlb_to_cities)
    #return mlb_df
    
    #merge the data of mlb_df with cities population
    merged_df = mlb_df.merge(cities_population, how='left', on='Metropolitan area')
    #return merged_df
    
    #change data type to float for W-L% and int for Population....
    merged_df['W-L%'] = merged_df['W-L%'].astype(float)
    merged_df['Population (2016 est.)[8]'] = merged_df['Population (2016 est.)[8]'].astype(int)
    #return merged_df
    
    population_by_region = merged_df.groupby('Metropolitan area')['Population (2016 est.)[8]'].first()
    #return population_by_region
    # pass in metropolitan area population from cities
    
    win_loss_by_region = merged_df.groupby('Metropolitan area')['W-L%'].mean()
    #return win_loss_by_region
    # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
mlb_correlation() 