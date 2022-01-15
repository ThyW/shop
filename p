#!/bin/bash 

set -e

echo $1

build() {
    nix --experimental-features "nix-command flakes" build .#dockerImages.x86_64-linux.db.config.system.build.ociImage.stream
}

load() {
    ./result | docker load
}

run() {
    docker run -p 5432:5432 -v $PWD/pgsql-data:/var/lib/postgresql -d shop-db
}

if [ $1 = "build" ]; then
    build;
elif [ $1 = "load" ]; then
    load;
elif [ $1 = "run" ]; then
    run;
fi
