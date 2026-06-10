async def test_api_ready(achat_api_client):
    response = await achat_api_client.get("info/ready")
    assert response.status_code == 200
    json_dict = response.json()
    assert json_dict["DBCheck"] is True
    assert json_dict["WorkerCheck"] is True
