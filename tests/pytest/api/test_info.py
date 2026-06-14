from shared.models.api import InfoResponse


async def test_api_info(api_client):
    response = await api_client.get("/api/v1/info/version")
    assert response.status_code == 200
    assert InfoResponse.model_validate(response.json())
