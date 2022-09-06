import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn 
import tensorflow
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import random
import json
import pickle


with open("intents.json") as file:
	data = json.load(file)


try:
	with open ("data.pickle","rb") as f:
		words,labels,trainer,output = pickle.load(f)

except:

	words = []
	labels = []
	docs_x = []
	docs_y = []

	for intent in data["intents"]:
		for pattern in intent["patterns"]:
			wrds= nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			docs_y.append(intent["tag"])


		if intent["tag"] not in labels:
			labels.append(intent["tag"])

	words = [stemmer.stem(w.lower()) for w in words if w!="?"]
	words = sorted(list(set(words)))

	labels = sorted(labels)

	trainer = []
	output = []

	out_empty = [0 for _ in range(len(labels))]

	for x,doc in enumerate(docs_x):
		bag = []

		wrds = [stemmer.stem(w) for w in doc]

		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1
		trainer.append(bag)
		output.append(output_row)

	trainer = numpy.array(trainer)
	output = numpy.array(output)

	with open ("data.pickle","wb") as f:
		pickle.dump((words,labels,trainer,output ), f)


# tensorflow.reset_default_graph()

net = tflearn.input_data(shape = [None , len(trainer[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]),activation ="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
	model.load("model.tflearn")
except:

	model.fit(trainer , output , n_epoch=1000,batch_size=8, show_metric=True)
	model.save("model.tflearn")

def bag_of_words(s,words):
	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i,w in enumerate(words):
			if w==se:
				bag[i] = 1
	return numpy.array(bag)

def chat():
	browser = webdriver.Chrome(executable_path=r'C:/Users/ht501/OneDrive/Desktop/chromedriver.exe')
	browser.get('https://web.whatsapp.com/')
	sleep(7)

	while True:
		
		#creating unread chats list
		sleep(3)
		unread_list = browser.find_elements_by_class_name("OUeyt") # The green dot tells us that the message is new
		
		#by checking it we will know if theres any unread chats exists or not
		if len(unread_list) > 0:
			#to assign from last chat bcs after replying chat will move to upwords
			ele = unread_list[-1]
			
			print(ele.text)
			action = webdriver.common.action_chains.ActionChains(browser)
			# move a bit to the left from the green dot
			action.move_to_element_with_offset(ele, 0, -20)
		    

	        # Clicking couple of times because sometimes whatsapp web responds after two clicks
			action.click()
			action.perform()
			"""action.click()
												action.perform()"""
			sleep(2)
			#find element of text box to write message
			try:
				scroll_button = browser.find_element_by_xpath('//*[@id="main"]/div[3]/div/span[2]/div/span[1]/span')
				print(scroll_button.text)
				if len(scroll_button.text)>0:
					scroll_button.click()
			except:
				print("not found")


			msg = []
			msg = browser.find_elements_by_class_name('_3zb-j')
			"""for i in msg:
													print("all the msg in list: "+i.text)"""
			msg1 = msg[-1]
			msg1 = msg1.text.lower()
			#give input to model to predict ans
			print("last message of user: "+msg1)

			result = model.predict([bag_of_words(msg1, words)])
			result_index = numpy.argmax(result)
			tag = labels[result_index]

			for tg in data["intents"]:
				if tg['tag'] == tag:
					response = tg['responses']
			response = random.choice(response)
			print("response of computer: "+response)
			text_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
			#find element of search box to send it after writing message
			sleep(2)
			#write message in box
			text_box.send_keys(response)
			
			send_button = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span')
			#give time to open and find elements some browser works slow
			
			#send.
			send_button.click()
			
			"""to continue one chat with anyone if a theres only one user whom chatiing with then it wo get new msg notification
			it will go to second chat which has no msg it will happen so quick so that are new chat remains unread and it will add to that
			unreadchat list,,,,and there will be no problem if we open a second chat which has no msg. """ 
			"""if len(unread_list) == 1:
															name = []
															name = browser.find_elements_by_class_name("_3NWy8")
															name = name[-1]
															name.click()
														#if we are not talking to only one then it will pass the statement and code will run untill theres only one user 		
														else:
															pass"""
			try:
				scroll_button = browser.find_element_by_xpath('//*[@id="main"]/div[3]/div/span[2]/div/span[1]/span')
				#print(scroll_button.text)
				if len(scroll_button.text)>0:
					scroll_button.click()
			except:
					
				listforscroll = []
				listforscroll = browser.find_elements_by_class_name('_3zb-j')
							
				msg2 = listforscroll[0]
				#print("mesg to scroll: "+msg2.text)
				browser.execute_script('arguments[0].scrollIntoView()',msg2)
		
				print("not found")		


chat()