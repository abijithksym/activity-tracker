#!/bin/bash

 

# git add .
# git commit -m "commitMessage"

 
# send -- "abijithksym\r"

# send -- "symptots123\r"
# git push 
#!/usr/bin/expect -f
spawn ssh aspen
git add .
git commit -m "message"
git push
expect "user name"
send "abijithksym\r"

expect "password: "
send "symptots123\r"

send "exit\r"