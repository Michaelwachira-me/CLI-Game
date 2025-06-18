"""
Implement monster catching mechanics with probability based on rarity
    - it ensures rare monsters are harder to catch
    - leveling up makes it easy to catch rare monsters (reward system)
calculate_catch_rate does:
    - each species rarity begins with a base/initial catch rate.
    - based on the player's level, theres a bonus 
    - adds the bonus to the initial rate to get the final chance rate.
"""
def calculate_catch_rate(species_rarity, player_level):
    initial_catch_rates = {
        "normal": 1.0,
        "rare": 0.5,
        "Elite": 0.2,
        "godslayer": 0.05
    }
    
    # check if species_rarity is in dict
    if species_rarity in initial_catch_rates:
        initial_catch_rate = initial_catch_rates[species_rarity]
    else:
        initial_catch_rate = 0.25 #defaut if species_rarity not in dict
    
    # calculate player bonus based on level
    level_bonus = player_level/100
    
    # limit bonus to 0.2
    if level_bonus > 0.2:
        level_bonus = 0.2
    
    # aggregate to find final catch rate
    final_catch_rate = initial_catch_rate + level_bonus
    
    # Ensure no catch chance goes beyond 0.9 (there's always a fail probability)
    if final_catch_rate > 0.9:
        final_catch_rate = 0.9
    
    return final_catch_rate
    
