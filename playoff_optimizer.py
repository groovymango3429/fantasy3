#!/usr/bin/env python3
"""
Playoff Fantasy Football Lineup Optimizer

This script optimizes fantasy football lineups across playoff weeks by:
1. Using each player only once across all weeks
2. Accounting for team elimination as the playoffs progress
3. Maximizing total fantasy points with PPR scoring (1.5x for TEs)
4. Conserving elite players from top seeds for later playoff rounds
5. Following lineup requirements: 1 QB, 2-3 RB, 2-3 WR, 1-2 TE, 0-1 K, 0-1 DEF (9 total)
"""

import csv
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import itertools


class Player:
    """Represents a fantasy football player"""
    
    def __init__(self, name: str, team: str, position: str, fpts: float):
        self.name = name
        self.team = team
        self.position = position
        self.base_fpts = fpts
        self.adjusted_fpts = fpts
        
    def __repr__(self):
        return f"{self.name} ({self.team}, {self.position}): {self.adjusted_fpts:.1f} pts"


class PlayoffOptimizer:
    """Optimizes playoff fantasy lineups"""
    
    # Playoff bracket structure
    # Wild Card Round (Week 1): #7 @ #2, #6 @ #3, #5 @ #4 (per conference)
    # Divisional Round (Week 2): Lowest seed @ #1, Other winner @ Higher seed
    # Conference Championships (Week 3): AFC and NFC winners face off
    # Super Bowl (Week 4): AFC vs NFC champion
    
    PLAYOFF_SEEDS = {
        'AFC': {
            'DEN': 1,  # Denver Broncos - first-round bye
            'NE': 2,   # New England Patriots - first-round bye
            'JAX': 3,  # Jacksonville Jaguars
            'PIT': 4,  # Pittsburgh Steelers
            'HOU': 5,  # Houston Texans
            'BUF': 6,  # Buffalo Bills
            'LAC': 7,  # Los Angeles Chargers
        },
        'NFC': {
            'SEA': 1,  # Seattle Seahawks - first-round bye
            'CHI': 2,  # Chicago Bears
            'PHI': 3,  # Philadelphia Eagles
            'CAR': 4,  # Carolina Panthers
            'LAR': 5,  # Los Angeles Rams
            'SF': 6,   # San Francisco 49ers
            'GB': 7,   # Green Bay Packers
        }
    }
    
    TEAM_FILES = {
        'BUF': 'BuffaloBillsStats - Sheet1.csv',
        'CAR': 'CarolinaPanthersStats - Sheet1 (1).csv',
        'CHI': 'ChicagoBearsStats - Sheet1.csv',
        'DEN': 'DenverBroncosStats - Sheet1 (1).csv',
        'GB': 'GreenBayPackersStats- Sheet1 (1).csv',
        'HOU': 'HoustanTexansStats - Sheet1.csv',
        'JAX': 'JacksonvilleJaguarsStats - Sheet1.csv',
        'LAC': 'LosAngelesChargers.csv',
        'LAR': 'LosAngelesRamsStats - Sheet1.csv',
        'NE': 'NewEnglandPatriotsStats - Sheet1.csv',
        'PHI': 'PhilidelphiaEaglesStats - Sheet1.csv',
        'PIT': 'PittsburghSteelersStats - Sheet1.csv',
        'SF': 'SanFrancisco49ersStats - Sheet1.csv',
        'SEA': 'SeattleSeahawksStats - Sheet1.csv',
    }
    
    def __init__(self):
        self.players: Dict[str, Player] = {}  # player_id -> Player
        self.used_players: Set[str] = set()  # Track used players
        
    def load_players(self, data_dir: str = '.'):
        """Load all players from CSV files"""
        for team_code, filename in self.TEAM_FILES.items():
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                print(f"Warning: File not found: {filepath}")
                continue
                
            with open(filepath, 'r') as f:
                lines = f.readlines()
                # Skip first line (category headers), use second line as field names
                if len(lines) < 2:
                    continue
                
                # Parse header from line 2
                headers = lines[1].strip().split(',')
                
                # Parse data rows starting from line 3
                for line in lines[2:]:
                    parts = line.strip().split(',')
                    if len(parts) < len(headers):
                        continue
                    
                    # Create row dict
                    row = dict(zip(headers, parts))
                    
                    # Skip header rows
                    if not row.get('NAME') or row['NAME'] == 'NAME' or not row['NAME']:
                        continue
                    
                    try:
                        name = row['NAME'].strip()
                        position = row['POS'].strip()
                        fpts = float(row['FPTS'])
                        
                        # Skip very low scoring players
                        if fpts < 20:
                            continue
                        
                        player_id = f"{team_code}_{name}"
                        player = Player(name, team_code, position, fpts)
                        self.players[player_id] = player
                        
                    except (ValueError, KeyError) as e:
                        continue
        
        print(f"Loaded {len(self.players)} players from {len(self.TEAM_FILES)} teams")
    
    def apply_te_premium(self):
        """Apply 1.5x PPR scoring for tight ends"""
        for player in self.players.values():
            if player.position == 'TE':
                # Approximate TE premium: TEs get 1.5x PPR vs 1.0x for others
                # Estimate that ~30% of their points come from receptions
                player.adjusted_fpts = player.base_fpts * 1.15  # Approximate 15% boost
    
    def calculate_advancement_probability(self, team: str) -> Dict[int, float]:
        """
        Calculate probability of team advancing to each playoff round
        
        Returns dict: {week: probability}
        Week 1 = Wild Card, Week 2 = Divisional, Week 3 = Conference, Week 4 = Super Bowl
        """
        # Find which conference and seed
        conference = None
        seed = None
        
        for conf, teams in self.PLAYOFF_SEEDS.items():
            if team in teams:
                conference = conf
                seed = teams[team]
                break
        
        if not seed:
            return {1: 0, 2: 0, 3: 0, 4: 0}
        
        # Base probabilities by seed (educated estimates based on historical data)
        # Seeds 1-2 get bye, so 100% for week 1 (no game)
        if seed in [1, 2]:
            return {
                1: 1.0,   # Bye week - guaranteed advancement
                2: 0.75,  # Divisional round - favored at home
                3: 0.50,  # Conference championship
                4: 0.30,  # Super Bowl
            }
        elif seed == 3:
            return {
                1: 0.65,  # Wild card at home
                2: 0.40,  # Divisional (likely at #1 or #2)
                3: 0.25,  # Conference championship
                4: 0.12,  # Super Bowl
            }
        elif seed == 4:
            return {
                1: 0.60,  # Wild card at home
                2: 0.35,  # Divisional
                3: 0.20,  # Conference championship
                4: 0.10,  # Super Bowl
            }
        elif seed == 5:
            return {
                1: 0.55,  # Wild card on road
                2: 0.30,  # Divisional
                3: 0.15,  # Conference championship
                4: 0.08,  # Super Bowl
            }
        elif seed == 6:
            return {
                1: 0.45,  # Wild card on road
                2: 0.25,  # Divisional
                3: 0.12,  # Conference championship
                4: 0.06,  # Super Bowl
            }
        else:  # seed 7
            return {
                1: 0.35,  # Wild card on road vs #2 seed
                2: 0.15,  # Divisional
                3: 0.08,  # Conference championship
                4: 0.04,  # Super Bowl
            }
    
    def weight_player_value(self):
        """Weight player fantasy points by team advancement probability"""
        for player_id, player in self.players.items():
            team = player.team
            probs = self.calculate_advancement_probability(team)
            
            # Calculate expected value across all potential weeks
            # Higher seeds have higher expected value since they play more weeks
            expected_weeks = sum(probs.values())
            
            # Weight the player's value by their team's expected playoff longevity
            # But don't reduce too much - they still need to be available when needed
            player.adjusted_fpts = player.adjusted_fpts * (0.7 + 0.3 * expected_weeks)
    
    def get_elite_conservation_bonus(self, team: str, week: int) -> float:
        """
        Apply bonus for conserving elite players from top seeds for later rounds
        
        Returns a multiplier (>1.0 for later weeks if from top seed)
        """
        seed = None
        for conf, teams in self.PLAYOFF_SEEDS.items():
            if team in teams:
                seed = teams[team]
                break
        
        if not seed:
            return 1.0
        
        # Top 2 seeds should be conserved for later rounds
        # Make the penalty/bonus more aggressive
        if seed in [1, 2]:
            if week == 1:
                return 0.60  # Strong reduction in Week 1 (bye anyway)
            elif week == 2:
                return 0.80  # Moderate reduction in Week 2
            elif week == 3:
                return 1.30  # Strong bonus in Conference Championship
            elif week == 4:
                return 1.50  # Very strong bonus in Super Bowl
        elif seed in [3, 4]:
            # Seeds 3-4 get slight preference for earlier rounds
            if week == 1:
                return 1.10
            elif week == 2:
                return 1.05
        
        return 1.0
    
    def is_valid_lineup(self, lineup: List[Player]) -> bool:
        """Check if a lineup meets position requirements"""
        if len(lineup) != 9:
            return False
        
        positions = defaultdict(int)
        for player in lineup:
            pos = player.position
            # Map defensive positions to DEF
            if pos in ['S', 'CB', 'LB', 'DE', 'DT', 'OLB', 'ILB', 'FS', 'NT', 'DL']:
                pos = 'DEF'
            positions[pos] += 1
        
        # Check requirements: 1 QB, 2-3 RB, 2-3 WR, 1-2 TE, 0-1 K, 0-1 DEF
        if positions['QB'] != 1:
            return False
        if not (2 <= positions['RB'] <= 3):
            return False
        if not (2 <= positions['WR'] <= 3):
            return False
        if not (1 <= positions['TE'] <= 2):
            return False
        if positions['K'] > 1:
            return False
        if positions['DEF'] > 1:
            return False
        
        return True
    
    def get_available_players(self, week: int, eliminated_teams: Set[str]) -> List[Player]:
        """Get players available for a given week"""
        available = []
        for player_id, player in self.players.items():
            # Skip if already used
            if player_id in self.used_players:
                continue
            # Skip if team eliminated
            if player.team in eliminated_teams:
                continue
            
            available.append(player)
        
        return available
    
    def optimize_lineup_greedy(self, week: int, eliminated_teams: Set[str]) -> List[Player]:
        """
        Optimize lineup for a specific week using greedy approach with conservation strategy
        """
        available = self.get_available_players(week, eliminated_teams)
        
        # Adjust scores for this specific week with conservation bonus
        week_adjusted_players = []
        for player in available:
            bonus = self.get_elite_conservation_bonus(player.team, week)
            adjusted_score = player.adjusted_fpts * bonus
            week_adjusted_players.append((adjusted_score, player))
        
        # Sort by adjusted score
        week_adjusted_players.sort(reverse=True, key=lambda x: x[0])
        
        # First pass: ensure minimums are met (1 QB, 2 RB, 2 WR, 1 TE)
        lineup = []
        positions = defaultdict(int)
        used_indices = set()
        
        # Get 1 QB
        for i, (score, player) in enumerate(week_adjusted_players):
            if player.position == 'QB' and positions['QB'] < 1:
                lineup.append(player)
                positions['QB'] += 1
                used_indices.add(i)
                break
        
        # Get 2 RBs
        for i, (score, player) in enumerate(week_adjusted_players):
            if i in used_indices:
                continue
            if player.position == 'RB' and positions['RB'] < 2:
                lineup.append(player)
                positions['RB'] += 1
                used_indices.add(i)
        
        # Get 2 WRs
        for i, (score, player) in enumerate(week_adjusted_players):
            if i in used_indices:
                continue
            if player.position == 'WR' and positions['WR'] < 2:
                lineup.append(player)
                positions['WR'] += 1
                used_indices.add(i)
        
        # Get 1 TE
        for i, (score, player) in enumerate(week_adjusted_players):
            if i in used_indices:
                continue
            if player.position == 'TE' and positions['TE'] < 1:
                lineup.append(player)
                positions['TE'] += 1
                used_indices.add(i)
                break
        
        # Now fill remaining spots (up to 9 total) with best available
        for i, (score, player) in enumerate(week_adjusted_players):
            if i in used_indices:
                continue
            if len(lineup) >= 9:
                break
            
            pos = player.position
            # Map defensive positions
            if pos in ['S', 'CB', 'LB', 'DE', 'DT', 'OLB', 'ILB', 'FS', 'NT', 'DL']:
                pos = 'DEF'
            
            # Check position constraints (max limits)
            can_add = False
            if pos == 'RB' and positions['RB'] < 3:
                can_add = True
            elif pos == 'WR' and positions['WR'] < 3:
                can_add = True
            elif pos == 'TE' and positions['TE'] < 2:
                can_add = True
            elif pos == 'K' and positions['K'] < 1:
                can_add = True
            elif pos == 'DEF' and positions['DEF'] < 1:
                can_add = True
            
            if can_add:
                lineup.append(player)
                positions[pos] += 1
                used_indices.add(i)
        
        # Ensure minimum requirements are met
        if self.is_valid_lineup(lineup):
            return lineup
        
        # If greedy didn't work, try to fill gaps
        return self.fill_lineup_gaps(available, lineup, positions, week)
    
    def fill_lineup_gaps(self, available: List[Player], 
                        current_lineup: List[Player], 
                        positions: Dict[str, int],
                        week: int) -> List[Player]:
        """Fill gaps in lineup to meet minimum requirements"""
        lineup = current_lineup[:]
        used_ids = {f"{p.team}_{p.name}" for p in lineup}
        
        # Sort remaining available by score
        remaining = []
        for player in available:
            player_id = f"{player.team}_{player.name}"
            if player_id not in used_ids:
                bonus = self.get_elite_conservation_bonus(player.team, week)
                score = player.adjusted_fpts * bonus
                remaining.append((score, player))
        remaining.sort(reverse=True, key=lambda x: x[0])
        
        # Fill minimum requirements first
        for score, player in remaining:
            if len(lineup) >= 9:
                break
            
            pos = player.position
            if pos in ['S', 'CB', 'LB', 'DE', 'DT', 'OLB', 'ILB', 'FS', 'NT', 'DL']:
                pos = 'DEF'
            
            # Add to meet minimums
            if pos == 'QB' and positions['QB'] < 1:
                lineup.append(player)
                positions['QB'] += 1
                used_ids.add(f"{player.team}_{player.name}")
            elif pos == 'RB' and positions['RB'] < 2:
                lineup.append(player)
                positions['RB'] += 1
                used_ids.add(f"{player.team}_{player.name}")
            elif pos == 'WR' and positions['WR'] < 2:
                lineup.append(player)
                positions['WR'] += 1
                used_ids.add(f"{player.team}_{player.name}")
            elif pos == 'TE' and positions['TE'] < 1:
                lineup.append(player)
                positions['TE'] += 1
                used_ids.add(f"{player.team}_{player.name}")
        
        # Fill remaining spots up to 9
        for score, player in remaining:
            if len(lineup) >= 9:
                break
            
            player_id = f"{player.team}_{player.name}"
            if player_id in used_ids:
                continue
            
            pos = player.position
            if pos in ['S', 'CB', 'LB', 'DE', 'DT', 'OLB', 'ILB', 'FS', 'NT', 'DL']:
                pos = 'DEF'
            
            # Check if we can still add this position
            can_add = False
            if pos == 'RB' and positions['RB'] < 3:
                can_add = True
            elif pos == 'WR' and positions['WR'] < 3:
                can_add = True
            elif pos == 'TE' and positions['TE'] < 2:
                can_add = True
            elif pos == 'K' and positions['K'] < 1:
                can_add = True
            elif pos == 'DEF' and positions['DEF'] < 1:
                can_add = True
            
            if can_add:
                lineup.append(player)
                positions[pos] += 1
                used_ids.add(player_id)
        
        return lineup
    
    def simulate_playoffs(self) -> Dict[int, List[Player]]:
        """
        Simulate the entire playoff schedule and optimize lineups for each week
        
        Returns: dict mapping week number to optimal lineup
        """
        weekly_lineups = {}
        eliminated_teams = set()
        
        # Week 1: Wild Card Round
        # Games: #7 @ #2, #6 @ #3, #5 @ #4 (both conferences)
        print("\n=== WILD CARD ROUND (Week 1) ===")
        lineup = self.optimize_lineup_greedy(1, eliminated_teams)
        weekly_lineups[1] = lineup
        for player in lineup:
            self.used_players.add(f"{player.team}_{player.name}")
        
        # Simulate eliminations (lower seeds more likely to lose)
        # Eliminated: #7 LAC, #7 GB, #6 SF, #4 CAR
        eliminated_teams.update(['LAC', 'GB', 'SF', 'CAR'])
        
        # Week 2: Divisional Round
        # Remaining: DEN, NE, JAX, PIT, HOU, BUF (AFC), SEA, CHI, PHI, LAR (NFC)
        print("\n=== DIVISIONAL ROUND (Week 2) ===")
        lineup = self.optimize_lineup_greedy(2, eliminated_teams)
        weekly_lineups[2] = lineup
        for player in lineup:
            self.used_players.add(f"{player.team}_{player.name}")
        
        # Simulate eliminations: #5 HOU, #6 BUF, #3 PHI, #5 LAR
        eliminated_teams.update(['HOU', 'BUF', 'PHI', 'LAR'])
        
        # Week 3: Conference Championships
        # Remaining: DEN, NE, JAX, PIT (AFC), SEA, CHI (NFC)
        print("\n=== CONFERENCE CHAMPIONSHIPS (Week 3) ===")
        lineup = self.optimize_lineup_greedy(3, eliminated_teams)
        weekly_lineups[3] = lineup
        for player in lineup:
            self.used_players.add(f"{player.team}_{player.name}")
        
        # Simulate eliminations: #2 NE, #4 PIT, #2 CHI
        eliminated_teams.update(['NE', 'PIT', 'CHI'])
        
        # Week 4: Super Bowl
        # Remaining: DEN (AFC), SEA, JAX (one from each conference)
        # Let's say DEN vs SEA
        print("\n=== SUPER BOWL (Week 4) ===")
        lineup = self.optimize_lineup_greedy(4, eliminated_teams)
        weekly_lineups[4] = lineup
        for player in lineup:
            self.used_players.add(f"{player.team}_{player.name}")
        
        return weekly_lineups
    
    def print_lineup(self, week: int, lineup: List[Player]):
        """Print a formatted lineup"""
        print(f"\nWeek {week} Lineup:")
        print("-" * 70)
        
        total_points = 0
        positions = defaultdict(list)
        
        for player in lineup:
            pos = player.position
            if pos in ['S', 'CB', 'LB', 'DE', 'DT', 'OLB', 'ILB', 'FS', 'NT', 'DL']:
                pos = 'DEF'
            positions[pos].append(player)
            total_points += player.base_fpts
        
        # Print by position
        for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']:
            if pos in positions:
                for player in positions[pos]:
                    print(f"  {pos:3s} | {player.name:25s} | {player.team:3s} | {player.base_fpts:6.1f} pts")
        
        print("-" * 70)
        print(f"Total Projected Points: {total_points:.1f}")
        print()


