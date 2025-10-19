import os
import json
import requests
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

STORAGE_FILE = os.path.join(DATA_DIR, "previous_matches.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "summarized_football_data.json")

# -------------------------------
# ENVIRONMENT CONFIG
# -------------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "football_analysis")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "greek_matches")

# -------------------------------
# SETUP
# -------------------------------
greek_teams = [
    "Olympiacos", "PAOK", "AEK Athens", "Panathinaikos",
    "Aris", "OFI", "Asteras Tripolis", "Volos",
    "Atromitos", "Panetolikos", "Lamia", "PAS Giannina",
    "Panserraikos"
]

# Load summarization model
print("🧠 Loading summarization model (first time may take a while)...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# -------------------------------
# FUNCTIONS
# -------------------------------
def load_previous_matches():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_current_matches(matches):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(matches), f, indent=4, ensure_ascii=False)

def connect_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]

def get_all_matches():
    """Get all matches from API"""
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

def create_report(match_string):
    """Generate detailed text and AI summary for a match"""
    try:
        parts = match_string.split()
        home_team = parts[0]
        score = parts[1]
        away_team = ' '.join(parts[2:])
        home_score, away_score = map(int, score.split('-'))

        if home_score > away_score:
            outcome = f"{home_team} won at home"
        elif away_score > home_score:
            outcome = f"{away_team} won away"
        else:
            outcome = "the match ended in a draw"

        report = (
            f"Greek Super League match between {home_team} and {away_team}. "
            f"The final score was {home_score} to {away_score}. {outcome}. "
            "Both teams displayed competitive performances throughout the match."
        )

        summary = summarizer(report, do_sample=False, max_new_tokens=100)[0]['summary_text']
        return report, summary
    except Exception as e:
        print(f"⚠️ Summary failed for '{match_string}': {e}")
        return f"Match: {match_string}", f"Summary unavailable for {match_string}"

# -------------------------------
# MAIN EXECUTION
# -------------------------------
print("⚽ GREEK SUPER LEAGUE - NEW MATCHES")
print("=" * 60)

previous_matches = load_previous_matches()
current_matches = get_all_matches()
new_matches = current_matches - previous_matches

if not new_matches:
    print("✅ No new matches found.")
else:
    print(f"🎯 Found {len(new_matches)} new matches!\n")

    summarized_data = []
    for i, match in enumerate(sorted(new_matches), start=1):
        report, summary = create_report(match)
        print(f"{i}. {match}")
        print(f"   📝 {summary}\n")

        summarized_data.append({
            "match": match,
            "report": report,
            "summary": summary
        })

    # Save summaries as backup
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summarized_data, f, indent=4, ensure_ascii=False)
    print(f"📁 Summaries saved to '{SUMMARY_FILE}'")

    # Optional: save to MongoDB
    try:
        collection = connect_to_mongodb()
        collection.insert_many(summarized_data)
        print(f"✅ {len(summarized_data)} matches saved to MongoDB!")
    except Exception as e:
        print(f"⚠️ MongoDB save skipped: {e}")

save_current_matches(current_matches)
print("\n💾 Updated match data saved for next run.")
