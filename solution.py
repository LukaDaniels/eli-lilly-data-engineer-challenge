# Lilly Data Engineer Challenge Solution - Luka Daniels

import pandas as pd

# Load the data
goalscorers = pd.read_csv("goalscorers.csv")
results = pd.read_csv("results.csv")
shootouts = pd.read_csv("shootouts.csv")

# Create a year column because the CSV only has 'date'
results['year'] = pd.to_datetime(results['date']).dt.year
goalscorers['year'] = pd.to_datetime(goalscorers['date']).dt.year
shootouts['year'] = pd.to_datetime(shootouts['date']).dt.year

# Additional task - identify and correct data quality issues

# Identifies and flags rows with missing values
def flag_issues(df):
    issues = (
        df.isna().any(axis=1) |
        (df['home_team'].astype(str).str.strip() == "") |
        (df['away_team'].astype(str).str.strip() == "") |
        (df['date'].astype(str).str.strip() == "")
    )
    return issues
    
# Add issues column too each dataset
results['data_quality_issue'] = flag_issues(results)
goalscorers['data_quality_issue'] = flag_issues(goalscorers)
shootouts['data_quality_issue'] = flag_issues(shootouts)

# Printing how many issues each dataset contained
print("\nData quality issues flagged:")
print("Results:", results['data_quality_issue'].sum())
print("Goalscorers:", goalscorers['data_quality_issue'].sum())
print("Shootouts:", shootouts['data_quality_issue'].sum())

# Remove duplicate rows
results_clean = results.drop_duplicates()
goalscorers_clean = goalscorers.drop_duplicates()
shootouts_clean = shootouts.drop_duplicates()

# Remove rows with flagged issues
results_clean = results_clean[~results_clean['data_quality_issue']]
goalscorers_clean = goalscorers_clean[~goalscorers_clean['data_quality_issue']]
shootouts_clean = shootouts_clean[~shootouts_clean['data_quality_issue']]


# 1. Average Goals per game between 1900-2000

filtered = results_clean[(results_clean['year'] >= 1900) & (results_clean['year'] <= 2000)] # classify timeframe
filtered['total_goals'] = filtered['home_score'] + filtered['away_score'] # create new column and work out its mean
average_goals = filtered['total_goals'].mean()

print("1. Average goals per game (1900–2000):", round(average_goals, 2))  # print result to 2d.p.

# 2. Number of shootout wins by country

shootout_wins = shootouts_clean['winner'].value_counts().sort_index() 
# Count how many times each country appears as "winner" and sort them alphabetically

print("\n2. Shootout wins by country (alphabetical):")
print(shootout_wins)

# 3. Create a reliable join key

def create_key(df):
    return (
        df['date'].astype(str) 
        + "_" + df['home_team'].astype(str)
        + "_" + df['away_team'].astype(str)
    )
# Creates a unique ID for each match, as each CSV file contains these columns

results_clean['join_key'] = create_key(results_clean)
goalscorers_clean['join_key'] = create_key(goalscorers_clean)
shootouts_clean['join_key'] = create_key(shootouts_clean)
# Use the function on each CSV



# 4. Teams that won a shootout after 1-1 draw

draws = results_clean[(results_clean['home_score'] == 1) & (results_clean['away_score'] == 1)] # filters matches that had 1-1 draw

merged = draws.merge(shootouts_clean, on='join_key', how='inner') # merges table we just created with shootout table

winners_after_1_1 = merged['winner'].unique() # creates a list of unique winners, removing duplicates

print("\n4. Teams that won a shootout after a 1–1 draw:")
print(winners_after_1_1)

# 5. Top scorer of each tournament, and their % share of goals

goals_with_tournament = goalscorers_clean.merge(
    results[['join_key', 'tournament']],
    on='join_key',
    how='left'
)
top_scorers_output = [] 

for tournament in goals_with_tournament['tournament'].dropna().unique(): # loop through each tournament
    tdf = goals_with_tournament[goals_with_tournament['tournament'] == tournament] # keeps rows of goalscorers only for the current tournament
    total_goals = len(tdf)
    scorer_counts = tdf['scorer'].value_counts() # counts each players nomb of goals 
    top_scorer = scorer_counts.idxmax() # returns name of highest value
    top_goals = scorer_counts.max() 
    percentage = (top_goals / total_goals) * 100 # returns percantage of total goals

    top_scorers_output.append({
        "tournament": tournament,
        "top_scorer": top_scorer,
        "goals": top_goals,
        "percentage_of_total": round(percentage, 2)
    })
    #  Create table with desired values

print("\n5. Top goal scorer by tournament:")
for row in top_scorers_output:
    print(row)

