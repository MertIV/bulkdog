from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NoSuchElement
from selenium.common.exceptions import TimeoutException as Timeout
from selenium.common.exceptions import WebDriverException as DriverException
import sys, time, typing
from collections import defaultdict

import glob, os


class MessageBot:
    OVERFLOW_CNT = 3
    OVERFLOW_LIMIT = 10

    def __init__(self, driveroptions='chrome-data-mert'):
        self.options = Options()
        # self.options.add_argument("--user-data-dir=C:/Users/msi-/AppData/Local/Google/Chrome/User Data/Default")
        # self.options.add_argument('--profile-directory=Default')

        self.options.add_argument("--user-data-dir=chrome-data-mert")

        self.driver = webdriver.Chrome('C:/Users/msi-/Desktop/Enterpreneur/Side Project/chromedriver.exe',
                                       options=self.options)

        # self.driver.maximize_window()

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            # wait.until(lambda driver: self.driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            print(e)
            pass

    def login(self):
        try:
            el1 = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, xpath['login'])))
            el1.get_attribute("title")
            return True
        except Timeout:
            self.driver.get('https://web.whatsapp.com/')
            try:
                el2 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, xpath['login'])))
                print(el2.get_attribute("title"))
                return True
            except Timeout:
                self.login()
            except Exception as e:
                print('Başka bir şey yanlış : ' + e)
                return False

    def check_login(self):
        try:
            el = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, xpath['login'])))
            print(el.get_attribute("title"))
            return True
        except Timeout:
            self.login()

    def hit_number(self, phone_number):
        try:
            self.driver.get('https://web.whatsapp.com/send?phone={}'.format(phone_number))

            el2 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, xpath['hit_number'])))

            print(el2.text)
        except Timeout:
            print('Elemanı bulamıyor')
        except Exception as e:
            print(e)

    def send_message(self, message):
        try:
            message_box = self.driver.find_element_by_xpath(xpath['message_box'])
            message_box.send_keys(message)

            send_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, xpath['message_send_button'])))

            send_button.click()

            status = WebDriverWait(self.driver, 15).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "tSmQ1"), message))

            print(str(status) + " : Message sent")
            return status
        except Timeout:
            print("Timeout oldu ağa yok yani bu element")
            self.login()
            return False
        except Exception as e:
            print(e)
            self.login()
            return False

    def new_chat(self, user_name):
        new_chat = self.driver.find_element_by_xpath('//div[@class="_3qx7_"]')
        new_chat.click()

        new_user = self.driver.find_element_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')
        new_user.send_keys(user_name)

        try:
            select_receiver = self.driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
            select_receiver.click()
        except NoSuchElement:
            print('There is no "{}" in contact list'.format(user_name))
        except Exception as e:
            self.driver.close()
            print(e)
            sys.exit()

    def attach(self, image_folder_path="images", text=None):
        try:
            attach = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, xpath['attach_image'])))
            attach.click()

            self.driver.find_element_by_xpath(xpath['attach_input']). \
                send_keys(image_folder_path)

            if text is not None:
                textbox = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, xpath['attach_text_box'])))
                textbox.send_keys(text)

            image = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(
                (By.XPATH, xpath['attach_loaded'])))
            loaded = image.get_attribute("data-animate-attach-media")
            print(loaded)

            if loaded:
                button = self.driver.find_element_by_xpath(
                    xpath['attach_send_button'])
                button.click()

            return True

        except Timeout and NoSuchElement:
            print('Sayfa yüklenmemiş ona göre aksiyon al')

            return False

    def get_last_message_data(self):
        try:
            upper_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     css_selector['message_list_tab'])))

            upper_list_child = upper_list[-1].find_elements_by_css_selector("*")

            send_time = upper_list_child[0].text

            status = upper_list_child[2].get_attribute("data-testid")

            # status_list = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_all_elements_located((By.CSS_SELECTOR,
            #                                          css_selector['message_status'])))
            #
            # status_2 = status_list[-1].get_attribute("data-testid")

            last_message = {
                    'send_time': '00:00',
                    'status': 'msg-notchckd'
                }
            if status is not None and send_time is not None:
                last_message: typing.Dict[str, str] = {
                    'send_time': send_time,
                    'status': status
                }
                return last_message
            else:
                return last_message

        except Exception as e:
            print('Olmadı kanka : ' + str(e))

    def check_message_transmission(self):
        try:
            now = time.time()
            now_minus = now - 60

            current_time = time.strftime("%H:%M", time.localtime(now))
            current_time_minus = time.strftime("%H:%M", time.localtime(now_minus))

            last_message = self.get_last_message_data()
            print(last_message)

            last_message_time = last_message.get('send_time')
            last_message_status = last_message.get('status')

            if (last_message_time == current_time or last_message_time == current_time_minus) and \
                    (last_message_status == 'msg-dblcheck' or last_message_status == 'msg-check'):
                return True
            else:
                return False

        except Exception as e:
            print('Hatayı bas loga : ' + str(e))

    def format_number(self, phone_number):
        phone_number = phone_number.replace(" ", "").replace("+", "").strip()
        if len(phone_number) == 10:
            phone_number = "90{}".format(phone_number)
        return phone_number

    # def __del__(self):
    #     print("Shutting down chrome")
    #     self.driver.close()


class Task(object):
    def __init__(self, user, template, attachment, body, receiver_list):
        self.template = template
        self.user = user
        self.attachment = attachment
        self.body = body
        self.receiver_list = receiver_list

xpath = {
    'login': '//*[@id="side"]/header/div[2]/div/span/div[2]/div',
    'hit_number': '//*[@id="main"]/header/div[2]/div/div/span',
    'message_box': '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',
    'message_send_button': '//*[@id="main"]/footer/div[1]/div[3]/button',
    'message_tab_class': 'tSmQ1',
    'attach_image': '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span',
    'attach_input': '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input',
    'attach_text_box': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]',
    'attach_loaded': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[1]',
    'attach_send_button': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span',
}

css_selector = {
    'message_list_tab': 'div._185ho',
    'message_status': "span[data-testid*='msg-dblcheck'],span[data-testid*='msg-check']"
}