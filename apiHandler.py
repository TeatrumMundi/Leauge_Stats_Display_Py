from typing import List, Optional, Dict

import requests
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from configHandler import get_api_key

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for API URLs
API_ENDPOINTS = {
    "riot_account": "https://europe.api.riotgames.com/riot/account/v1/accounts",
    "summoner": "https://eun1.api.riotgames.com/tft/summoner/v1/summoners",
    "champion-mastery-v4": "https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"
}

api_key = get_api_key()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_data_from_api(url):
    """
    Performs a network request to the provided URL and handles errors that may occur.

    Parameters:
        url (str): The API endpoint URL.

    Returns:
        dict: JSON response data or error details.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error occurred: {req_err}")
        return {"error": f"Network error: {req_err}"}
    except ValueError as json_err:
        logger.error(f"Failed to parse JSON: {json_err}")
        return {"error": "Invalid JSON response"}

def get_puuid(nick, tag):
    """
    Retrieves the PUUID for a given Riot ID.

    Parameters:
        nick (str): The Riot username.
        tag (str): The Riot tag.

    Returns:
        str: The PUUID of the user or None if the user is not found.
    """

    url = f"{API_ENDPOINTS['riot_account']}/by-riot-id/{nick}/{tag}?api_key={api_key}"
    data = fetch_data_from_api(url)
    return data.get("puuid") if data and "error" not in data else None

def get_summoner_data(puuid, field):
    """
    Retrieves specific summoner data for a given PUUID.

    Parameters:
        puuid (str): The player's PUUID.
        field (str): The specific field to retrieve.

    Returns:
        Any: The value of the requested field or None if not found.
    """
    url = f"{API_ENDPOINTS['summoner']}/by-puuid/{puuid}?api_key={api_key}"
    data = fetch_data_from_api(url)
    if data and "error" not in data:
        return data.get(field)
    else:
        logger.warning(f"Field '{field}' not found in the response.")
        return None

def get_summoner_lvl(puuid):
    """Retrieves the summoner level for a given PUUID."""
    return get_summoner_data(puuid, "summonerLevel")

def get_summoner_icon(puuid):
    """Retrieves the summoner profile icon ID for a given PUUID."""
    return get_summoner_data(puuid, "profileIconId")

def get_summoner_id(puuid):
    """Retrieves the summoner ID for a given PUUID."""
    return get_summoner_data(puuid, "id")

def get_summoner_account_id(puuid):
    """Retrieves the summoner account ID for a given PUUID."""
    return get_summoner_data(puuid, "accountId")


def build_champion_mastery_url(puuid: str, number_of_champions: int) -> str:
    """Builds the URL for retrieving champion mastery data."""
    return f"{API_ENDPOINTS['champion-mastery-v4']}{puuid}/top?count={number_of_champions}&api_key={api_key}"


def get_champion_mastery_data(puuid: str, number_of_champions: int) -> dict | None:
    """
    Fetches champion mastery data for a player.

    Args:
        puuid (str): Player's unique identifier.
        number_of_champions (int): Number of top champions to fetch.

    Returns:
        Optional[List[Dict]]: List of champion mastery data or None if an error occurs.
    """
    url = build_champion_mastery_url(puuid, number_of_champions)
    data = fetch_data_from_api(url)

    if not data or "error" in data:
        return None

    return data


def get_top_champions_by_mastery(puuid: str, number_of_champions: int) -> List[int]:
    """
    Retrieves the top champions by mastery for a player.

    Args:
        puuid (str): Player's unique identifier.
        number_of_champions (int): Number of top champions to retrieve.

    Returns:
        List[int]: List of champion IDs sorted by mastery.
    """
    data = get_champion_mastery_data(puuid, number_of_champions)
    if not data:
        return []

    return [segment.get('championId') for segment in data if 'championId' in segment]
