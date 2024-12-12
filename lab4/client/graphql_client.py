import requests
import json

class GraphQLClient:
    def __init__(self, url="http://localhost:5000/graphql"):
        self.url = url

    def query_meeting(self, meeting_id):
        query = """
        query($id: Int!) {
          meeting(id:$id) {
            id
            title
            tags {
              id
              name
            }
          }
        }
        """
        variables = {"id": meeting_id}
        response = requests.post(self.url, json={'query': query, 'variables': variables})
        return response.json()

    def add_tag(self, meeting_id, tag_name):
        mutation = """
        mutation($mid: Int!, $name: String!){
          addTagToMeeting(meetingId:$mid, name:$name) {
            success
          }
        }
        """
        variables = {"mid": meeting_id, "name": tag_name}
        response = requests.post(self.url, json={'query': mutation, 'variables': variables})
        return response.json()
