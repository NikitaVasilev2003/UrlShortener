class TestMakeShorterHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/make_shorter"

    async def test_base_scenario(self, client):
        data = {"url": "https://google.com"}
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_200_OK

    async def test_vip_scenario(self, client):
        data = {"url": "https://example.com/vip", "vip_key": "example_vip"}
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["short_url"] == url_from_suffix(data["vip_key"])
        assert "secret_key" in response_data

        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

