import pandas as pd
import click
import requests
import os
import urllib3

urllib3.disable_warnings()

url = f"https://{os.getenv('WEBSITE')}.leankit.com/io"
headers = {
    "Authorization": f"Bearer {os.getenv('AGILEPLACE')}",
    "Content-Type": "application/json",
}


# Replace with your AgilePlace API endpoint
@click.command()
def cards():
    api_url = f"{url}/board"
    board_details_url = f"{api_url}/2003022297"

    card = f"{board_details_url}/card"

    card_resp = requests.get(card, headers=headers, verify=False)
    if card_resp.ok:
        x = card_resp.json()['cards']
        df = pd.DataFrame.from_dict(x)
        df.to_csv("cards.csv")

    # # Make a GET request
    # response = requests.get(api_url, headers=headers)
    # resp = requests.get(board_details_url, headers=headers)
    # parent = requests.get(parent_card_url, headers=headers)
    # if parent.ok:
    #     print(json.dumps(parent.json(), indent=4))
    # if resp.ok:
    #     print(json.dumps(resp.json(), indent=4))
    #
    # if response.status_code == 200:
    #     # Request was successful
    #     data = response.json()
    #     print(json.dumps(data))
    # else:
    #     print(f"Error: {response.status_code}")


@click.command()
def boards():
    api_url = f"{url}/board"
    board_details_url = f"{api_url}/2003022297"

    board_resp = requests.get(board_details_url, headers=headers, verify=False)
    if board_resp.ok:
        x = board_resp.json()["users"]
        df = pd.DataFrame.from_dict(x)
        df.to_csv("users.csv")


if __name__ == "__main__":
    cli = click.Group()
    cli.add_command(cards)
    cli.add_command(boards)
    cli()
