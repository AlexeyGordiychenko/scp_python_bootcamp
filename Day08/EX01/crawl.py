import aiohttp
import asyncio
import sys

URL = 'http://localhost:8888/api/v1/tasks/'


async def main(urls):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL, json={"urls": urls}) as response:
                response.raise_for_status()
                task = await response.json()
        except aiohttp.ClientError as e:
            print(f"Error sending POST to the server: {str(e)}")
            return
        i = 0
        dots = ['.  ', '.. ', '...']  # dots indicating progress
        delay = max(0.5, min(len(urls)/100, 2))  # delay min 0.5, max 2 seconds
        while True:
            try:
                async with session.get(f'{URL}{task["id"]}') as response:
                    data = await response.json()
            except aiohttp.ClientError:
                print(f"Can't get tasks results")
                break
            if data.get("status", "ready") == "ready":
                print('\rResults:   ')
                for url, status in data.get("result", {}).items():
                    print(f"{status}\t{url}")
                break
            print('Checking' + dots[i % 3], end='\r')
            i += 1
            await asyncio.sleep(delay)

if __name__ == '__main__':
    urls = sys.argv[1:]
    if urls:
        asyncio.run(main(urls))
