def calculate_stats_upon_leveling(base_stats:dict, level:int) -> dict:
    """
    what are the current stats, if given monster's base stats and level?
    - assume base_stats is {"hp":50, "attack": 15, "defence": 6}, level:2
        -game rules could mean growing stats per level with may HP +10%...     
    """
# empty dict to hold new stats
    new_stats = {}
    
# for every stat in base_stats, define growth rate(5% for hp: 2.5% for others)
    for stat_name in base_stats:
        base_value = base_stats[stat_name]
        
        if stat_name == "hp":
            growth_rate = 0.05
        else:
            growth_rate = 0.025 
         

# for each level after 1, multiply by (1+growthrate) 
        new_value = base_value #allow compunding at all levels
        
        for i in range(1, level):
            new_value = new_value * (1+growth_rate)
            
        new_stats[stat_name] = int(new_value)
    return new_stats
            
            
    
            
           
            
        