import aiohttp
import asyncio
import urllib.parse


url = 'http://localhost:5000/api/login'

urls = login_url, *secrets = (urllib.parse.urlunsplit(('http', 'localhost:5000', f'api/{item}', '', ''))
                              for item in ('login', *(f'secret{i}' for i in range(1, 4))))



async def authenticate(session, url): 
  async with session.post(url, json={"username": "guest", "password": "guest"}) as resp:
      print(resp.status)
      return await resp.text()

async def main():
  async with aiohttp.ClientSession() as session:
      token = await authenticate(session, login_url)
  print(token)


if __name__ == "__main__":

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())

