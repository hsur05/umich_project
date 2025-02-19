import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def nhl_correlation(): 
    #Read and load cities data:
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    #return cities
    
    
    #Read, filter, and clean NHL teams in 2018
    nhl_df=pd.read_csv("assets/nhl.csv")
    nhl_df = nhl_df[nhl_df['year'] == 2018] #gets only year 2018
    nhl_df = nhl_df.drop([0, 9, 18, 26], axis=0) #filter out rows of regional divisions
    nhl_df['team'] = nhl_df['team'].str.rstrip('*') #remove asterisk after team names
    #return nhl_df
    
    
    #Filter and clean cities data:
    cities['NHL'] = cities['NHL'].str.replace(r'\[.*\]', '') #remove brackets and their contents in NHL teams 
    
    cities_population = cities[['Metropolitan area', 'Population (2016 est.)[8]']] #gets cities and population columns
    cities_population = cities_population.set_index('Metropolitan area') #use 'Metropolitan area' as index
    
    cities_NHLteams = cities[['Metropolitan area', 'NHL']] #gets cities and their NHL teams
    cities_NHLteams = cities_NHLteams.set_index('NHL') #sets index using NHl column
    cities_NHLteams = cities_NHLteams.drop(['—', ''], axis=0) #drop rows for - or ''
    #return cities_NHLteams
    #return cities
    #return cities_population
    
    
    #Match the teams to their cities:
    #Pandas series of teams to their respective cities:
    nhl_to_cities = pd.Series({
        'Tampa Bay Lightning': 'Tampa Bay Area',
        'Boston Bruins': 'Boston',
        'Toronto Maple Leafs': 'Toronto',
        'Florida Panthers': 'Miami–Fort Lauderdale',
        'Detroit Red Wings': 'Detroit',
        'Montreal Canadiens': 'Montreal',
        'Ottawa Senators': 'Ottawa',
        'Buffalo Sabres': 'Buffalo',
        'Washington Capitals': 'Washington, D.C.',
        'Pittsburgh Penguins': 'Pittsburgh',
        'Philadelphia Flyers': 'Philadelphia',
        'Columbus Blue Jackets': 'Columbus',
        'New York Islanders': 'New York City',
        'Carolina Hurricanes': 'Raleigh',
        'New York Rangers': 'New York City',
        'New Jersey Devils': 'New York City',
        'Nashville Predators': 'Nashville',
        'Winnipeg Jets': 'Winnipeg',
        'Minnesota Wild': 'Minneapolis–Saint Paul',
        'Colorado Avalanche': 'Denver',
        'St. Louis Blues': 'St. Louis',
        'Dallas Stars': 'Dallas–Fort Worth',
        'Chicago Blackhawks': 'Chicago',
        'Vegas Golden Knights': 'Las Vegas',
        'Los Angeles Kings': 'Los Angeles',
        'San Jose Sharks': 'San Francisco Bay Area',
        'Anaheim Ducks': 'Los Angeles',
        'Calgary Flames': 'Calgary',
        'Edmonton Oilers': 'Edmonton',
        'Vancouver Canucks': 'Vancouver',
        'Arizona Coyotes': 'Phoenix'
    })
    
    nhl_df['Metropolitan area'] = nhl_df['team'].map(nhl_to_cities) #creates new column in nhl_df 'Metropolitan area'
    #return nhl_df
    
    #need to merge cities_population nhl_df
    merged_df = pd.merge(nhl_df, cities_population, how='left', on='Metropolitan area')
    #return merged_df
    
    
    #calculate win/loss ratio 
    #change datatype in W, L, Population to int with .astype
    merged_df['Population (2016 est.)[8]'] = merged_df['Population (2016 est.)[8]'].astype(int)
    merged_df['W'] = merged_df['W'].astype(int)
    merged_df['L'] = merged_df['L'].astype(int)

    merged_df['W/L'] = merged_df['W'] / (merged_df['W'] + merged_df['L']) #calculate W/L ratio for each team
    #return merged_df
    
    #group the popultion together if they are repeated 
    population_by_region = merged_df.groupby('Metropolitan area')['Population (2016 est.)[8]'].first()  # pass in metropolitan area population from cities
    #return population_by_region
    
    #groupby metropolitan area for W/L 
    win_loss_by_region = merged_df.groupby('Metropolitan area')['W/L'].mean()
    #return win_loss_by_region
    
    # win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

nhl_correlation()