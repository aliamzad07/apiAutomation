import requests
import pytest

class TestLocationRetrieval:

    base_url = 'https://partners.api.skyscanner.net/apiservices/v3'
    valid_api_key = 'sh428739766321522266746152871799'
    invalid_locale = 'invalid_locale'
    locale = 'fr-FR'

    @pytest.fixture
    def valid_headers(self):
        return {'x-api-key': self.valid_api_key}

    @pytest.fixture
    def invalid_headers(self):
        return {'x-api-key': 'invalid_api_key'}
    # TC001
    def test_location_retrieval(self, valid_headers):
        # For send request
        url = f'{self.base_url}/geo/hierarchy/flights/{self.locale}'

        # for response
        response = requests.get(url, headers=valid_headers)

        # status code
        assert response.status_code == 200, f'Unexpected status code: {response.status_code}'

        # json parsing
        json_response = response.json()

        # check the status from response
        assert json_response.get('status') == 'RESULT_STATUS_COMPLETE'

        # Verify that the response contains accurate location data for the specified locale
        places = json_response.get('places', {})
        assert places, 'No places data in the response'

        # Iterate over each place and check the accuracy of location data
        for place_id, place_info in places.items():
            # Ensure each place has coordinates
            assert 'coordinates' in place_info, f'No coordinates for place {place_id}'

            # Verify that latitude and longitude are present
            coordinates = place_info['coordinates']
            assert 'latitude' in coordinates, f'No latitude for place {place_id}'
            assert 'longitude' in coordinates, f'No longitude for place {place_id}'

            # Example: Verify that latitude and longitude are within valid ranges
            latitude = coordinates['latitude']
            longitude = coordinates['longitude']
            assert -90 <= latitude <= 90, f'Invalid latitude for place {place_id}'
            assert -180 <= longitude <= 180, f'Invalid longitude for place {place_id}'

    ## TC005
    def test_security_aspect_invalid_api_key(self, invalid_headers):
        # for request
        url = f'{self.base_url}/geo/hierarchy/flights/{self.locale}'
        # for response
        response = requests.get(url, headers=invalid_headers)
        # response status code match
        assert response.status_code == 401, f'Unexpected status code: {response.status_code}'
        json_response = response.json()
        assert json_response.get('code') == 16, 'Unexpected error code in the response'
        assert json_response.get('message') == 'Invalid API key provided. Please provide a valid API key.', 'Unexpected error message in the response'

    ## TC009
    def test_locale_validation_invalid_locale(self, valid_headers):
        url = f'{self.base_url}/geo/hierarchy/flights/{self.invalid_locale}'
        response = requests.get(url, headers=valid_headers)
        assert response.status_code == 400, f'Unexpected status code: {response.status_code}'
        json_response = response.json()
        assert json_response.get('code') == 3, 'Unexpected error code in the response'
        assert json_response.get('message') == 'The locale is invalid', 'Unexpected error message in the response'
