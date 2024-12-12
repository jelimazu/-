import requests

class RestClient:
    BASE_URL = "http://localhost:5000/api"

    @staticmethod
    def get_meetings():
        response = requests.get(f"{RestClient.BASE_URL}/meetings")
        return response.json()

    @staticmethod
    def create_meeting(data):
        response = requests.post(f"{RestClient.BASE_URL}/meetings", json=data)
        return response.json()

    @staticmethod
    def update_meeting(meeting_id, data):
        response = requests.put(f"{RestClient.BASE_URL}/meetings/{meeting_id}", json=data)
        return response.json()

    @staticmethod
    def delete_meeting(meeting_id):
        response = requests.delete(f"{RestClient.BASE_URL}/meetings/{meeting_id}")
        return response.status_code
