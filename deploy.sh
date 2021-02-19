#!/bin/bash

echo "Server:"
echo $AWS_SERVER
echo "User:"
echo $AWS_USER
echo "Token"
echo $TOKEN

SCRIPT="cd /home/${AWS_USER}/ryan_coderbot/discord-coderbot; git pull origin main; source env/bin/activate; pip install -r requirements.txt; sudo service coderbot restart"
ssh -i "website.pem" -l ${AWS_USER}@${AWS_SERVER} "${SCRIPT}"
