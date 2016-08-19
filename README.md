it's a word count example using docker engine and docker compose to appply a map reduce and scale up the application

REQUIERMENTS

try to use docker engine 1.12 and docker-compose > 1.8 It need to be able to use the version 2 of the compose yml file.

HOW TO SET IT UP

create the following directoy : '/WordCountPipe' 

OR
ajust the volumes in the compose file to match the directory of the project (we will call it $DIRECTORY) CD into this directory,
run docker-compose create, docker-compose -d start (root needed to run docker/docker-compose) f

or each manager step run : CD $DIRECTORY/master_step_X in this directory edit the Dockerfile HOST_NAME (user name) and PASSWORD 
to match the one of the HOST machine NB : the user need to have access to docker and docker-compose command (usualy it's root access) 
THEN RUN : docker build -t manager_step_x:latest . 
docker run -dit --name manager_step_x -v $DIRECTORY/$(name of the step input volume, see docker-compose.yml)\ 
/outbox:/watched_dir manager_step_x -exec ['python3', '/scripts/manager.py']

exemple : 
docker run -dit --name manager_step_1 -v /home/maxime/Desktop/WordCountPipe/split/outbox/:watched_dir
to start of the process: drag a big text file into /split/inbox and run cd $DIRECTORY/split && ./split.sh

TODO: REDUCE STEP manager reduce step.
