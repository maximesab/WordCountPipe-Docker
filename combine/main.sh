#! /bin/bash

INPUT_DIR="/home/maxime/Desktop/WordCountPipe/map/outbox/processed"
cd "/home/maxime/Desktop/WordCountPipe/combine"
function block_for_change {
  inotifywait -r \
	-e moved_to,create \
	$INPUT_DIR
}

BUILD_SCRIPT=main.py   

function build {
  bash python3 $BUILD_SCRIPT -i $INPUT_DIR -o "/home/maxime/Desktop/WordCountPipe/combine/outbox"
}


while block_for_change; do
  build
done
