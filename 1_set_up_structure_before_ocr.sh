#!/bin/sh

set -e

echo 'Setting up git'
cp gitignore ../.gitignore

cd ..

git init --initial-branch=main

read -p "Enter fullname: " fullname
read -p "Enter user: " user

git config user.email "$fullname"
git config user.name "$user"

echo 'Setting up folders ...'

mkdir "1. source"
mkdir "2. ocr"
mkdir -p "3. text review/ghost"
mkdir -p "4. outputs/Pandoc"
mkdir -p "4. outputs/LaTex"
mkdir -p "4. outputs/html"
mkdir "5. prepress"

git add *
git commit -m "Initial setup"
