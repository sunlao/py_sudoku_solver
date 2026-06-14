async def test_api_ready(api_client):
    response = await api_client.get("/api/v1/info/ready")
    assert response.status_code == 200
    json_dict = response.json()
    assert json_dict["API"] is True
    assert json_dict["Mailbox"] is True
    assert json_dict["Handler"] is True