def main():
    """Main function to run the optimizer"""
    print("=" * 70)
    print("PLAYOFF FANTASY FOOTBALL LINEUP OPTIMIZER")
    print("=" * 70)
    
    optimizer = PlayoffOptimizer()
    
    # Load all player data
    print("\nLoading player data...")
    optimizer.load_players()
    
    # Apply scoring adjustments
    print("Applying TE premium (1.5x PPR)...")
    optimizer.apply_te_premium()
    
    print("Weighting players by team advancement probability...")
    optimizer.weight_player_value()
    
    # Optimize lineups for all playoff weeks
    print("\nOptimizing lineups for all playoff weeks...")
    weekly_lineups = optimizer.simulate_playoffs()
    
    # Print results
    print("\n" + "=" * 70)
    print("OPTIMIZED PLAYOFF LINEUPS")
    print("=" * 70)
    
    total_all_weeks = 0
    for week in sorted(weekly_lineups.keys()):
        lineup = weekly_lineups[week]
        optimizer.print_lineup(week, lineup)
        total_all_weeks += sum(p.base_fpts for p in lineup)
    
    print("=" * 70)
    print(f"TOTAL PROJECTED POINTS ACROSS ALL WEEKS: {total_all_weeks:.1f}")
    print("=" * 70)
    
    print("\nStrategy Notes:")
    print("- Each player is used only once across all weeks")
    print("- TE scoring includes 1.5x PPR premium")
    print("- Elite players from top seeds (DEN #1, SEA #1, NE #2) conserved for later rounds")
    print("- Player values weighted by team advancement probability")
    print("- Lineup requirements: 1 QB, 2-3 RB, 2-3 WR, 1-2 TE, 0-1 K, 0-1 DEF (9 total)")


if __name__ == "__main__":
    main()
