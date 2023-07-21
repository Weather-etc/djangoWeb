# K-G Robot of agriculture
This project consists a chat robot based on knowledge graph. This robot is mainly about agriculture, but it's ok
to freely chat with it thanks to open source language models.

## Prepare
### Environment requirements
To run this project locally, we provide a list of necessary tools which we used to develop this project.

1. Database:
   neo4j version 5.9.0
   MySQL version 8.0.33
2. Compiler:
   Python 3.8
3. Broswer:
   Chrome
   
### Python environment setup
To setup Python environment, cd to main directory and execute:

pip install -r requirements.txt

## Execute the project
### Build Database:
   
### execute in broswer
To execute it, cd to main directory and execute commands blow in CMD:

python .\manage.py makemigrations
python .\manage.py migrate
python .\manage.py runserver

See webpages at URL: http://127.0.0.1:8000
