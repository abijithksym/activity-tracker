
git add .
git commit -m "message1"
# if [ -n "$(git status - porcelain)" ];
# then
#  echo "IT IS CLEAN"
# else
git status
echo "Pushing data to remote server!!!"
git push -f set-url "https://github.com/abijithksym/activity-tracker.git" origin
# fi