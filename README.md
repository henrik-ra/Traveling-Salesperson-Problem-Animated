# Traveling Salesperson Person
This repository contains the code for generating the explanation video for the traveling salesperson problem using manim.

Contributors:
1. Ahmet Korkmaz
2. Henrik Rathai 
3. Tobias Ludwig

## Requirements
The project dependencies are listed in the requirements.txt file. You can install them using the following command:

pip install -r src/requirements.txt

Please note that the project uses audio generation features that require an Azure Cognitive Services API key. The key used in the original project is expired, so you need to get a new one to generate the video with audio.

## Setting Up Azure Cognitive Services
1. Create a new Azure Cognitive Services resource in the Azure Portal.
2. Copy the Endpoint and Key from the resource you created.
3. Create a .env file in the root directory of this project and add the following lines, replacing YOUR_SUBSCRIPTION_KEY and YOUR_SERVICE_REGION with your actual values:
    
    AZURE_SUBSCRIPTION_KEY=YOUR_SUBSCRIPTION_KEY # insert Key 1 here
    AZURE_SERVICE_REGION=YOUR_SERVICE_REGION # e.g."germanywestcentral"

This will allow the manim-voiceover module to generate audio using Azure's Text-to-Speech service.

## Custom Graph Class
The custom_graph.py file contains a customized graph class to create a similar graph structure for every graph and extends functionalities of the default graph class provided by the Manim library.

## Generating the Video
To generate the final video, run the final_project.py script:

python final_project.py

Ensure that your environment is properly set up with all necessary dependencies and the Azure API key is correctly configured in your .env file.

## Contribution
Contributions to this project are welcome. Feel free to fork the repository, make your changes, and submit a pull request.