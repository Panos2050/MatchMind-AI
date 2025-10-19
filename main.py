import json
from transformers import pipeline
from pymongo import MongoClient
import os

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def create_match_report(match_string):
    """Create a detailed match report from the score string"""
    try:
        parts = match_string.split()
        if len(parts) >= 3:
            home_team = parts[0]
            score = parts[1]
            away_team = ' '.join(parts[2:])
            
            home_score, away_score = score.split('-')
            
            # Determine match outcome
            if home_score > away_score:
                outcome = f"{home_team} won at home"
            elif away_score > home_score:
                outcome = f"{away_team} won away"
            else:
                outcome = "the match ended in a draw"
            
            report = f"""
            Greek Super League match between {home_team} and {away_team}. 
            The final score was {home_score} to {away_score}. 
            {outcome}. Both teams displayed competitive performance throughout the game.
            This result impacts their standings in the league table.
            """
            
            return report.strip(), home_team, away_team, home_score, away_score
    except:
        report = f"Football match: {match_string}. An exciting Greek Super League encounter."
        return report, "Unknown", "Unknown", "0", "0"

def connect_to_mongodb():
    """Connect to MongoDB on external harddrive"""
    # If MongoDB is running on your external drive, use:
    # client = MongoClient('mongodb://localhost:27017/')
    
    # Or if you have a specific connection string:
    # client = MongoClient('mongodb://username:password@localhost:27017/')
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['football_analysis']
    collection = db['greek_matches']
    return collection

def save_to_mongodb(collection, summarized_matches):
    """Save all matches to MongoDB"""
    # Clear existing data (optional)
    collection.delete_many({})
    
    # Insert all matches
    result = collection.insert_many(summarized_matches)
    return len(result.inserted_ids)

# Load matches
with open("previous_matches.json", "r") as file:
    match_strings = json.load(file)

print(f"📊 Processing {len(match_strings)} matches...")
summarized_matches = []

# Connect to MongoDB
try:
    collection = connect_to_mongodb()
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    collection = None

for i, match_str in enumerate(match_strings):
    print(f"Processing match {i+1}/{len(match_strings)}: {match_str}")
    
    # Create detailed report
    report, home_team, away_team, home_score, away_score = create_match_report(match_str)
    
    # Generate summary
    try:
        summary = summarizer(report, max_length=50, min_length=20, do_sample=False)[0]['summary_text']
    except:
        summary = f"Match: {home_team} {home_score}-{away_score} {away_team}"
    
    # Create match document
    match_doc = {
        "match_id": i + 1,
        "match_string": match_str,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": int(home_score),
        "away_score": int(away_score),
        "league": "Greek Super League",
        "season": "2024-2025",
        "original_report": report,
        "ai_summary": summary,
        "timestamp": json.dumps(str(__import__('datetime').datetime.now()))
    }
    
    summarized_matches.append(match_doc)

# Save to MongoDB
if collection is not None:
    saved_count = save_to_mongodb(collection, summarized_matches)
    print(f"✅ Successfully saved {saved_count} matches to MongoDB!")
else:
    print("❌ Could not save to MongoDB")

# Also save to JSON as backup (make sure summarized_matches doesn't contain ObjectId)
json_backup_data = []
for match in summarized_matches:
    clean_match = match.copy()
    # Remove any MongoDB-specific fields
    if '_id' in clean_match:
        del clean_match['_id']
    json_backup_data.append(clean_match)

with open("summarized_football_data.json", "w") as out_file:
    json.dump(json_backup_data, out_file, indent=4, ensure_ascii=False)

print(f"📁 Backup saved to 'summarized_football_data.json'")