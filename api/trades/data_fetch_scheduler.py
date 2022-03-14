from datetime import datetime
import atexit
import requests

from apscheduler.schedulers.background import BackgroundScheduler

def run_data_processing(url):
    print(datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f") + ": processing")
    #process_leaders_data()
    requests.get(url)
    print(datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f") + ": finished")

scheduler = BackgroundScheduler()

def start_scheduler(seconds, fetch_endpoint_url):
    scheduler.add_job(func=lambda: run_data_processing(fetch_endpoint_url), trigger="interval", seconds=seconds)
    scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())