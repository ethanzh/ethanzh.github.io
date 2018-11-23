python3 build.py
current_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
message="Running build on " + current_date_time
git add .
git commit -m message
git push
