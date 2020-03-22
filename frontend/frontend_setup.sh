#!/bin/sh

cd ./frontend/ || exit
#npm install
yarn install
#yarn build
#yarn serve --host 0.0.0.0
yarn build --watch --mode=production
