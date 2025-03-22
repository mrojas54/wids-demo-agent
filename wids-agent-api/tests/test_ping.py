import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    # Given
    # test_app

    # When
    response = await client.get("/ping")

    # Then
    assert response.status_code == 200
    assert response.json() == {"environment": "test", "ping": "pong!", "testing": True}
