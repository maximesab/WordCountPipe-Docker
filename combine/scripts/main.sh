#! /bin/bash
TMP_FILE=$(mktemp)
echo "source ~/.bashrc" > $TMP_FILE
echo ". /scripts/env_file" >> $TMP_FILE
echo "rm -f $TMPFILE" >> $TMP_FILE
echo "bash /scripts/inotify.sh" >> $TMP_FILE
bash --rcfile $TMP_FILE

