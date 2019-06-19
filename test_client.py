import asyncio
import pytest

from client import secret_urls, run

@pytest.mark.asyncio
async def test_run():
  res = await run(secret_urls)
  assert b'expected result' == res