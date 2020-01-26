#!/bin/bash

echo "VERSION=$(cat VERSION)"
echo "CHANGELOG=$(cat CHANGELOG)"

cd ~/project
echo "CURRENT_PATH=$(pwd)"

ls -la

echo 'Creating git tag...'
git tag $(cat VERSION) -m "$(cat CHANGELOG)"
git push origin $(cat VERSION)
echo 'FINISHED! o/'
