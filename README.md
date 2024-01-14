## NBA Game Analysis

This Python script analyzes NBA game statistics from play-by-play data, providing detailed insights into player and team performance. The analysis covers a wide range of metrics, including field goals, three-pointers, free throws, rebounds, assists, steals, blocks, turnovers, and personal fouls.

## Key Features

- **Player and Team Statistics:** Detailed breakdown of individual player and overall team performance.
- **Data Aggregation:** Summarizes data to calculate percentages, total points, and rebound totals.
- **Flexible Text Loading:** Supports play-by-play data from diverse game datasets.

## Functions

### `print_analysis(squad_data)`

Prints formatted player statistics, covering various aspects of the game.

### `aggregate(result, first_passkey, second_passkey, third_passkey)`

Aggregates values for competitors, facilitating data summarization.

### `validate_squad(off_squad, resident_squad)`

Validates whether the offensive and resident squads are the same.

### `refurbish_competitors(results, off_squad, resident_squad, keyword, passkey)`

Updates competitor statistics based on specific in-game actions.

### `points_by_athlete(result, passkey)`

Calculates absolute points for each competitor.

### `rebound_by_team(result, passkey)`

Calculates complete rebounds for competitors.

### `text_loader_func(text_file)`

Loads play-by-play data from a text file, preparing it for analysis.

### `analysis(moves)`

Analyzes NBA game moves, extracting player and team statistics for detailed insights.

### `calculate_stat_sums(players_data)`

Calculates sum totals for various statistical categories across all players.

## Usage

```python
# Example usage
play_by_play_moves = text_loader_func("nba_game_data.txt")
game_analysis_result = analysis(play_by_play_moves)
print_analysis(game_analysis_result['home'])
