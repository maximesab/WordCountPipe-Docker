cd /home/maxime/Desktop/WordCountPipe/split/inbox
split --lines=500000 --numeric-suffixes --suffix-length=2 test.txt ../outbox/t 
chmod -R 777 ../outbox

