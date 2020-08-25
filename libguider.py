import argparse
import aiohttp
import asyncio
import async_timeout
import backoff
import json
from os import mkdir, path
from random import randint
import time
import urllib


parser = argparse.ArgumentParser()
parser.add_argument("--site_id", help="Libguides Site ID")
parser.add_argument("--api_key", help="Libguides API key")
parser.add_argument("--guide_status", help="Libguides statuses to include. ex. 1 or 1,2", 
  default="1")
args = parser.parse_args()

site_id = args.site_id
lg_api_key = args.api_key
status = args.guide_status

@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60)
async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def lg_pages_fetch(guide, session, semaphore):
    await semaphore.acquire()
    try:
        for page in guide["pages"]:
            guide_path = f"./data/{guide['id']}"
            if not path.exists(guide_path):
                try:
                    mkdir(guide_path)
                except FileExistsError:
                    pass
            with open(f"{guide_path}/guide.json", "w") as guide_json:
                guide_json.write(json.dumps(guide))
            filename = f"{guide_path}/page-{page['id']}.html"
            if not path.exists(filename):
                html = await fetch(session, page["url"])
                with open(filename, "w") as f:
                    f.write(html)
    finally:
        semaphore.release()

async def main():

    before = time.time()

    semaphore = asyncio.Semaphore(15)
    with urllib.request.urlopen(f"https://lgapi-us.libapps.com/1.1/guides?site_id={site_id}&key={lg_api_key}&status={status}&expand=owner,subjects,pages") as r:
       lgb = json.loads(r.read().decode('utf-8'))
       async with aiohttp.ClientSession() as session:
           await asyncio.gather(*[lg_pages_fetch(guide, session, semaphore) for guide in lgb])
    
    print(f"Operation took {time.time() - before} seconds")

asyncio.run(main())

# egrep -oh 'libproxy\.temple\.edu\/[a-zA-Z0-9&?:/\.=-]*' * | grep -v public | sort | uniq -c | sort -n