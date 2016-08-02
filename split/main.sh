#! /bin/bash
INPUT_DIR="/home/maxime/Desktop/WordCountPipe/split/inbox"
cd "/home/maxime/Desktop/WordCountPipe/split"
function block_for_change {
  inotifywait -r \
	-e moved_to,create \
	$INPUT_DIR
}

BUILD_SCRIPT=split.sh    

function build {
  bash $BUILD_SCRIPT
}


while block_for_change; do
  build
done
