
git add .
git commit -m "message1"
# if [ -n "$(git status - porcelain)" ];
# then
#  echo "IT IS CLEAN"
# else
git status
echo "Pushing data to remote server!!!"
git push -u origin set-url "https://abijithksym@github.com"
# fi