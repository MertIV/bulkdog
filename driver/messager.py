from driver import webdriver
from app.models import User, Message
from flask_login import current_user, login_user, logout_user, login_required
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException as NoSuchElement
from selenium.common.exceptions import TimeoutException as Timeout
from selenium.common.exceptions import WebDriverException as DriverException
import openpyxl as excel
import time


def send(phone_number_list, attachment=None, attachment_body=None, message_body=None):

    send_list = readContacts(phone_number_list)

    app1 = webdriver.MessageBot(driveroptions='chrome-data-mert')

    app1.login()

    receiver_list = format_number(send_list)
    message_list = []
    try:
        for number in receiver_list:
            try:
                if app1.check_login():

                    app1.hit_number(number)

                    try:
                        WebDriverWait(app1.driver, 1).until(EC.alert_is_present())
                        alert = app1.driver.switch_to.alert
                        alert.accept()
                        print("alert accepted")
                    except:
                        message_status = app1.attach(image_folder_path=attachment)

                        counter = 0

                        try:
                            while app1.check_message_transmission() is False:
                                counter += 1
                            else:
                                app1.send_message(message_body)
                                #time.sleep(2)
                        except Exception as e:
                            print('Exception is : ' + str(e))

                        message = {"phone_number": number, "status": message_status}

                        message_list.append(message)

                        if message["status"] is False:
                            print('Bu mesaj {} numarasına gönderilmedi '.format(number))
                            try:
                                WebDriverWait(app1.driver, 5).until(EC.presence_of_element_located(
                                    (By.XPATH, webdriver.xpath['login'])))
                            except Timeout:
                                print('İnternette problem var heralde')
                                app1.driver.close()
                                app1 = webdriver.MessageBot()
                        else:
                            print('Bu mesaj {} numarasına gönderildi '.format(number))

                        WebDriverWait(app1.driver, 1).until(EC.alert_is_present())
                        alert = app1.driver.switch_to.alert
                        alert.accept()
                        print("alert accepted")

                WebDriverWait(app1.driver, 1).until(EC.alert_is_present())
                alert = app1.driver.switch_to.alert
                alert.accept()
                print("alert accepted")

            except Timeout:
                print("Alert vermedi devamke")

            except DriverException:
                app1.driver.close()
                app1 = webdriver.MessageBot()

        return message_list
    except Exception as e:
        print('Driver da problem var : ' + str(e))


def format_number(phone_number_list):
    formatted_list = []
    for phone_number in phone_number_list:
        phone_number = phone_number.replace(" ", "").replace("+", "").strip()
        if len(phone_number) == 10:
            phone_number = "90{}".format(phone_number)
        formatted_list.append(phone_number)
    return formatted_list


def readContacts(fileName):
    lst = []
    file = excel.load_workbook(fileName)
    sheet = file.active
    firstCol = sheet['A']
    for cell in range(len(firstCol)):
        if firstCol[cell].value is not None:
            contact = str(firstCol[cell].value)
            # contact = "\"" + contact + "\""
            lst.append(contact)
    return lst


status_list = send(phone_number_list='C:/Users/msi-/Desktop/Enterpreneur/Side Project/numbers.xlsx',
                   attachment='C:/Users/msi-/Desktop/Enterpreneur/Side Project/tom.jpeg',
                   message_body='Tomito')

print(status_list)
