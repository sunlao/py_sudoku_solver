from shared.models.api import InfoResponse


async def test_api_info(achat_api_client):
    response = await achat_api_client.get("info/version")
    assert response.status_code == 200
    assert InfoResponse.model_validate(response.json())
