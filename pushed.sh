
git add .
git commit -m"message"
if [ -n "$(git status - porcelain)" ];
then
 git status
 echo "Pushing data to remote server!!!"
 git push -u origin
 
else
 echo "IT IS CLEAN"
fi