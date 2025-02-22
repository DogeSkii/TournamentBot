# Tournament Bot

Tournament Bot is a Python script that fetches Fortnite tournament data and sends notifications to a Discord webhook. The script uses the Fortnite API to get tournament details and sends notifications to a specified Discord channel.

## Features

- Fetches tournament data from the Fortnite API.
- Sends notifications to a Discord webhook.
- Supports different rank categories with custom emojis.
- Logs the script execution duration to a log webhook.

## Requirements

- Python 3.6+
- `requests` library
- `python-dotenv` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/tournament-bot.git
    cd tournament-bot
    ```

2. Install the required libraries:

    ```sh
    pip install requests python-dotenv
    ```

3. Create a `.env` file in the project directory and add your API key and webhook URLs:

    ```env
    API_KEY=your_api_key_here
    MAIN-HOOK=your_main_webhook_url
    TEST-HOOK=your_test_webhook_url
    LOG-HOOK=your_log_webhook_url
    ```

## Usage

1. Set the TESTMODE variable in TournBot.py to `True` or `False` depending on whether you want to use the test webhook or the main webhook.

2. Run the script:

    ```sh
    python TournBot.py
    ```

## Configuration

- TESTMODE: Set to `True` to use the test webhook, or `False` to use the main webhook.
- API_URL: The URL of the Fortnite API endpoint.
- HEADERS: The headers for the API request, including the API key.
- webhook_url, testhook, loghook: The URLs of the Discord webhooks for notifications and logging.
- role_id: The ID of the Discord role to mention in notifications.
- rank_emojis: A dictionary of custom emojis for different rank categories.

## License
 TournamentBot © 2025 by DogeSkii is licensed under CC BY-NC-SA 4.0 

