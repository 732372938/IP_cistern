apt install git
git init
git reset --hard
git pull https://github.com/XgzK/IP_cistern.git main
ps -ef|grep ip.py |grep -v grep|awk '{print $2}'|xargs kill -9
python3 ip.py