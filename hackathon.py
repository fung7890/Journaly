from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.config import Config
from colour import Color
import random


Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

Builder.load_string("""
<Logo>:
	canvas.before:
		Rectangle:
			pos: self.pos
			size: self.size
			source: 'logo.PNG'
	BoxLayout:
		Button:
			background_color: 0, 0, 0, 0
			on_press: root.manager.current = 'intro'

<JournalScreen>:
	canvas.before:
		Rectangle:
			pos: self.pos
			size: self.size
			source: 'journal.PNG'

	id: journal_screen
	journal_screen: journal_screen

	FloatLayout:
		Button:
			background_color: 0, 0, 0, 0
			color:0,0,1,1
			on_press: root.journal_screen.save_journal(root.manager, journal.text)
			on_press: root.manager.current = 'intro'
		TextInput:
			size_hint: (None, None)
			size: 275,300
			pos_hint: {'x':0.115, 'y': 0.37}
			id: journal
			text: 'How was your day?'

<Introduction>:
	id: intro
	intro: intro

	canvas.before:
		Rectangle:
			pos: self.pos
			size: self.size
			source: 'intro.PNG'
	BoxLayout:
		Button:
			background_color: 0, 0, 0, 0
			color:0,0,1,1
			text: 'Calendar'
			on_press: root.manager.current = 'calendar'
			on_press: root.intro.getDataFromJournal()
		Button:
			background_color: 0, 0, 0, 0
			color:0,0,1,1
			text: 'Journal'
			on_press: root.manager.current = 'journalScreen'

<Calendar>:
	canvas.before:
		Rectangle:
			pos: self.pos
			size: self.size
			source: 'calendar.PNG'
	BoxLayout:
		Button:
			background_color: 0, 0, 0, 0
			color: 0,0,1,1
			on_press: root.manager.current = 'intro'

""")
class Logo(Screen):
	pass

class JournalScreen(Screen):
	data = [] # sentiment analysis results (0-1)
	journal_data = []
	# def on_enter(self):
		# self.TextInput().text = ""
	def save_journal(self, instance, text):
		analyzer = SentimentIntensityAnalyzer()
		vs = analyzer.polarity_scores(text) # accesses the text written 

		self.data.append((vs['compound'] + 1)/2) # appending sentiment score 
		# self.journal_data.append(text) # saving actual text

class Introduction(Screen):
	def getDataFromJournal(self):
		print(self.manager.get_screen("journalScreen").data)

class Calendar(Screen):
	def on_enter(self): # on startup of Calendar screen
		# remove previous days 
		for child in self.children[:]:
			if child.id == 'date':
				self.remove_widget(child)

		journal_data = self.manager.get_screen("journalScreen").data
		transparency = 0.4
		height = 1
		blue = Color("blue")
		green = Color("green")
		colours = list(blue.range_to(green, 10)) # list of 10 colours of gradient from blue to green 

		# convert color so it contains transparency
		for idx, i in enumerate(range(len(journal_data))): 
			
			# color index will change to int(sentiment*10)
			index = int(journal_data[idx]*10)

			if i < 2:
				height = 1.15
			elif i >= 2 and i < 9:
				height = 1
			elif i >= 9 and i < 16:
				height = 0.845 # 1 - 0.155
			elif i >= 16 and i < 23:
				height = 0.69 # 0.845 - 0.155
			elif i >= 23 and i < 30:
				height = 0.535 # 0.69 - 0.155

			if i >= 2: # readjust i
				i = (i-2)%7

			if height == 1.15:
				col_pos = i*46+250
			else:
				col_pos = i*46+20

			self.add_widget(Button(id = 'date', text = "", size_hint=(None,None), size=(45,45), 
								   pos = (col_pos, height*330), background_normal = '', 
								   background_color= tuple(list(colours[index].rgb)+[transparency])))

class Journaly(App):
	def build(self):
		self.title = 'Journaly'
		# for multiple screen view
		self.sm = ScreenManager() 
		self.sm.add_widget(Logo(name='logo'))
		self.sm.add_widget(Introduction(name='intro'))
		self.sm.add_widget(Calendar(name='calendar'))
		self.sm.add_widget(JournalScreen(name='journalScreen'))

		return self.sm


Journaly().run()
