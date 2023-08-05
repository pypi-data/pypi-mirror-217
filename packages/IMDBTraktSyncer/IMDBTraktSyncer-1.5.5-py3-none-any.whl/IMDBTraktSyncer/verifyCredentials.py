import os
import json
import datetime
try:
    from IMDBTraktSyncer import authTrakt
    from IMDBTraktSyncer import errorLogger as EL
except ImportError:
    import authTrakt
    import errorLogger as EL

def prompt_get_credentials():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Old version support (v1.0.6 and below). Convert old credentials.txt format to json
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
        if lines[0].startswith("trakt_client_id="):
            values = {}
            for line in lines:
                key, value = line.strip().split("=")
                values[key] = value
            with open(file_path, 'w', encoding='utf-8') as txt_file:
                json.dump(values, txt_file)
            print("Warning: You are using a depreciated credentials.txt file.\nConversion successful: credentials.txt file converted to the new JSON format.")

    # Check if the file exists
    if not os.path.isfile(file_path):
        # If the file does not exist, create it with default values
        default_values = {
            "trakt_client_id": "empty",
            "trakt_client_secret": "empty",
            "trakt_access_token": "empty",
            "imdb_username": "empty",
            "imdb_password": "empty"
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_values, f)

    # Load the values from the file
    with open(file_path, 'r', encoding='utf-8') as f:
        values = json.load(f)

    # Check if any of the values are "empty" and prompt the user to enter them
    for key in values.keys():
        if values[key] == "empty" and key != "trakt_access_token":
            values[key] = input(f"Please enter a value for {key}: ").strip()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(values, f)

    # Get the trakt_access_token value if it exists, or run the authTrakt.py function to get it
    trakt_access_token = None
    if "trakt_access_token" in values and values["trakt_access_token"] != "empty":
        trakt_access_token = values["trakt_access_token"]
    else:
        client_id = values["trakt_client_id"]
        client_secret = values["trakt_client_secret"]
        trakt_access_token = authTrakt.authenticate(client_id, client_secret)
        values["trakt_access_token"] = trakt_access_token
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(values, f)

    trakt_client_id = values["trakt_client_id"]
    trakt_client_secret = values["trakt_client_secret"]
    trakt_access_token = values["trakt_access_token"]
    imdb_username = values["imdb_username"]
    imdb_password = values["imdb_password"]
    
    return trakt_client_id, trakt_client_secret, trakt_access_token, imdb_username, imdb_password

def prompt_sync_ratings():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Check if credentials file exists
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            sync_ratings_value = credentials.get('sync_ratings')
            if sync_ratings_value is not None:
                return sync_ratings_value
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    while True:
        # Prompt the user for input
        print("Do you want to sync ratings? (y/n)")
        user_input = input("Enter your choice: ")

        # Validate user input
        if user_input.lower() == 'y':
            sync_ratings_value = True
            break
        elif user_input.lower() == 'n':
            sync_ratings_value = False
            break
        else:
            # Invalid input, ask again
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update the value in the JSON file
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    credentials['sync_ratings'] = sync_ratings_value

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(credentials, file)

    # return true or false
    return sync_ratings_value

def prompt_sync_watchlist():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Check if credentials file exists
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            sync_watchlist_value = credentials.get('sync_watchlist')
            if sync_watchlist_value is not None:
                return sync_watchlist_value
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    while True:
        # Prompt the user for input
        print("Do you want to sync watchlists? (y/n)")
        user_input = input("Enter your choice: ")

        # Validate user input
        if user_input.lower() == 'y':
            sync_watchlist_value = True
            break
        elif user_input.lower() == 'n':
            sync_watchlist_value = False
            break
        else:
            # Invalid input, ask again
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update the value in the JSON file
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    credentials['sync_watchlist'] = sync_watchlist_value

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(credentials, file)

    # return true or false
    return sync_watchlist_value

# Last run function, used to determine when the last time IMDB reviews were submitted    
def check_imdb_reviews_last_submitted():
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')
    
    # Load credentials from credentials.txt
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    else:
        credentials = {}

    imdb_reviews_last_submitted_date_str = credentials.get('imdb_reviews_last_submitted_date')

    # If imdb_reviews_last_submitted_date is not available or not in the correct format, consider it as 10 days ago
    imdb_reviews_last_submitted_date = datetime.datetime.strptime(imdb_reviews_last_submitted_date_str, '%Y-%m-%d %H:%M:%S') if imdb_reviews_last_submitted_date_str else datetime.datetime.now() - datetime.timedelta(hours=240)

    # Check if 240 hours have passed since the last run
    if datetime.datetime.now() - imdb_reviews_last_submitted_date >= datetime.timedelta(hours=240):
        # Update the imdb_reviews_last_submitted_date with the current time
        credentials['imdb_reviews_last_submitted_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save updated credentials to credentials.txt
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(credentials, file)

        return True
    else:
        return False
        
def prompt_sync_reviews():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Check if credentials file exists
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            sync_reviews_value = credentials.get('sync_reviews')
            if sync_reviews_value is not None:
                return sync_reviews_value
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    while True:
        # Prompt the user for input
        print("Ratings are synced by default. Please note: comments synced to IMDB will use \"My Review\" as the title field.")
        print("Do you want to sync comments? (y/n)")
        user_input = input("Enter your choice: ")

        # Validate user input
        if user_input.lower() == 'y':
            sync_reviews_value = True
            break
        elif user_input.lower() == 'n':
            sync_reviews_value = False
            break
        else:
            # Invalid input, ask again
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update the value in the JSON file
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    credentials['sync_reviews'] = sync_reviews_value

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(credentials, file)

    # return true or false
    return sync_reviews_value

def prompt_remove_watched_from_watchlists():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Check if credentials file exists
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            remove_watched_from_watchlists_value = credentials.get('remove_watched_from_watchlists')
            if remove_watched_from_watchlists_value is not None:
                return remove_watched_from_watchlists_value
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    while True:
        # Prompt the user for input
        print("Movies and Episodes are removed from watchlists after 1 play.")
        print("Shows are removed when atleast 80% of the episodes are watched AND the series is marked as ended or cancelled.")
        print("Do you want to remove watched items watchlists? (y/n)")
        user_input = input("Enter your choice: ")

        # Validate user input
        if user_input.lower() == 'y':
            remove_watched_from_watchlists_value = True
            break
        elif user_input.lower() == 'n':
            remove_watched_from_watchlists_value = False
            break
        else:
            # Invalid input, ask again
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update the value in the JSON file
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        error_message = "File not found error"
        EL.logger.error(error_message, exc_info=True)
        pass

    credentials['remove_watched_from_watchlists'] = remove_watched_from_watchlists_value

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(credentials, file)

    # return true or false
    return remove_watched_from_watchlists_value

# Save the credential values as variables
trakt_client_id, trakt_client_secret, trakt_access_token, imdb_username, imdb_password = prompt_get_credentials()
sync_watchlist_value = prompt_sync_watchlist()
sync_ratings_value = prompt_sync_ratings()
remove_watched_from_watchlists_value = prompt_remove_watched_from_watchlists()
sync_reviews_value = prompt_sync_reviews()