#!/bin/sh
git add * 
git stash
git pull
sudo kill -9 $(sudo lsof -t -i:80)
sudo nohup python3 app.py > log.txt 2>&1 &
