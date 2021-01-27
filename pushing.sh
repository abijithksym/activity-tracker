#!/bin/bash
git add .
git commit -m "commitMessage"
expect "Enter username\r"
 
send -- "abijithksym\r"
 
expect "Enter password\r"
 
send -- "symptots123\r"
git push 

 
