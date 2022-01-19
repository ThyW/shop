#!/bin/bash 

set -e

echo $1

build() {
    nix --experimental-features "nix-command flakes" build .#dockerImages.x86_64-linux.db.config.system.build.ociImage.stream
}

load() {
    ./result | sudo docker load
}

run() {
    echo $(sudo docker run -p 5432:5432 -v $PWD/pgsql-data:/var/lib/postgresql -d shop-db) > .id
}

kill() {
    sudo docker kill $(cat .id);
}

db-shell() {
    psql --host=localhost --port=5432 --user=shop -w
}

if [ $1 = "build" ]; then
    build;
elif [ $1 = "load" ]; then
    load;
elif [ $1 = "run" ]; then
    run;
elif [ $1 = "kill" ]; then
    kill;
elif [ $1 = "db" -a $2 = "shell" ]; then
    db-shell;
fi
