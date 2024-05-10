import requests

from langchain.tools import tool


@tool
def datetime(
        timezone: str
):
    """Used to obtain date and time based on provided city and automatically found timezone"""

    url = f'http://worldtimeapi.org/api/timezone/{timezone}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        return f"Error: {response.status_code}"
    return data