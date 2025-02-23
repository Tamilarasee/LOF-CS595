import requests

BASE_URL = "http://localhost:8000/api"


class CCDServices:

    def register_patient(self, patient_info):
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(BASE_URL + '/patient/registration/', json=patient_info, headers=headers)
        print("Patient registration status code : ", response.status_code, response.text)
        return response.json()

    def get_auth_token(self):
        headers = {
            "Content-Type": "application/json"
        }
        user_creds = {
            "username": "demo",
            "password": "demo@1234"
        }

        response = requests.post(BASE_URL + '/auth-token/', json=user_creds, headers=headers)
        return response.json()['token']

    def delete_patient(self, patient_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + self.get_auth_token()
        }

        response = requests.delete(BASE_URL + '/patient-app/delete/?patient_id=' + patient_id, headers=headers)

        print("Patient Deleted. Status Code:", response.status_code)
