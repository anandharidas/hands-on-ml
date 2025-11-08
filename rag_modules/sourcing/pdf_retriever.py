import os
import requests

pdf_path = "datasets/nutrition/human-nutrition-text.pdf"

if not os.path.exists(pdf_path):
    print("File does not exist... downloading...")
    
    #url of the PDF you want to download
    url = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"
    
    #The local filename to save the downloaded file
    filename = pdf_path
    
    #Send a GET request to the URL
    response = requests.get(url)
    
    #Check if the request was suceessfull
    if response.status_code == 200:
        #Open a file in binary write mode and save the content to it
        with open(filename,"wb") as file:
            file.write(response.content)
        print(f"File downloaded and saved to {filename}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
else:
    print(f"File already exists at {pdf_path}")
    
    