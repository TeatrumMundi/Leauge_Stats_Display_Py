from apiHandler import get_puuid, get_summoner_lvl, get_summoner_icon, get_summoner_id, get_summoner_account_id

if __name__ == "__main__":
    #user_nick = input("Enter your nickname: ")
    #user_tag = input("Enter your tag: ")
    user_nick = "Teatrum Mundi"
    user_tag = "GOD"

    puuid = get_puuid(user_nick, user_tag)
    summoner_lvl = str(get_summoner_lvl(puuid))
    summoner_icon = str(get_summoner_icon(puuid))
    summoner_id = str(get_summoner_id(puuid))
    get_summoner_account_id = str(get_summoner_account_id(puuid))

    if puuid is not None:
        print("Your summoner level: " + summoner_lvl)
        print("Your summoner icon: " + summoner_icon)
        print("Your summoner id: " + summoner_id)
        print("Your summoner account: " + get_summoner_account_id)
        print("Your puuid: " + puuid)