import requests
import json
import os

# --- TEAM LIST ---
greek_teams = [
    "Olympiacos", "PAOK", "AEK Athens", "Panathinaikos",
    "Aris", "OFI", "Asteras Tripolis", "Volos",
    "Atromitos", "Panetolikos", "Lamia", "PAS Giannina",
    "Panserraikos"
]

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Create data/ if missing

STORAGE_FILE = os.path.join(DATA_DIR, "previous_matches.json")

# --- FUNCTIONS ---

def load_previous_matches():
    """Load previously seen matches from file"""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_current_matches(matches):
    """Save current matches to file"""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(matches), f, indent=4, ensure_ascii=False)

def get_all_matches():
    """Get all matches from TheSportsDB API"""
    all_matches = set()

    for team in greek_teams:
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchevents.php?e={team}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ Failed to fetch for {team}: {e}")
            continue

        for match in data.get('event', []):
            if match.get('intHomeScore') is not None:
                home = match['strHomeTeam']
                away = match['strAwayTeam']

                if home in greek_teams and away in greek_teams:
                    match_str = f"{home} {match['intHomeScore']}-{match['intAwayScore']} {away}"
                    all_matches.add(match_str)
    
    return all_matches

# --- MAIN EXECUTION ---

print("⚽ GREEK SUPER LEAGUE - NEW MATCHES")
print("=" * 45)

# Load previous matches
previous_matches = load_previous_matches()
print(f"📁 Previously stored matches: {len(previous_matches)}")

# Fetch from API
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

# Save current matches
save_current_matches(current_matches)
print(f"\n💾 Saved {len(current_matches)} matches for next comparison")
