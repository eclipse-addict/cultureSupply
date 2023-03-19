from datetime import date

def crontab_job():
    now = date.now()
    print('#' *30)
    print("[TEST_Cron Schedule] I'm running every minute Current time : ", now.strftime("%Y-%m-%d %H:%M:%S"))
    print('#' *30)