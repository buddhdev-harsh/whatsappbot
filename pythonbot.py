from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import autoit

browser = webdriver.Chrome(executable_path=r'C:/Users/ht501/OneDrive/Desktop/chromedriver.exe')
browser.get('https://web.whatsapp.com/')
sleep(10)


bot_users = {} # A dictionary that stores all the users that sent activate bot 
while True:
	unread = browser.find_elements_by_class_name("_1ZMSM") # The green dot tells us that the message is new
	
	if len(unread) > 0:
		ele = unread[-1]
		action = webdriver.common.action_chains.ActionChains(browser)
		action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot
        
        # Clicking couple of times because sometimes whatsapp web responds after two clicks
		action.click()
		action.perform()
		action.click()
		action.perform()
		
		bot_users[name] = True
		response = "hi this is bot here you can leave msg or wait for him to get online."
		#find element of text box to write message
		text_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
		#find element of search box to send it after writing message
		send_button = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
		#give time to open and find elements some browser works slow
		sleep(4)
		#write message in box
		text_box.send_keys(response)
		sleep(2)
		#send.
		send_button.click()

			
				
			
		
	sleep(2)