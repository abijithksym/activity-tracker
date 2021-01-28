#! /bin/bash
DIRECTORY_TO_OBSERVE="/home/symptots/Desktop/git_upload/activity-tracker"
function block_for_change {
  inotifywait -r \
    -e 'modify,move,create,delete' --exclude '(/4913|.swx|.swp)$' \
    $DIRECTORY_TO_OBSERVE
}


while block_for_change; do
git add --all
git rm $(git ls-files --deleted)
git commit -m 'Update -  $(date)'
git push -u origin master
expect "Username:"
send "TestUsernme\r\n"
expect "Password:"
send "TestPassword\r\n"
done
