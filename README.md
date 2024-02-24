# traveling_salesperson_in_manim

Beim Ausführen des Codes wurden die aus der requirements.txt-Datei eingesetzt.
Ein einfaches run über Python ist nicht möglich, da der Azure-Key, der zum generieren des Audios verwendet wurde, nicht mehr aktuell ist.
Bei Bedarf kann hierbei eine eigene Azure Ressource cognitive service erstellt werden und nach einfügen in der .env-Datei lässt sich das Video erneut generieren.  

Die Datei custom_graph.py enthält eine angepasste Klasse des Graphens aus der Manim library.
final_project.py enthält den Code, der das finale Video erzeugt.

# Traveling Salesperson visualized in manim
This repository contains the code necessary to generate a video using the Manim library, along with custom enhancements such as voiceovers and specialized graph animations.

## Requirements
The project dependencies are listed in the requirements.txt file. You can install them using the following command:

pip install -r requirements.txt

Please note that the project utilizes audio generation features that require an Azure Cognitive Services API key. The key used in the original project has expired, and you will need to obtain a new one to generate audio.

## Setting Up Azure Cognitive Services
1. Create a new Azure Cognitive Services resource in the Azure Portal.
2. Copy the Endpoint and Key from the resource you created.
3. Create a .env file in the root directory of this project and add the following lines, replacing YOUR_AZURE_ENDPOINT and YOUR_AZURE_KEY with your actual values:
    AZURE_ENDPOINT=YOUR_AZURE_ENDPOINT
    AZURE_KEY=YOUR_AZURE_KEY
This will allow the manim-voiceover module to generate audio using Azure's Text-to-Speech service.

## Custom Graph Class
The custom_graph.py file contains a customized graph class that extends functionalities of the default graph class provided by the Manim library. This allows for more specialized animations and interactions within the generated video.

## Generating the Video
To generate the final video, run the final_project.py script:

python final_project.py
Ensure that your environment is properly set up with all necessary dependencies and the Azure API key is correctly configured in your .env file.

## Contribution
Contributions to this project are welcome. Feel free to fork the repository, make your changes, and submit a pull request.