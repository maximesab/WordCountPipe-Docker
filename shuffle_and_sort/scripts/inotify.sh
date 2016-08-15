#! /bin/sh

mkdir -p $INPUT_DIR $TMP_OUTPUT_DIR $OUTPUT_DIR

FIFO="/scripts/inotify2.fifo"

#fUNCTIONS

on_exit() {
	kill $INOTIFY_PID
	rm $FIFO
	exit
}

on_event() {
	local date=$1
	local time=$2
	local file=$3
	python3 $MAIN_SCRIPT -i $INPUT_DIR"/"$file -o $TMP_OUTPUT_DIR && echo 'python3 launched' || echo 'cannot launch python script'
	echo "$date $time Fichier cree: $file"
}

cd $INPUT_DIR

#MAIN
if [ ! -e "$FIFO" ]
then
        mkfifo "$FIFO"
fi

inotifywait -m -r -e moved_to,create --timefmt '%Y-%m-%d %H:%M:%S' \
	--format '%T %f' $INPUT_DIR > "$FIFO" & INOTIFY_PID=$!

trap "on_exit" 2 3 15

while read date time file
do 
	on_event $date $time $file
done < "$FIFO"

on_exit

