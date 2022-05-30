
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd
import argparse

class OnRobotGripper:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.login()
    
    def login(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        #chrome_options.add_argument('window-size=1920x1080')
        url = f'http://{self.ip}'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.driver.find_element(by = By.XPATH, value = '/html/body/app-root/app-main-layout/app-layout-content/mat-sidenav-container/mat-sidenav-content/div/app-login/div/div/div/div/app-login-form/div/form/div[1]/input').send_keys(self.username)
        self.driver.find_element(by = By.XPATH, value = '/html/body/app-root/app-main-layout/app-layout-content/mat-sidenav-container/mat-sidenav-content/div/app-login/div/div/div/div/app-login-form/div/form/div[2]/input').send_keys(self.password)
        self.driver.find_element(by = By.XPATH, value = '/html/body/app-root/app-main-layout/app-layout-content/mat-sidenav-container/mat-sidenav-content/div/app-login/div/div/div/div/app-login-form/div/form/div[4]/button').click()
        self.driver.get(url)

        elements = self.driver.find_elements(by=By.CLASS_NAME, value = 'btn.on-card-button')

        elements[-1].click()
        
 
    def gripDetected(self):
        tablehtml = self.driver.find_element(by = By.CLASS_NAME, value = 'table.table-bordered.m-0.on-actual-values').get_attribute('outerHTML')
        tablehtml = tablehtml.replace('<span class="status-dot-true">', '<span class="status-dot-true">True').replace('<span class="status-dot-false">', '<span class="status-dot-false">False')
        table = pd.read_html(tablehtml)[0]
        return table.loc[2][1] == 'True'
    
    def isBusy(self):
        tablehtml = self.driver.find_element(by = By.CLASS_NAME, value = 'table.table-bordered.m-0.on-actual-values').get_attribute('outerHTML')
        tablehtml = tablehtml.replace('<span class="status-dot-true">', '<span class="status-dot-true">True').replace('<span class="status-dot-false">', '<span class="status-dot-false">False')
        table = pd.read_html(tablehtml)[0]

        return table.loc[1][1] == 'True' or not self.attarget()
    
    def attarget(self):
        return self.gripDetected() or abs(self.target - self.getposition()) < 1
    
    def getposition(self):
        
        current_width_element, stopbtn = self.driver.find_elements(by = By.CLASS_NAME, value = 'py-4')
        current_width = float(current_width_element.get_attribute('innerHTML').replace('Current width: ', '').replace('mm', ''))
        return current_width
    
    def open(self, force = 20, speed = 10):
        self.moveto(37, force, speed)
    
    def close(self, force = 20, speed = 10):
        self.moveto(0, force, speed)
    

    def moveto(self, width, force = 20, speed = 10):
        assert 0 <= width <= 37
        self.target = width
        cmd = f'http://{self.ip}/api/dc/twofg/grip_external/0/{width}/{force}/{speed}'
        r = requests.get(cmd)
    

        
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, action='store', default='.', help="username")
    parser.add_argument('-pw', '--password', required=True, action='store', default='.', help="password")
    return parser.parse_args()

def main():
    args = get_args()
    gripper = OnRobotGripper('192.168.1.1', args.username, args.password)
    
    

if __name__ == "__main__":
    main()


# Load more products button  

#element=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[.//div[text()='Load more products']]")))
#driver.execute_script("arguments[0].click();", element)

# To verify that whether button is clicked or not
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(2) #wait for page to load
#print(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='qa6 qmz qn0']"))).text)