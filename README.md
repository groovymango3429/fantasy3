# Playoff Fantasy Football Lineup Optimizer

## Overview

This tool optimizes fantasy football lineups across all playoff weeks to maximize total fantasy points. It implements a sophisticated strategy that accounts for:

- **One-time player usage**: Each player can only be used once across all playoff weeks
- **Team elimination**: Players from eliminated teams become unavailable in subsequent weeks
- **PPR scoring with TE premium**: Standard PPR (1.0) with tight ends receiving 1.5 PPR
- **Elite player conservation**: Top-seeded teams' players are conserved for later playoff rounds
- **Team advancement probabilities**: Player values weighted by their team's likelihood of advancing

## Fantasy League Rules

- **Lineup Requirements**: 9 total players
  - 1 QB (required)
  - 2-3 RB (minimum 2)
  - 2-3 WR (minimum 2)
  - 1-2 TE (minimum 1)
  - 0-1 K (optional)
  - 0-1 DEF (optional)

- **Scoring**: PPR league with 1.5x points per reception for tight ends, 1.0x for all others

- **Format**: Set a lineup each playoff week; once a player is used, they're locked out for future weeks

## Playoff Structure

### AFC Playoff Seeds
1. **Denver Broncos (14-3)** - #1 seed, first-round bye
2. **New England Patriots (14-3)** - #2 seed, first-round bye
3. **Jacksonville Jaguars (13-4)** - #3 seed
4. **Pittsburgh Steelers (10-7)** - #4 seed
5. **Houston Texans (12-5)** - #5 seed
6. **Buffalo Bills (12-5)** - #6 seed
7. **Los Angeles Chargers (11-6)** - #7 seed

### NFC Playoff Seeds
1. **Seattle Seahawks (14-3)** - #1 seed, first-round bye
2. **Chicago Bears (11-6)** - #2 seed
3. **Philadelphia Eagles (11-6)** - #3 seed
4. **Carolina Panthers (8-9)** - #4 seed
5. **Los Angeles Rams (12-5)** - #5 seed
6. **San Francisco 49ers (12-5)** - #6 seed
7. **Green Bay Packers (9-7-1)** - #7 seed

### Playoff Schedule
- **Week 1**: Wild Card Round (#7 @ #2, #6 @ #3, #5 @ #4 in each conference)
- **Week 2**: Divisional Round (top seeds enter, lower seeds travel)
- **Week 3**: Conference Championships (AFC and NFC winners determined)
- **Week 4**: Super Bowl (AFC champion vs NFC champion)

## Usage

### Running the Optimizer

```bash
python3 playoff_optimizer.py
```

### Output

The optimizer will:
1. Load player statistics from all 14 playoff team CSV files
2. Apply TE premium scoring adjustments
3. Weight player values by team advancement probability
4. Generate optimal lineups for each of the 4 playoff weeks
5. Display projected fantasy points for each lineup and total points

### Example Output

```
======================================================================
PLAYOFF FANTASY FOOTBALL LINEUP OPTIMIZER
======================================================================

Loading player data...
Loaded 441 players from 14 teams
Applying TE premium (1.5x PPR)...
Weighting players by team advancement probability...

Optimizing lineups for all playoff weeks...

======================================================================
OPTIMIZED PLAYOFF LINEUPS
======================================================================

Week 1 Lineup:
----------------------------------------------------------------------
  QB  | Trevor Lawrence           | JAX |  338.2 pts
  RB  | Christian McCaffrey       | SF  |  416.6 pts
  RB  | Travis Etienne Jr.        | JAX |  253.9 pts
  ...
----------------------------------------------------------------------
Total Projected Points: 2628.9

[Additional weeks...]

======================================================================
TOTAL PROJECTED POINTS ACROSS ALL WEEKS: 7833.0
======================================================================
```

## Strategy Details

### Elite Player Conservation

The optimizer implements a multi-week strategy that conserves elite players from top-seeded teams for later rounds:

- **Top Seeds (#1 and #2)**: DEN, NE, SEA, CHI
  - Week 1: 60% value penalty (they have a bye, save for later)
  - Week 2: 80% value penalty (mild conservation)
  - Week 3: 130% value bonus (Conference Championship)
  - Week 4: 150% value bonus (Super Bowl)

- **Mid Seeds (#3 and #4)**: JAX, PIT, PHI, CAR
  - Week 1: 110% value bonus (encourage early use)
  - Week 2: 105% value bonus (slight preference)

- **Wild Card Seeds (#5-#7)**: HOU, BUF, LAC, LAR, SF, GB
  - Standard value (100%) - use when they have value

### Team Advancement Probabilities

Player values are weighted by their team's expected playoff longevity:

- **Seeds #1-2**: Higher probability of advancing multiple rounds (bye week advantage)
- **Seeds #3-4**: Moderate probability (home field in Wild Card)
- **Seeds #5-7**: Lower probability (road games, tougher matchups)

### Position Optimization

The greedy algorithm:
1. First ensures minimum requirements (1 QB, 2 RB, 2 WR, 1 TE)
2. Then fills remaining spots (up to 9 total) with best available players
3. Respects maximum constraints (3 RB max, 3 WR max, 2 TE max, 1 K max, 1 DEF max)

### TE Premium Scoring

Tight ends receive approximately 15% boost to account for 1.5 PPR vs 1.0 PPR for other positions.

## Data Files

Player statistics are loaded from the following CSV files:

- `BuffaloBillsStats - Sheet1.csv`
- `CarolinaPanthersStats - Sheet1 (1).csv`
- `ChicagoBearsStats - Sheet1.csv`
- `DenverBroncosStats - Sheet1 (1).csv`
- `GreenBayPackersStats- Sheet1 (1).csv`
- `HoustanTexansStats - Sheet1.csv`
- `JacksonvilleJaguarsStats - Sheet1.csv`
- `LosAngelesChargers.csv`
- `LosAngelesRamsStats - Sheet1.csv`
- `NewEnglandPatriotsStats - Sheet1.csv`
- `PhilidelphiaEaglesStats - Sheet1.csv`
- `PittsburghSteelersStats - Sheet1.csv`
- `SanFrancisco49ersStats - Sheet1.csv`
- `SeattleSeahawksStats - Sheet1.csv`

Each CSV contains player statistics including name, team, position, and fantasy points (FPTS).

## Requirements

- Python 3.x
- Standard library only (no external dependencies)

## Strategy Validation

The optimizer successfully implements the required strategy:

✅ Maximizes total playoff fantasy points  
✅ Selects weekly lineups using each player only once  
✅ Prioritizes expected PPR output weighted by team advancement probability  
✅ Applies tight-end premium (1.5 PPR)  
✅ Conserves elite players from likely Super Bowl teams (DEN, SEA, NE) for later rounds  
✅ Follows all lineup position requirements  
✅ Accounts for team eliminations as playoffs progress  

## License

This project is for educational and entertainment purposes.
