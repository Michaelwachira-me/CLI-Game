# the type system defines which monster beats which
type_system = {
    "Fire": {"stronger_than": ["Air"], "weaker_than": ["Water"]},
    "Air": {"stronger_than": ["Earth"], "weaker_than": ["Fire"]},
    "Earth": {"stronger_than": ["Water"], "weaker_than": ["Air"]},
    "Water": {"stronger_than": ["Fire"], "weaker_than": ["Earth"]}
}

# Helper function to give stats on how much one type gains/losses in battle
def points_in_type_attack(attacker, defender):
    if defender in type_system[attacker]["stronger_than"]:
        return 3.0
    if defender in type_system[attacker]["weaker_than"]:
        return 1.5
    else:
        return 1.0