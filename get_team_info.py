import requests
import json
import os

greek_teams = [
    "Olympiacos", "PAOK", "AEK Athens", "Panathinaikos",
    "Aris", "OFI", "Asteras Tripolis", "Volos",
    "Atromitos", "Panetolikos", "Lamia", "PAS Giannina",
    "Panserraikos"
]

STORAGE_FILE = "previous_matches.json"

def load_previous_matches():
    """Load previously seen matches from file"""
    if os.path.exists(STORAGE_FILE):
        with open (STORAGE_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_current_matches(matches):
    """Save current matches to file"""
    with open(STORAGE_FILE, "w") as f:
        json.dump(list(matches), f)

def get_all_matches():
    """Get all matches from API"""
    all_matches = set()

    for team in greek_teams:
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchevents.php?e={team}"
        data = requests.get(url).json()

        for match in data.get('event', []):
            if match.get('intHomeScore') is not None:
                home = match['strHomeTeam']
                away = match['strAwayTeam']

                if home in greek_teams and away in greek_teams:
                    match_str = f"{home} {match['intHomeScore']}-{match['intAwayScore']} {away}"
                    all_matches.add(match_str)
    
    return all_matches

# Main execution
print("⚽ GREEK SUPER LEAGUE - NEW MATCHES")
print("=" * 45)

# Load previous matches
previous_matches = load_previous_matches()
print(f"📁 Previously stored matches: {len(previous_matches)}")

# Get current matches from API
current_matches = get_all_matches()
print(f"🔍 Current matches from API: {len(current_matches)}")

# Find new matches
new_matches = current_matches - previous_matches

if new_matches:
    print(f"\n🎯 NEW MATCHES FOUND: {len(new_matches)}")
    for match in sorted(new_matches):
        print(f"  ⚽ {match}")
else:
    print(f"\n✅ No new matches since last check")

# Update storage with current matches
save_current_matches(current_matches)
print(f"\n💾 Saved {len(current_matches)} matches for next comparison")
