from datetime import datetime
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm

from njcaa.baseball.baseball_utils import get_njcaa_baseball_season


def get_njcaa_baseball_teams(season: int, division: int) -> pd.DataFrame():
    """
    Retrives a list of NJCAA baseball teams from a specific season, 
    and a specific NJCAA baseball division.

    If you want all teams, regardless of division, 
    use `get_all_njcaa_baseball_teams()` instead.

    Parameters
    ----------
    `season` (int, mandatory):
        The NJCAA baseball season you want a team list from.

    `division` (int, mandatory):
        The NJCAA baseball divison you want a team list from.

    Returns
    ----------
    A pandas DataFrame object containing every NJCAA baseball team
    in a specific season and division.
    """
    now = datetime.now()

    if season < 2013:
        raise ValueError('`season` must be greater than 2013.')
    elif season > now.year:
        raise ValueError(f'`season` must be greater than {now.year}.')

    divison_str = ""

    if division == 1:
        divison_str = "div1"
    elif division == 2:
        divison_str = "div2"
    elif division == 3:
        divison_str = "div3"
    else:
        raise ValueError('`division` must be an integer between 1 and 3.')

    row_df = pd.DataFrame()
    teams_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    print(f'Getting a list of Division {division} NJCAA Baseball teams.')
    year_str = get_njcaa_baseball_season(season)
    teams_url = f"https://njcaa.prestosports.com/sports/bsb/{year_str}/{divison_str}/teams?dec=printer-decorator&r=0&pos=h&sort="

    response = requests.get(teams_url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    teams_table = soup.find('table')
    team_rows = teams_table.find_all('tr')

    print(f'Parsing a list of Division {division} NJCAA Baseball teams.')

    for i in tqdm(range(1, len(team_rows))):
        team_row = team_rows[i].find_all('td')
        team_id = team_row[1].find('a').get('href')
        team_id = team_id.split('/')[-1]
        team_name = team_row[1].find('a').text

        row_df = pd.DataFrame(
            {
                'season': season,
                'njcaa_season': year_str,
                'division': division,
                'njcaa_division': divison_str,
                'team_id': team_id,
                'team_name': team_name
            },
            index=[0]
        )

        teams_df = pd.concat([teams_df, row_df], ignore_index=True)
        del row_df, team_id, team_name, team_row

    return teams_df


def get_all_njcaa_baseball_teams(season: int) -> pd.DataFrame():
    """
    Retrives a list of NJCAA baseball teams from a specific season.

    Parameters
    ----------
    `season` (int, mandatory):
        The NJCAA baseball season you want a team list from.

    Returns
    ----------
    A pandas DataFrame object containing every NJCAA baseball team
    in a specific NJCAA season.
    """

    teams_df = pd.DataFrame()
    division_df = pd.DataFrame()

    for i in range(1, 4):
        division_df = get_njcaa_baseball_teams(season, i)
        teams_df = pd.concat([teams_df, division_df], ignore_index=True)
        del division_df

    return teams_df


def get_njcaa_baseball_roster(season: int, division: int, team_id: str) -> pd.DataFrame():
    """
    Retrives the roster for an NJCAA Baseball team.

    Parameters
    ----------
    `season` (int, mandatory):
        The NJCAA baseball season you want 
        roster data from this team.

    `division` (int, mandatory):
        The NJCAA baseball divison this team played in.
        YOU MUST PASS IN THE CORRECT DIVISION!

        In testing, not inputting a divison lead to 
        signifigantly slower load times.

    `team_id` (str, mandatory):
        The NJCAA baseball team (id) you want roster data from.
        This is an input for a team ID, not a team name.

    Returns
    ----------
    A pandas DataFrame object containing the roster information
    of a valid NJCAA Baseball team.

    """
    now = datetime.now()
    roster_df = pd.DataFrame()
    row_df = pd.DataFrame()

    if season < 2013:
        raise ValueError('`season` must be greater than 2013.')
    elif season > now.year:
        raise ValueError(f'`season` must be greater than {now.year}.')

    divison_str = ""

    if division == 1:
        divison_str = "div1"
    elif division == 2:
        divison_str = "div2"
    elif division == 3:
        divison_str = "div3"
    else:
        raise ValueError('`division` must be an integer between 1 and 3.')

    year_str = get_njcaa_baseball_season(season)

    roster_url = f"https://njcaa.prestosports.com/sports/bsb/{year_str}/{divison_str}/teams/{team_id}?view=roster"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(roster_url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    time.sleep(1)

    with open('test.html', 'w+') as f:
        f.write(response.text)

    # try:
    table = soup.find_all('table')[1]

    # try:
    for k in tqdm(table.find_all('tr')):
        row = k.find_all('td')
        if len(row) == 0:
            pass
        else:
            player_num = row[0].text.strip()
            player_name = row[1].text.strip()
            player_position = row[2].text.strip()
            player_year = row[3].text.strip()

            player_url = "https://www.njcaa.org" + \
                str(row[1].find("a").get("href"))
            try:
                player_id = player_url.split('/')[9]
            except:
                player_id = player_url.split('/')[8]
            row_df = pd.DataFrame(
                {
                    'season': season,
                    'njcaa_season': year_str,
                    'division': division,
                    'njcaa_division': divison_str,
                    'player_id': player_id,
                    'player_num': player_num,
                    'player_name': player_name,
                    'player_position': player_position,
                    'player_year': player_year,
                    'player_url': player_url
                },
                index=[0]
            )

            del player_id, player_num, \
                player_name, player_position, \
                player_year, player_url

            roster_df = pd.concat([roster_df, row_df], ignore_index=True)
            del row_df
    # except:
    #     raise SystemError(
    #         f"Could not find a roster for the {year_str} {team_id} baseball team.")

    return roster_df
