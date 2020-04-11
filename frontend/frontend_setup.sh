#!/bin/sh

cd frontend/ || exit
npm rebuild node-sass
npm install
#npm run serve
yarn serve --host 0.0.0.0

#yarn install
#yarn build
#yarn build --watch --mode=production
