#!/bin/bash

#currentily this code is not workig as it should, dont run it!

echo "Running the validation script..."
./valid.sh

echo "Activating the venv"
source venv/bin/activate

echo "Running a local Redis server.."
docker run --name redis -p 6379:6379 -d redis

echo "Activating the venv"
source venv/bin/activate

echo "Runnig a local NATS server.."
gnome-terminal --tab -- bash -c "sudo docker run -d --name nats-server -p 4222:4222 nats:latest; exec bash"

echo "Activating the venv"
source venv/bin/activate

cd even-odd-project
echo "Running the server..."
gnome-terminal --tab -- bash -c "python3 server.py; exec bash"

echo "Activating the venv"
source venv/bin/activate

echo "Running services..."
gnome-terminal --tab -- bash -c "python3 even_service.py; exec bash"

source venv/bin/activate
gnome-terminal --tab -- bash -c "python3 odd_service.py; exec bash"

echo -e "Now it's time to use the client.\nTo do this, run the command 'python3 client.py -h' inside the even-odd-project!"

exit 0
