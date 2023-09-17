#!/usr/bin/env python3

import pandas as pd
import click
import requests
import os
import urllib3

urllib3.disable_warnings()
#  You will need 2 environment variables set, 1 for the URL, 1 for your token
url = f"https://{os.getenv('WEBSITE')}.leankit.com/io"
headers = {
    "Authorization": f"Bearer {os.getenv('AGILEPLACE')}",
    "Content-Type": "application/json",
}
api_url = f"{url}/board"
board_details_url = f"{api_url}/2003022297"


# Replace with your AgilePlace API endpoint
@click.command()
@click.option("-o", "--out", type=str, help="Path to output file")
def cards(out="cards"):
    """Retrieves data for all cards on a Planview Board"""
    card = f"{board_details_url}/card"
    response = requests.get(card, headers=headers, verify=False)
    if response.ok:
        create_csv(response.json()["cards"], out)


@click.command()
@click.option("-o", "--out", type=str, help="Path to output file")
def users(out="users"):
    """Gets all data for board users from Agileplace Planview"""
    response = requests.get(board_details_url, headers=headers, verify=False)
    if response.ok:
        create_csv(response.json()["users"], out)
    else:
        raise Exception(f"Error status {response.status_code}, problem getting card info")


def create_csv(json_data, file_name_out):
    df = pd.DataFrame.from_dict(json_data)
    df.to_csv(f"{file_name_out}.csv")
    print(f"Writing file {file_name_out}.csv")


if __name__ == "__main__":
    cli = click.Group()
    cli.add_command(cards)
    cli.add_command(users)
    cli()
