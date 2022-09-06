from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# import autoit
from selenium.webdriver.common.by import By

# browser = Service(executable_path='D:/softwarelibs/chromedriver_win32/chromedriver.exe', log_path='NUL')
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get('https://web.whatsapp.com/')
sleep(10)


bot_users = {} # A dictionary that stores all the users that sent activate bot 
while True:
	name = ''
	unread = browser.find_elements(By.CLASS_NAME, '_1pJ9J') # The green dot tells us that the message is new
	
	if len(unread) > 0:
		print(unread)
		print("in if block")
		ele = unread[-1]
		action = webdriver.common.action_chains.ActionChains(browser)
		action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot
        
        # Clicking couple of times because sometimes whatsapp web responds after two clicks
		action.click()
		action.perform()
		
		sleep(4)
		name = browser.find_elements(By.XPATH,'//*[@id="main"]/header/div[2]/div/div/span')
		name = name[0].text
		print(name)
		bot_users[name] = True
		response = "hi " +name+" this is bot here you can leave msg or wait for him to get online."
		#find element of text box to write message
		text_box = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')
		sleep(1)
		#find element of search box to send it after writing message
		#give time to open and find elements some browser works slow
		sleep(4)
		#write message in box
	
		text_box.send_keys(response)
		sleep(2)
		send_button = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
		#send.
		sleep(10)
		send_button.click()
		
		
		del bot_users[name]
			
				
			
		
