import os
import requests

SERVER_URL = "http://localhost:8080/upload"

class Model():
    def load(self):
        pass

    def predict(self, input_data):
        pass

    def upload_files_to_server():
        current_directory = os.getcwd()
        files = []
        for file_name in os.listdir(current_directory):
            file_path = os.path.join(current_directory, file_name)
            if os.path.isfile(file_path):
                files = {'file': open(file_path, 'rb')}
                response = requests.post(SERVER_URL, files=files)
                if response.status_code == 200:
                    print("Files uploaded successfully!")
                else:
                    print("Failed to upload files!")

    async def deploy():
        response = await requests.get("http://localhost:8080/deploy")
        if response.status_code == 200:
            print("Deployed successfully!")
        else:
            print("Failed to deploy!") 

Model.deploy()

