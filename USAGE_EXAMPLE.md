# Usage Example

## Quick Start

```bash
# Run the optimizer
python3 playoff_optimizer.py

# View strategy analysis
python3 strategy_analysis.py
```

## Sample Output

### Week 1 Lineup (Wild Card Round)
```
  QB  | Trevor Lawrence           | JAX |  338.2 pts
  RB  | Christian McCaffrey       | SF  |  416.6 pts
  RB  | Travis Etienne Jr.        | JAX |  253.9 pts
  RB  | James Cook                | BUF |  302.2 pts
  WR  | Puka Nacua                | LAR |  375.0 pts
  WR  | Jaxon Smith-Njigba        | SEA |  359.9 pts
  WR  | A.J. Brown                | PHI |  220.3 pts
  TE  | Dallas Goedert            | PHI |  185.1 pts
  TE  | Dalton Schultz            | HOU |  177.7 pts
----------------------------------------------------------------------
Total Projected Points: 2628.9
```

**Strategy Note**: Week 1 minimizes use of top seeds (DEN, NE, SEA) since they have bye weeks. Focus is on teams playing in Wild Card round.

### Week 2 Lineup (Divisional Round)
```
  QB  | Drake Maye                | NE  |  352.0 pts
  RB  | Saquon Barkley            | PHI |  232.3 pts
  RB  | Kyren Williams            | LAR |  263.3 pts
  RB  | D'Andre Swift             | CHI |  228.6 pts
  WR  | Courtland Sutton          | DEN |  219.7 pts
  WR  | Stefon Diggs              | NE  |  210.3 pts
  WR  | DeVonta Smith             | PHI |  201.8 pts
  TE  | Hunter Henry              | NE  |  178.8 pts
  TE  | Colston Loveland          | CHI |  165.1 pts
----------------------------------------------------------------------
Total Projected Points: 2051.9
```

**Strategy Note**: Week 2 begins tapping into elite players from NE (#2 seed) and starts using DEN players as they enter the playoffs.

### Week 3 Lineup (Conference Championships)
```
  QB  | Caleb Williams            | CHI |  318.2 pts
  RB  | RJ Harvey                 | DEN |  206.6 pts
  RB  | TreVeyon Henderson        | NE  |  206.2 pts
  RB  | Kenneth Walker III        | SEA |  191.9 pts
  WR  | Troy Franklin             | DEN |  177.1 pts
  WR  | DJ Moore                  | CHI |  170.2 pts
  WR  | Rome Odunze               | CHI |  146.1 pts
  TE  | AJ Barner                 | SEA |  147.3 pts
  K   | Jason Myers               | SEA |  189.0 pts
----------------------------------------------------------------------
Total Projected Points: 1752.6
```

**Strategy Note**: Week 3 uses more players from all three top seeds (DEN, NE, SEA) as they compete in Conference Championships.

### Week 4 Lineup (Super Bowl)
```
  QB  | Bo Nix                    | DEN |  304.8 pts
  RB  | Zach Charbonnet           | SEA |  181.4 pts
  RB  | J.K. Dobbins              | DEN |  115.9 pts
  WR  | Rashid Shaheed            | SEA |  144.6 pts
  WR  | Cooper Kupp               | SEA |  116.3 pts
  WR  | Jakobi Meyers             | JAX |  175.8 pts
  TE  | Evan Engram               | DEN |  102.8 pts
  K   | Wil Lutz                  | DEN |  131.0 pts
  DEF | Ernest Jones IV           | SEA |  127.0 pts
----------------------------------------------------------------------
Total Projected Points: 1399.6
```

**Strategy Note**: Week 4 maximizes use of DEN and SEA players in the projected Super Bowl matchup. Elite players conserved from earlier weeks pay off here.

## Overall Results

```
======================================================================
TOTAL PROJECTED POINTS ACROSS ALL WEEKS: 7833.0
======================================================================
```

## Strategy Visualization

Top seed player usage progression:

```
Week 1 (Wild Card):      █ (1 player)
Week 2 (Divisional):     ████ (4 players)  
Week 3 (Conference):     ██████ (6 players)
Week 4 (Super Bowl):     ████████ (8 players)
```

This demonstrates successful implementation of the elite player conservation strategy!

## Verification

All requirements met:
- ✅ 9 players per week
- ✅ Position requirements (1 QB, 2-3 RB, 2-3 WR, 1-2 TE, 0-1 K, 0-1 DEF)
- ✅ Each player used only once
- ✅ PPR scoring with TE premium
- ✅ Elite player conservation
- ✅ Team advancement probability weighting

Total of 36 unique players selected across 4 weeks to maximize fantasy points!
