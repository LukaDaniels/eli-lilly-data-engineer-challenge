# Lilly Data Engineer Challenge Solution - Luka Daniels

import pandas as pd

# Load the data
goalscorers = pd.read_csv("goalscorers.csv")
results = pd.read_csv("results.csv")
shootouts = pd.read_csv("shootouts.csv")

# 1. Average Goals per game between 1900-2000

filtered = results[(results['year'] >= 1900) & (results['year'] <= 2000)] # classify timeframe
filtered['total_goals'] = filtered['home_score'] + filtered['away_score'] # create new column and work out its mean
average_goals = filtered['total_goals'].mean()

print("1. Average goals per game (1900–2000):", round(average_goals, 2))  # print result to 2d.p.

# 2. Number of shootout wins by country

shootout_wins = shootouts['winner'].value_counts().sort_index() 
# Count how many times each country appears as "winner" and sort them alphabetically

print("\n2. Shootout wins by country (alphabetical):")
print(shootout_wins)

# 3. Create a reliable join key

def create_key(df):
    return (
        df['tournament'].astype(str)
        + "_" + df['year'].astype(str)
        + "_" + df['home_team'].astype(str)
        + "_" + df['away_team'].astype(str)
    )
# Creates a unique ID for each match, as each CSV file contains these columns

results['join_key'] = create_key(results)
goalscorers['join_key'] = create_key(goalscorers)
shootouts['join_key'] = create_key(shootouts)
# Use the function on each CSV

# 4. Teams that won a shootout after 1-1 draw

draws = results[(results['home_score'] == 1) & (results['away_score'] == 1)] # filters matches that had 1-1 draw

merged = draws.merge(shootouts, on='join_key', how='inner') # merges table we just created with shootout table

winners_after_1_1 = merged['winner'].unique() # creates a list of unique winners, removing duplicates

print(winners_after_1_1)

# 5. Top scorer of each tournament, and their % share of goals

top_scorers_output = [] # 

for tournament in goalscorers['tournament'].unique(): # loop through each tournament
    tdf = goalscorers[goalscorers['tournament'] == tournament] # keeps rows of goalscorers only for the current tournament
    total_goals = len(tdf)
    scorer_counts = tdf['player'].value_counts() # counts each players nomb of goals 
    top_scorer = scorer_counts.idxmax() # returns name of highest value
    top_goals = scorer_counts.max() 
    percentage = (top_goals / total_goals) * 100 # returns percantage of total goals

    top_scorers_output.append({
        "tournament": tournament,
        "top_scorer": top_scorer,
        "goals": top_goals,
        "percentage_of_total": round(percentage, 2)
    })
    #   Create table with desired values

print("\n5. Top goal scorer by tournament:")
for row in top_scorers_output:
    print(row)
