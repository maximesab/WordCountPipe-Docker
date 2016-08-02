#! /bin/bash

INPUT_DIR="/home/maxime/Desktop/WordCountPipe/split/outbox"
cd "/home/maxime/Desktop/WordCountPipe/map"
function block_for_change {
  inotifywait -r \
	-e moved_to,create \
	$INPUT_DIR
}

BUILD_SCRIPT=main.py   

function build {
  bash python3 main.py -i $INPUT_DIR -o "/home/maxime/Desktop/WordCountPipe/map/outbox"
}


while block_for_change; do
  build
done

docker run -dit --name map -v /home/maxime/Desktop/WordCountPipe/split/outbox:/inbox -v /outbox:/home/maxime/Desktop/WordCountPipe/map/outbox map:test 
