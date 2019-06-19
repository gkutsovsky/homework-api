import asyncio
import pytest

from client import secret_urls, run

@pytest.mark.asyncio
async def test_run():
  results = await run(secret_urls)
  for key in secret_urls:
    print(results[key])
    assert results.get(key)