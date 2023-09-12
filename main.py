import asyncio
import aiohttp
from tqdm import tqdm
from colorama import init, Fore

# Initialize colorama for ANSI color support on Windows
init(autoreset=True)

async def fetch_joke(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data.get('value', 'No joke found')

async def main():
    urls = ['https://api.chucknorris.io/jokes/random'] * 10000  # Example: Fetch the URL 10 times

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_joke(session, url) for url in urls]

        num_tasks = len(tasks)
        color_changes = [0.2, 0.4, 0.6, 0.8]  # Completion percentages to change colors

        with tqdm(total=num_tasks, unit="jokes", ncols=100) as pbar:
            for i, task in enumerate(asyncio.as_completed(tasks), start=1):
                joke = await task
                pbar.update(1)

                # Calculate current completion percentage
                completion_percentage = i / num_tasks

                # Change color based on completion percentage
                if completion_percentage >= color_changes[3]:
                    color = Fore.GREEN
                elif completion_percentage >= color_changes[2]:
                    color = Fore.YELLOW
                elif completion_percentage >= color_changes[1]:
                    color = Fore.RED
                elif completion_percentage >= color_changes[0]:
                    color = Fore.MAGENTA
                else:
                    color = Fore.BLUE

                pbar.set_description(color + f"Progress: {completion_percentage * 100:.1f}%")

                # print(color + f"Chuck Norris Joke: {joke}")

if __name__ == "__main__":
    asyncio.run(main())
