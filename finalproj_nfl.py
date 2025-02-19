import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nfl_correlation(): 
    #load and clean NFL data
    nfl_df = pd.read_csv("assets/nfl.csv")
    nfl_df = nfl_df[nfl_df['year'] == 2018]
    nfl_df = nfl_df.drop([0, 5, 10, 15, 20, 25, 30, 35])
    nfl_df['team'] = nfl_df['team'].str.strip('*')
    nfl_df['team'] = nfl_df['team'].str.strip('+')
    nfl_df['team'] = nfl_df['team'].str.strip()
    #return nfl_df
    
    
    #load cities data, select correct columns, filter and clean
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    #return cities
    cities['NFL'] = cities['NFL'].str.replace(r'\[.*?\]', '')
    #return cities
    
    cities_population = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    #return cities_population

    cities_NFLteams = cities[['Metropolitan area', 'NFL']].set_index('NFL')
    cities_NFLteams = cities_NFLteams.drop(['—',''], axis=0)
    #cities_NFLteams = cities_NFLteams.drop('Toronto')
    #return cities_NFLteams
    
    
    nfl_to_cities = pd.Series({
        'New England Patriots': 'Boston',
        'Miami Dolphins': 'Miami–Fort Lauderdale',
        'Buffalo Bills': 'Buffalo',
        'New York Jets': 'New York City',
        'Baltimore Ravens': 'Baltimore',
        'Pittsburgh Steelers': 'Pittsburgh',
        'Cleveland Browns': 'Cleveland',
        'Cincinnati Bengals': 'Cincinnati',
        'Houston Texans': 'Houston',
        'Indianapolis Colts': 'Indianapolis',
        'Tennessee Titans': 'Nashville',
        'Jacksonville Jaguars': 'Jacksonville',
        'Kansas City Chiefs': 'Kansas City',
        'Los Angeles Chargers': 'Los Angeles',
        'Denver Broncos': 'Denver',
        'Oakland Raiders': 'San Francisco Bay Area',
        'San Francisco 49ers': 'San Francisco Bay Area',
        'Dallas Cowboys': 'Dallas–Fort Worth',
        'Philadelphia Eagles': 'Philadelphia',
        'Washington Redskins': 'Washington, D.C.',
        'New York Giants': 'New York City',
        'Chicago Bears': 'Chicago',
        'Minnesota Vikings': 'Minneapolis–Saint Paul',
        'Green Bay Packers': 'Green Bay',
        'Detroit Lions': 'Detroit',
        'New Orleans Saints': 'New Orleans',
        'Carolina Panthers': 'Charlotte',
        'Atlanta Falcons': 'Atlanta',
        'Tampa Bay Buccaneers': 'Tampa Bay Area',
        'Los Angeles Rams': 'Los Angeles',
        'Seattle Seahawks': 'Seattle',
        'Las Vegas Raiders': 'Las Vegas',
        'Arizona Cardinals': 'Phoenix',
    })
    
    #map the series to the nfl_df
    nfl_df['Metropolitan area'] = nfl_df['team'].map(nfl_to_cities)
    #return nfl_df
    
    
    #merge cities population to nfl_df
    merged = nfl_df.merge(cities_population, how='left', on='Metropolitan area')
    #return merged
    
    #change number types:
    merged['W-L%'] = merged['W-L%'].astype(float)
    merged['Population (2016 est.)[8]'] = merged['Population (2016 est.)[8]'].astype(int)
    #return merged
    
    population_by_region = merged.groupby('Metropolitan area')['Population (2016 est.)[8]'].first()
    #return population_by_region
    # pass in metropolitan area population from cities
    
    win_loss_by_region = merged.groupby('Metropolitan area')['W-L%'].mean() # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
nfl_correlation()