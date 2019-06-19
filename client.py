import aiohttp
import asyncio
import urllib.parse
import json


url = 'http://localhost:5000/api/login'

urls = login_url, *secrets = (urllib.parse.urlunsplit(('http', 'localhost:5000', f'api/{item}', '', ''))
                              for item in ('login', *(f'secret{i}' for i in range(1, 4))))



async def authenticate(session, url): 
  async with session.post(url, json={"username": "guest", "password": "guest"}) as resp:
      print(resp.status)
      return await resp.text()

async def get(session, url, headers):
  async with session.get(url, headers=headers) as resp:
    print('get', resp.status)
    text = await resp.text()
    return resp.status, text

    return 

async def get_headers(session):
  response = await authenticate(session, login_url)
  token = json.loads(response)
  return {'Authorization': f'Bearer {token["access_token"]}'}

async def main():
  async with aiohttp.ClientSession() as session:
      headers = await get_headers(session)
      # need headers Authorization: Bearer <access_token_value>
      for session, url in ((session, url) for url in secrets):
            status, response = await get(session, url, headers)
            if status == 401:
              headers = await get_headers(session)
              status, response = await get(session, url, headers)
            print(status, response)
            
  


if __name__ == "__main__":

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())

