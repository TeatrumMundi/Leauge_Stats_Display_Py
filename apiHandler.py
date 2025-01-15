import requests
from configHandler import get_api_key

base_link_riot = "https://europe.api.riotgames.com"
base_link_eun1 = "https://eun1.api.riotgames.com"

def fetch_data_from_api(url):
    """
    This method performs a network request to the provided URL and handles errors that may occur during the process
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as exception:
        print(f"Network error occurred: {exception}")
        return None
    except ValueError:
        print("Error: Failed to decode JSON response")
        return None

def get_puuid(nick, tag):
    url = f"{base_link_riot}/riot/account/v1/accounts/by-riot-id/{nick}/{tag}?api_key={get_api_key()}"
    data = fetch_data_from_api(url)
    if data:
        return data.get("puuid")
    return None

def get_summoner_data(puuid, field):
    url = f"{base_link_eun1}/tft/summoner/v1/summoners/by-puuid/{puuid}?api_key={get_api_key()}"
    data = fetch_data_from_api(url)
    if data:
        return data.get(field)
    return None

def get_summoner_lvl(puuid):
    return get_summoner_data(puuid, "summonerLevel")

def get_summoner_icon(puuid):
    return get_summoner_data(puuid, "profileIconId")

def get_summoner_id(puuid):
    return get_summoner_data(puuid, "id")

def get_summoner_account_id(puuid):
    return get_summoner_data(puuid, "accountId")