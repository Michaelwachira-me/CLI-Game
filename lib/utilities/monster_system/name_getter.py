def get_monster_name(monster):
    """
    Returns the display name:
    - If it has 'nickname', use it.
    - Else if it has 'name', use it.
    - Else if it has 'monster_species', use species name.
    """
    if hasattr(monster, "nickname") and monster.nickname:
        return monster.nickname
    elif hasattr(monster, "name") and monster.name:
        return monster.name
    elif hasattr(monster, "monster_species") and monster.monster_species:
        return monster.monster_species.name
    return "Unknown"
