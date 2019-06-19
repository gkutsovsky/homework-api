import aiohttp
import asyncio
import urllib.parse
import json

from collections import namedtuple

Result = namedtuple('Result', 'status answer')
url = 'http://localhost:5000/api/login'

urls = login_url, *secret_urls = (urllib.parse.urlunsplit(('http', 'localhost:5000', f'api/{item}', '', ''))
                              for item in ('login', *(f'secret{i}' for i in range(1, 4))))



async def authenticate(session, url): 
  async with session.post(url, json={"username": "guest", "password": "guest"}) as resp:
      return await resp.text()

async def get(session, url, headers):
  async with session.get(url, headers=headers) as resp:
    text = await resp.text()
    return resp.status, text

async def get_headers(session):
  response = await authenticate(session, login_url)
  token = json.loads(response)
  return {'Authorization': f'Bearer {token["access_token"]}'}

async def get_response(url, session):
  headers = await get_headers(session)
  status, response = await get(session, url, headers)
  return status, json.loads(response)['answer']

async def run(urls):
  results = {}
  async with aiohttp.ClientSession() as session:
      for session, url in ((session, url) for url in urls):
        results[url] = Result(*(await get_response(url, session)))
        status, _ = results[url]
        if status == 401:
          results[url] = Result(*(await get_response(url, session)))
  return results

async def main():
  print((await run(secret_urls)))

            
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

