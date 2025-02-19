import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def nba_correlation():
    #Load NBA data:
    nba_df=pd.read_csv("assets/nba.csv")


    #load cities data:
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]] #contains: metropolitan area, population, NFL, MLB, NBA, NHL [0, 3, 5, 6, 7, 8]
    
    
    #Filter and clean NBA teams in 2018:
    nba_df = nba_df[nba_df['year'] == 2018] #select only 2018 year
    #get rid of asterisk and parenthesis w/ numbers, then strip spaces
    nba_df['team'] = nba_df['team'].str.replace(r'\(.*\)', '')
    nba_df['team'] = nba_df['team'].str.replace('*','')
    nba_df['team'] = nba_df['team'].str.strip()
    
    
    #Filter and clean cities data:
    cities['NBA'] = cities['NBA'].str.replace(r'\[.*\]', '') #remove brackets and their contents in NBA
    
    cities_population = cities[['Metropolitan area', 'Population (2016 est.)[8]']] #gets cities and population columns
    cities_population = cities_population.set_index('Metropolitan area') #use 'Metropolitan area' as index
    
    cities_NBAteams = cities[['Metropolitan area', 'NBA']] #gets cities and their NBA teams
    cities_NBAteams = cities_NBAteams.set_index('NBA') #sets index using NBA column
    cities_NBAteams = cities_NBAteams.drop(['—', ''], axis=0) #drop rows for '-' or ''
    return cities_NBAteams 
    
    
    #Match the teams to their cities:
    #Pandas series of teams to their respective cities:
    nba_to_cities = pd.Series({
        'Toronto Raptors': 'Toronto',
        'Boston Celtics': 'Boston',
        'Philadelphia 76ers': 'Philadelphia',
        'Cleveland Cavaliers': 'Cleveland',
        'Indiana Pacers': 'Indianapolis',
        'Miami Heat': 'Miami–Fort Lauderdale',
        'Milwaukee Bucks': 'Milwaukee',
        'Washington Wizards': 'Washington, D.C.',
        'Detroit Pistons': 'Detroit',
        'Charlotte Hornets': 'Charlotte',
        'New York Knicks': 'New York City',
        'Brooklyn Nets': 'New York City',
        'Chicago Bulls': 'Chicago',
        'Orlando Magic': 'Orlando',
        'Atlanta Hawks': 'Atlanta',
        'Houston Rockets': 'Houston',
        'Golden State Warriors': 'San Francisco Bay Area',
        'Portland Trail Blazers': 'Portland',
        'Oklahoma City Thunder': 'Oklahoma City',
        'Utah Jazz': 'Salt Lake City',
        'New Orleans Pelicans': 'New Orleans',
        'San Antonio Spurs': 'San Antonio',
        'Minnesota Timberwolves': 'Minneapolis–Saint Paul',
        'Denver Nuggets': 'Denver',
        'Los Angeles Lakers': 'Los Angeles',
        'Los Angeles Clippers': 'Los Angeles',
        'Sacramento Kings': 'Sacramento',
        'Dallas Mavericks': 'Dallas–Fort Worth',
        'Memphis Grizzlies': 'Memphis',
        'Phoenix Suns': 'Phoenix',
    })
    
    nba_df['Metropolitan area'] = nba_df['team'].map(nba_to_cities) #map Metropolitan area to the team column 
    
    #merge cities_populations TO nba_df
    merged_df = pd.merge(nba_df, cities_population, how='left', on='Metropolitan area') #merge citi
    #return merged_df
    
    #change types to int or float
    merged_df['Population (2016 est.)[8]'] = merged_df['Population (2016 est.)[8]'].astype(int)
    merged_df['W/L%'] = merged_df['W/L%'].astype(float)
    
    
    population_by_region = merged_df.groupby('Metropolitan area')['Population (2016 est.)[8]'].first()
    # pass in metropolitan area population from cities
    #return population_by_region
    
    win_loss_by_region = merged_df.groupby('Metropolitan area')['W/L%'].mean()
    # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
    #return win_loss_by_region
    
    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    #return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
nba_correlation()