from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_summary(client: AsyncClient):
    response = await client.post("/summaries", json={"url": "https://foo.bar"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["url"] == "https://foo.bar"
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_create_summary_invalid_json(client: AsyncClient):
    response = await client.post("/summaries/", json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }


@pytest.mark.asyncio
async def test_read_summary(client: AsyncClient):
    response = await client.post("/summaries", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = await client.get(f"/summaries/{summary_id}")
    assert response.status_code == HTTPStatus.OK

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


@pytest.mark.asyncio
async def test_read_summary_incorrect_id(client: AsyncClient):
    response = await client.get("/summaries/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


@pytest.mark.asyncio
async def test_read_all_summaries(client: AsyncClient):
    response = await client.post("/summaries", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = await client.get("/summaries")
    assert response.status_code == HTTPStatus.OK

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
