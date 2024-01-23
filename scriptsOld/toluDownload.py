import requests
import json
gseIdList = ["gse103852"]
for gse in gseIdList:
    url = f'https://pephub-api.databio.org/api/v1/projects/geo/{gse}?tag=default'

    # Make a GET request to the URL
    response = requests.get(url)
    print(response.text)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content to a file
        with open("downloaded_data.json", "w") as file:
            file.write(response.text)
        print("Data downloaded successfully.")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")

with open("downloaded_data.json", "r") as readFile:
    dictionarySpecialty = json.loads(readFile.read())
    # print(dictionarySpecialty["items"])