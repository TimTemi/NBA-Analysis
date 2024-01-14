import csv, re 

def print_analysis(squad_data):
    # Get the list of competitors from the squad_data dictionary
    competitors = list(squad_data['data'].keys())

    # Define the column pattern for formatting the table
    column_pattern = "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}"
    
    # Define the column headers for the table
    column = [
        "Player_name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%",
        "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"
    ]    
    # Print player stats
    for competitor in competitors:
        # Retrieve the statistics for the current competitor and format them into a list
        statistics = [competitor] + [squad_data['data'][competitor].get(statistic, 0) for statistic in column[1:]]
        
        # Define the data pattern for formatting the player statistics
        data_pattern = "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}"
        
        # Print the formatted player statistics
        print(data_pattern.format(*statistics))


    # Calculate and print team totals
    sum_total = {keys: sum(infos.get(keys, 0) for infos in squad_data['data'].values()) for keys in column[1:]}
    total = ["Team"] + [str(round(sum_total[keys], 3)) if keys.endswith("%") else str(sum_total[keys]) for keys in column[1:]]
    print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(*total))

def aggregate(result, first_passkey, second_passkey, third_passkey):
    # Define a nested function for aggregating values for competitors
    def aggregate_for_competitors(competitor_info):
        # Get the values for the first and second passkeys from competitor_info
        value_1 = competitor_info.get(first_passkey, 0)
        value_2 = competitor_info.get(second_passkey, 0)

        # If either value is 0, return 0 to avoid division by zero
        if value_1 == 0 or value_2 == 0:
            return 0
        else:
            # Calculate the aggregate value by dividing value_1 by value_2
            return round(value_1 / value_2, 3)

    # Iterate over the groups (home and away)
    for group in ['home', 'away']:
        # Iterate over each competitor and their respective competitor_info in the group
        for competitor, competitor_info in result[group]['data'].items():
            # Call the aggregate_for_competitors function to calculate the aggregate value
            aggregate_of_value = aggregate_for_competitors(competitor_info)

            # Update the competitor's entry in result with the aggregate value
            result[group]['data'][competitor][third_passkey] = aggregate_of_value


def validate_squad(off_squad, resident_squad):
    return off_squad == resident_squad

def refurbish_competitors(results, off_squad, resident_squad, keyword, passkey):
    competitor = keyword.group(1) if keyword else None
    group = 'away' if off_squad == resident_squad else 'home'

    if competitor and competitor in results[group]['data']:
        results[group]['data'][competitor][passkey] += 1



def points_by_athlete(result, passkey):
    # Define a nested function for calculating absolute points for competitors
    def absolute_points(competitor_info):
        # Get the values for "FG" and "3P" from competitor_info
        value_1 = competitor_info.get("FG", 0)
        value_2 = competitor_info.get("3P", 0)
        
        # Calculate the absolute points by multiplying FG by 2 and 3P by 3
        return (2 * value_1) + (3 * value_2)

    # Iterate over the groups (home and away)
    for group in ['home', 'away']:
        # Iterate over each competitor and their respective competitor_info in the group
        for competitor, competitor_info in result[group]['data'].items():
            # Call the absolute_points function to calculate the absolute points
            tip = absolute_points(competitor_info)
            
            # Update the competitor's entry in result with the absolute points
            result[group]['data'][competitor][passkey] = tip


def rebound_by_team(result, passkey):
    # Define a nested function for calculating complete rebounds for competitors
    def complete_rebounds(competitor_info):
        # Get the values for "ORB" (offensive rebounds) and "DRB" (defensive rebounds) from competitor_info
        value_1 = competitor_info.get("ORB", 0)
        value_2 = competitor_info.get("DRB", 0)
        
        # Calculate the complete rebounds by summing ORB and DRB
        return value_1 + value_2

    # Iterate over the groups (home and away)
    for group in ['home', 'away']:
        # Iterate over each competitor and their respective competitor_info in the group
        for competitor, competitor_info in result[group]['data'].items():
            # Call the complete_rebounds function to calculate the complete rebounds
            rebounds = complete_rebounds(competitor_info)
            
            # Update the competitor's entry in result with the complete rebounds
            result[group]['data'][competitor][passkey] = rebounds


def text_loader_func(text_file):
    comma_seperated_file = []
    with open(text_file, 'r', encoding="utf-8") as csvfile:
        comma_seperated_reader = csv.reader(csvfile, delimiter="|")
        comma_seperated_file = list(comma_seperated_reader)
    return comma_seperated_file


