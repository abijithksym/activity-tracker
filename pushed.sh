#!/usr/bin/expect -f
 
set timeout -1
spawn git add .
spawn git commit -m "fargg"
spawn git push
spawn ./pushing.sh
 
expect "Enter  username\r"
 
send -- "abijithksym\r"
 
expect "Enter password\r"
 
send -- "symptots123\r"
 
expect eof
