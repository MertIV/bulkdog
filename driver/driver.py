from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NoSuchElement
from selenium.common.exceptions import TimeoutException as Timeout
from selenium.common.exceptions import WebDriverException as DriverException
import sys, time
import glob, os



class MessageBot:

    OVERFLOW_CNT = 3
    OVERFLOW_LIMIT = 10

    def __init__(self, driveroptions='chrome-data-mert'):
        self.options = Options()
        #self.options.add_argument("--user-data-dir=C:/Users/msi-/AppData/Local/Google/Chrome/User Data/Default")
        #self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--user-data-dir={}".format(driveroptions))

        self.driver = webdriver.Chrome('C:/Users/msi-/Desktop/Enterpreneur/Side Project/chromedriver.exe',
                                       options=self.options)
        self.driver.maximize_window()

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda driver: self.driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            print(e)
            pass

    def login(self):
        self.driver.get('https://web.whatsapp.com/')
        try:
            el = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')))
            print(el.get_attribute("title"))
            return True
        except Timeout:
            self.login()

    def hit_number(self, phone_number):
        try:
            self.driver.get('https://web.whatsapp.com/send?phone={}'.format(phone_number))

            el2 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/header/div[2]/div/div/span')))

            print(el2.text)
        except Timeout:
            print('Elemanı bulamıyor')
        except Exception as e:
            print(e)

    def send_message(self, message):
        try:
            message_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            message_box.send_keys(message)
            time.sleep(5)
            send_button = self.driver.find_element_by_xpath('//button[@class="_1U1xa"]')
            send_button.click()

            status = WebDriverWait(self.driver, 15).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "z_tTQ"), message))

            print(str(status) + " : Message sent")
            return status
        except Timeout:
            print("Timeout oldu ağa yok yani bu element")
            self.login()
            return False
        except Exception as e:
            print(e)
            self.login()

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

    def attach(self,image_folder_path="images", text=None):
        try:
            attach = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')))
            attach.click()
            self.driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input').send_keys(
                image_folder_path)

            if text is not None:
                textbar = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]')))
                textbar.send_keys(text)

            image = WebDriverWait(self.driver,15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[1]')))
            loaded = image.get_attribute("data-animate-attach-media")
            print(loaded)

            if loaded:
                button = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                button.click()

            status = WebDriverWait(self.driver, 15).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "z_tTQ"), text))

            return status

        except Timeout:
            print('Sayfa yüklenmemiş ona göre aksiyon al')

            return False

    def format_number(self, phone_number):
        phone_number = phone_number.replace(" ", "").replace("+", "").strip()
        if len(phone_number) == 10:
            phone_number = "90{}".format(phone_number)
        return phone_number

    def __del__(self):
        print("Shutting down chrome")
        self.driver.close()


# app1 = MessageBot()
#
# app1.login()
#
# number_list = ['+905313093460']
#
#
# for number in number_list:
#     try:
#         app1.hit_number(number)
#         message_status = app1.attach(image_folder_path='C:/Users/msi-/Desktop/Enterpreneur/kedi.png',
#                                      text='kedi')
#
#         if message_status is False:
#             print('Bu mesaj {} numarasına gönderilmedi '.format(number))
#
#         alert = WebDriverWait(app1.driver, 2).until(EC.alert_is_present())
#         alert.accept()
#     except Timeout:
#         print("Alert vermedi devamke")
