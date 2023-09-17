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
        create_csv(card_resp, "cards")


def create_csv(card_resp, name):
    x = card_resp.json()[name]
    df = pd.DataFrame.from_dict(x)
    df.to_csv(f"{name}.csv")
    print(f"Writing file {name}.csv")


@click.command()
def boards():
    api_url = f"{url}/board"
    board_details_url = f"{api_url}/2003022297"
    board_resp = requests.get(board_details_url, headers=headers, verify=False)
    if board_resp.ok:
        create_csv(board_resp, "users")


if __name__ == "__main__":
    cli = click.Group()
    cli.add_command(cards)
    cli.add_command(boards)
    cli()
