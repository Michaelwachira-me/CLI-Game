def create_ai_opponent(difficulty_level) -> dict:
    return {
        "name": "AI player",
        "monsters": [
            {"name": "Wantam", "level": difficulty_level, "attack": 12, "defense": 9, "current_hp": 25},
            {"name": "Ontam", "level": difficulty_level, "attack": 13, "defense": 10, "current_hp": 30}
        ]
    }
