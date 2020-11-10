from driver import driver
from app.models import User, Message
from flask_login import current_user, login_user, logout_user, login_required
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException as NoSuchElement
from selenium.common.exceptions import TimeoutException as Timeout
from selenium.common.exceptions import WebDriverException as DriverException


@login_required
def send(message=Message, user=User):
    receiver_list = format_number(message.receiver_list)
    message_list = []
    try:
        app1 = driver.MessageBot(driveroptions=str(user.phone_number))

        if app1.login():
            for number in receiver_list:
                try:
                    app1.hit_number(number)

                    if message.attachment is not None:
                        message_status = app1.attach(image_folder_path=message.attachment, text=message.body)

                    message = {"phone_number": number, "status": message_status}

                    message_list.append(message)

                    if message["status"] is False:
                        print('Bu mesaj {} numarasına gönderilmedi '.format(number))
                        try:
                            WebDriverWait(app1.driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')))
                        except Timeout:
                            print('İnternette problem var heralde')
                        #check if driver is still intact
                    else:
                        print('Bu mesaj {} numarasına gönderildi '.format(number))

                    WebDriverWait(app1.driver, 2).until(EC.alert_is_present())
                    app1.driver.switch_to.alert.dismiss()

                except Timeout:
                    print("Alert vermedi devamke")
    except:
        print('Driver da problem var')


def format_number(phone_number_list):
    formatted_list = []
    for phone_number in phone_number_list:
        phone_number = phone_number.replace(" ", "").replace("+", "").strip()
        if len(phone_number) == 10:
            phone_number = "90{}".format(phone_number)
        formatted_list.append(phone_number)
    return formatted_list
