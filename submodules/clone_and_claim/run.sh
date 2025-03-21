#!/bin/sh

set -e
DIR=$(dirname "$(readlink -f "$0")")

error() {
    msg="$1" ; shift
    echo "ERROR: $msg"
    exit 1
}

cd "$DIR/../../"

# Ensure the function is called with the candidate_repo argument
[ $# -lt 1 ] \
  && error "please, pass your public repo url as parameter. \nUsage: ./setup_repo.sh <candidate_repo>"

candidate_repo="$1" ; shift

# Ensure the candidate repository is not the placeholder string
[ "$candidate_repo" = "___YOUR_REPOSITORY_URL___" ] && error "Invalid candidate repository URL"

current_folder=$(basename "$PWD")
original_repo_name="$current_folder"


# Remove the interviewer repository structure
[ -f README.md ] && [ -f README.md.candidate ] \
  && rm README.md \
  && mv README.md.candidate README.md

[ -d .git ] \
  && rm -rf .git


# Set up the candidate repository
git init
git add .
git commit -m "project setup"
git remote add origin "$candidate_repo"

