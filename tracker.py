import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np

# login, is_online, and main functions remain the same
USERNAME = 'Username'
PASSWORD = 'Password'
TARGET_USERNAMES = ['taregetuser1']

online_status_history = {username: [] for username in TARGET_USERNAMES}


def generate_report():
    fig, ax = plt.subplots()

    for username, history in online_status_history.items():
        online_durations = []
        current_online_start = None
        for record in history:
            if record["online"]:
                if not current_online_start:
                    current_online_start = record["time"]
                online_durations.append(record["time"] - current_online_start)
            else:
                online_durations.append(0.2)
                current_online_start = None

        dates = [datetime.fromtimestamp(record["time"]) for record in history]
        bar_colors = ['g' if record["online"] else 'r' for record in history]

        ax.bar(dates, online_durations, width=0.01, color=bar_colors, align='center', label=username)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.set_yticks([])
    ax.legend()

    plt.title('Online Status History')
    plt.xlabel('Timestamp')
    plt.ylabel('Online Duration (green) / Offline ')

    plt.savefig('online_status_history.png', bbox_inches='tight')
    plt.show()


def login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    # Find button and click it
    button = driver.find_element("xpath",
                                 "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]")
    button.click()

    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys(username)

    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys(password)

    login_button = driver.find_element("xpath",
                                       '//*[@id="loginForm"]/div/div[3]/button/div')
    login_button.click()

    time.sleep(10)


def is_online(driver, username):

    active_status = driver.find_element('xpath',
                                        '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/a/div[1]/div/div/div[2]/div/div/div[2]/span/div/span/span'
                                        )
    print(active_status.text)

    try:
        if active_status.text == 'Active now':

            return True
        else:
            return False
    except:
        return False


def main():
    driver = webdriver.Chrome()  # Replace with the path to your chromedriver or geckodriver for Firefox

    login(driver, USERNAME, PASSWORD)
    driver.get('https://www.instagram.com/direct/inbox/')
    time.sleep(5)
    turn_on_notifications_button = driver.find_element(
        'xpath', '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
    turn_on_notifications_button.click()
    time.sleep(2)

    while True:
        print("Online users:")
        for target_username in TARGET_USERNAMES:
            online = is_online(driver, target_username)
            online_status_history[target_username].append({"time": time.time(), "online": online})
            print(online_status_history)

            if online:
                print(f"{target_username} is online.")
            else:
                print(f"{target_username} is offline.")
        print("Generating report...")
        generate_report()

        print("\nWaiting for 5 minutes before checking again...")
        time.sleep(30)

    driver.quit()


if __name__ == "__main__":
    main()