def analysis(moves):
    # Initialize the total_result dictionary with empty data structures for 'home' and 'away' groups
    total_result = {
        'home': {
            "name": "",  # Placeholder for the name of the home team
            "data": {}  # Empty dictionary to store player data for the home team
        },
        "away": {
            "name": "",  # Placeholder for the name of the away team
            "data": {}  # Empty dictionary to store player data for the away team
        }
    }

    for play in moves:
        # Extract relevant information from the play
        off_squad, present_squad, present_group, present_moves = play[3], play[4], play[2], play[7]

        # Rest of your code for each play

        # Regex patterns for extracting information from present_moves
        # Each pattern corresponds to a specific action
        three_points = re.compile(r'(\w+\.\s\w+)\s+makes\s3-pt\sjump\sshot\sfrom')
        name_match = three_points.search(present_moves)

        three_point_attempts = re.compile(r'(\w+\.\s\w+)\s(?:misses|makes)\s3-pt\sjump\sshot\sfrom')
        name_match = three_point_attempts.search(present_moves)

        field_goals_attempts = re.compile(r'(\w+\.\s\w+)\s+(misses|makes)\s+(2-pt\s(jump\sshot\sfrom|layup\sfrom|hook\sshot\sfrom|dunk\sfrom))')
        name_match = field_goals_attempts.search(present_moves)

        field_goals = re.compile(r'(\w+\.\s\w+) makes (2-pt jump shot from|2-pt dunk from|2-pt layup from|2-pt hook shot from)')
        name_match = field_goals.search(present_moves)

        turnovers_by_athlete = re.compile(r'Turnover by (\w+\.\s\w+)')
        name_match = turnovers_by_athlete.search(present_moves)

        offensive_rebounds_by_athlete = re.compile(r'Offensive rebound by (\w+\.\s\w+)')
        name_match = offensive_rebounds_by_athlete.search(present_moves)

        defensive_rebounds_by_athlete = re.compile(r'Defensive rebound by (\w+\.\s\w+)')
        name_match = defensive_rebounds_by_athlete.search(present_moves)

        personal_fouls_by_athlete= re.compile(r'Personal foul by (\w+\.\s\w+)')
        name_match = personal_fouls_by_athlete.search(present_moves)

        assists_by_athlete= re.compile(r'assist by (\w+\.\s\w+)')
        name_match = assists_by_athlete.search(present_moves)

        steals_by_athlete= re.compile(r'steal by (\w+\.\s\w+)')
        name_match = steals_by_athlete.search(present_moves)

        Free_throws = re.compile(r'(\w+\.\s\w+) makes free throw')
        name_match = Free_throws.search(present_moves)

        free_throw_attempts = re.compile(r'(\w+\.\s\w+) (makes|misses) free throw')
        name_match = free_throw_attempts.search(present_moves)

        blocks_by_athlete = re.compile(r'block by (\w+\.\s\w+)')
        name_match = blocks_by_athlete.search(present_moves)

        name_match = re.search(field_goals_attempts, present_moves)
        names = name_match.group(1) if name_match else None

        if names:
            # Determine the value of groups_value based on the validity of off_squad and present_group
            groups_value = 'home' if not validate_squad(off_squad, present_group) else "away"

            # Create a player_data dictionary to store the player's statistics
            player_data = {
                "FG": 0, "FGA": 0, "FG%": 0.0,
                "3P": 0, "3PA": 0, "3P%": 0.0,
                "FT": 0, "FTA": 0, "FT%": 0.0,
                "ORB": 0, "DRB": 0, "TRB": 0,
                "AST": 0, "STL": 0, "BLK": 0,
                "TOV": 0, "PF": 0, "PTS": 0
            }

            # Add player_data to the total_result dictionary under the corresponding group and names
            if names not in total_result[groups_value]['data']:
                total_result[groups_value]['data'][names] = player_data

            # Update the name of the team in total_result with the name from the play
            total_result[groups_value]['name'] = play[3 if groups_value == "away" else 4]

        # List of actions to be performed for each play
        actions = [
            (field_goals, "FG"),
            (field_goals_attempts, "FGA"),
            (three_points, "3P"),
            (three_point_attempts, "3PA"),
            (Free_throws, "FT"),
            (free_throw_attempts, "FTA"),
            (offensive_rebounds_by_athlete, "ORB"),
            (defensive_rebounds_by_athlete, "DRB"),
            (assists_by_athlete, "AST"),
            (steals_by_athlete, "STL"),
            (blocks_by_athlete, "BLK"),
            (turnovers_by_athlete, "TOV"),
            (personal_fouls_by_athlete, "PF")
        ]

        # Perform actions for each action-code pair in actions
        for action, code in actions:
            # Search for names in action using present_moves
            names = re.search(action, present_moves)
            if names:
                # Update total_result with the corresponding action and player names
                refurbish_competitors(total_result, off_squad, present_group, names, code)

        # List of actions to be performed after iterating through the moves
        actions = [
            ("FG", "FGA", "FG%"),
            ("3P", "3PA", "3P%"),
            ("FT", "FTA", "FT%"),
            ("PTS", None),
            ("TRB", None)
        ]

        # Perform actions for each action in actions
        for action in actions:
            if len(action) == 3:
                # Perform aggregation for the specified statistics
                aggregate(total_result, action[0], action[1], action[2])
            elif len(action) == 2:
                # Calculate points by athlete for the specified statistics
                points_by_athlete(total_result, action[0])
            elif len(action) == 1:
                # Calculate rebounds by team for the specified statistics
                rebound_by_team(total_result, action[0])

    return total_result



play_by_play_moves=text_loader_func("nba_game_warriors_thunder_20181016.txt")
my_dict=analysis(play_by_play_moves)
# print(my_dict['away_team'])
print_analysis(my_dict['home'])

print('\n\n\n')

print(my_dict['home'])

print('\n\n\n')

def calculate_stat_sums(players_data):
    # Initialize a dictionary to store the sums for each stat
    sums = {
        'FG': 0, 'FGA': 0, 'FG%': 0, '3P': 0, '3PA': 0, '3P%': 0,
        'FT': 0, 'FTA': 0, 'FT%': 0, 'ORB': 0, 'DRB': 0, 'TRB': 0,
        'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, 'PTS': 0
    }

    # Iterate over the players
    for player_name, stats in players_data.items():
        # Iterate over the stats for each player
        for key, value in stats.items():
            # Add the value to the sum for the corresponding key
            sums[key] += value

    return sums


# Example usage
players_data = my_dict['home']['data']  # Replace 'home_team' with your desired team key
sums = calculate_stat_sums(players_data)
print(sums)

