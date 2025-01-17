import requests
from datetime import datetime

# API details
API_URL = "https://fortniteapi.io/v1/events/list/active?region=EU" # regions: en, fr, ar, de, es, es-419, it, ja, ko, pl, pt-br, ru, tr
API_KEY = "api key"
HEADERS = {"Authorization": API_KEY}

webhook_url = "Webhook here"

role_id = "ping id here"
role_mention = f"<@&{role_id}>"
messageaa = f"{role_mention}"

data = {
    "content": messageaa
}

response = requests.post(webhook_url, json=data)

# Check if the request was successful
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")


# Set to track notified windows
notified_windows = set()

# Discord Emojis for rank categories
rank_emojis = {
    "elite": "<:Elite:1320445236882702426>",  # elite
    "champ": "<:Champion:1320445329413247086>",  # champion
    "unreal": "<:Unreal:1320445363571785751>",  # unreal
    "pd": ["<:Platinum:1320445036294439014>",  # platinum
           "<:Diamond:1320445163973120030>"],  # diamond
    "bsg": ["<:Bronze:1320444926223192149>",  # bronze
            "<:Silver:1320444964618108949>",  # silver
            "<:Gold:1320444992166301718>"],  # gold
    "unranked": "<:Unranked:1320445396530757663>"  # unranked
}

# Notification function
def send_notification(tournament_name, start_time, poster_url, description, tournament_link, is_live, is_started, rank_emoji):

    # Use Discord's <t:timestamp:R> format for relative time if live
    formatted_time = f"<t:{int(start_time.timestamp())}:R>" if is_live else f"<t:{int(start_time.timestamp())}:d>"

    # Set the appropriate text based on whether the tournament has already started or is upcoming
    status_text = "Tournament Ends" if is_started else "Tournament Starts"

    embed = {
        "embeds": [{
            "title": tournament_name,
            "description": description,
            "color": 0x1F8A70,  # Green color
            "timestamp": start_time.isoformat(),
            "footer": {
                "text": "Don't miss it!"
            },
            "thumbnail": {
                "url": poster_url
            },
            "fields": [{
                "name": status_text,
                "value": formatted_time,
                "inline": False
            }, {
                "name": "Rank Category",
                "value": rank_emoji,
                "inline": False
            }]
        }]
    }

    try:
        response = requests.post(webhook_url, json=embed)
        response.raise_for_status()
        print(f"Notification sent for tournament '{tournament_name}'.")
    except requests.RequestException as e:
        print(f"Error sending notification for '{tournament_name}': {e}")

# Function to fetch tournaments
def fetch_tournaments():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("events", [])
    except requests.RequestException as e:
        print(f"Error fetching tournaments: {e}")
        return []

# Function to process tournaments
def process_tournaments():
    tournaments = fetch_tournaments()
    if not tournaments:
        print("No tournaments found.")
        return

    now = datetime.utcnow()
    upcoming_tournaments = []

    # Collect both live and upcoming tournaments with their windows
    for tournament in tournaments:
        windows = tournament.get("windows", [])
        tournament_name = tournament.get("name_line1", "Unknown Tournament")  # Ensure we use name_line1
        tournament_full_name = tournament_name + " " + tournament.get("name_line2", "")

        description = tournament.get("short_description", "No description available.")
        poster_url = tournament.get("poster", "")  # Get the poster URL
        tournament_link = f"https://www.epicgames.com/fortnite/competitive/{tournament.get('id')}"  # Link to the tournament page

        # Determine rank emoji based on tournament name
        rank_emoji = rank_emojis["unranked"]  # default unranked emoji
        if "elite" in tournament_name.lower():
            rank_emoji = f"{rank_emojis['elite']} {rank_emojis['champ']} {rank_emojis['unreal']}"
        elif "platinum" in tournament_name.lower() or "diamond" in tournament_name.lower():
            rank_emoji = " ".join(rank_emojis["pd"])  # platinum and diamond
        elif "bronze" in tournament_name.lower() or "silver" in tournament_name.lower() or "gold" in tournament_name.lower():
            rank_emoji = " ".join(rank_emojis["bsg"])  # bronze, silver, and gold

        for window in windows:
            window_id = window.get("windowId")
            if window_id in notified_windows:
                continue  # Skip already notified windows

            begin_time_str = window.get("beginTime")
            end_time_str = window.get("endTime")
            if begin_time_str and end_time_str:
                try:
                    begin_time = datetime.strptime(begin_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

                    # Check if tournament is live or upcoming
                    is_live = now >= begin_time and now <= end_time
                    if now <= begin_time:  # Upcoming tournaments
                        upcoming_tournaments.append((tournament_full_name, begin_time, window_id, poster_url, description, tournament_link, False, False, rank_emoji))
                    elif is_live:  # Live tournaments
                        is_started = now >= begin_time
                        upcoming_tournaments.append((tournament_full_name, end_time, window_id, poster_url, description, tournament_link, True, is_started, rank_emoji))

                except ValueError as e:
                    print(f"Error parsing time for tournament '{tournament_full_name}': {e}")

    # Sort the tournaments by their start time (earliest first)
    upcoming_tournaments.sort(key=lambda x: x[1])

    # Send notifications for the next 7 tournaments
    count = 0
    for tournament_name, begin_time, window_id, poster_url, description, tournament_link, is_live, is_started, rank_emoji in upcoming_tournaments:
        if count >= 7:
            break
        send_notification(tournament_name, begin_time, poster_url, description, tournament_link, is_live, is_started, rank_emoji)
        notified_windows.add(window_id)  # Mark as notified
        count += 1

if __name__ == "__main__":
    process_tournaments()
