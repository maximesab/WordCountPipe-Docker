#! /bin/bash

INPUT_DIR=/$(pwd)
DIRECTORIES=$(ls -d */)
echo $DIRECTORIES
for element in $DIRECTORIES;
	do echo $element && bash $element\main.sh &
done

