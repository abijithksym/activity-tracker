import base64
import requests
from github import Github
from pprint import pprint
import os
username = "abijithksym"
url = f"https://api.github.com/{username}/activity-tracker.git"
g = Github()
user=g.get_user(username)
for repo in user.get_repos():
	pprint(repo)

user_data = requests.get(url).json()
print(user_data)

os.system('git init')
os.system('git add .')
os.system('git status')
os.system('git commit -m "trail"')
# os.system("./updating.sh")
# url2 = f"https://github.com/abijithksym/123.git"
os.system('git remote set-url origin '+ url)
# os.system('git remote set-url origin'+url2)
os.system('git push -u origin ')
print('\n',10*'==','completed.....',10*'==')