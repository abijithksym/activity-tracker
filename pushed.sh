
git add .
git commit -m "message1"
# if [ -n "$(git status - porcelain)" ];
# then
#  echo "IT IS CLEAN"
# else
git status
echo "Pushing data to remote server!!!"
username = "abijithksym"
password = "symptots123"
git push -u origin set-url " https://{username}:{password}@github.com/abijithksym/activity-tracker.git"
# fi