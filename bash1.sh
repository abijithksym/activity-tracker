#! /bin/bash
DIRECTORY_TO_OBSERVE="/home/symptots/Desktop/git_upload/activity-tracker"
function block_for_change {
  inotifywait -r \
    -e 'modify,move,create,delete' --exclude '(/4913|.swx|.swp)$' \
    $DIRECTORY_TO_OBSERVE
}

git add --all
git rm $(git ls-files --deleted)
git commit -m 'Update -  $(date)'
git push -u origin master
# Keeping the 'expect' code with '-c' flag