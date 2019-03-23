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
	id: journal_screen
	journal_screen: journal_screen

	BoxLayout:
		Button:
			text: 'Goto settings'
			on_press: root.manager.current = 'intro'
		TextInput:
			id: journal
			text: 'Hello'
		Button:
			text: 'Save'
			on_press: root.journal_screen.save_journal(root.manager, journal.text)

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

""")
class Logo(Screen):
	pass

class JournalScreen(Screen):
	data = [] # sentiment analysis results (0-1)
	journal_data = []
	def save_journal(self, instance, text):
		print(text) # accesses the text written 
		self.data.append(random.uniform(0.0, 1.0))
		self.journal_data.append(text)

class Introduction(Screen):
	def getDataFromJournal(self):
		print(self.manager.get_screen("journalScreen").data)

class Calendar(Screen):
	def on_enter(self): # on startup of Calendar screen
		journal_data = self.manager.get_screen("journalScreen").data
		transparency = 0.4
		height = 1
		red = Color("red")
		green = Color("green")
		colours = list(red.range_to(green, 10)) # list of 10 colours of gradient from red to green 

		# convert color so it contains transparency
		for idx, i in enumerate(range(len(journal_data))): 
			
			# color index will change to int(sentiment*10)
			index = int(journal_data[idx]*10)

			if i >= 7 and i < 14:
				height = 0.845 # 1 - 0.155
			elif i >= 14 and i < 21:
				height = 0.69 # 0.845 - 0.155
			elif i >= 21 and i < 28:
				height = 0.535 # 0.69 - 0.155

			if i >= 7: # readjust i
				i = i%7

			self.add_widget(Button(text = "", size_hint=(None,None), size=(45,49), 
								   pos = (i*46+20, height*330), background_normal = '', 
								   background_color= tuple(list(colours[index].rgb)+[transparency])))

class TestApp(App):
	def build(self):
		# for multiple screen view
		self.sm = ScreenManager() 
		self.sm.add_widget(Logo(name='logo'))
		self.sm.add_widget(Introduction(name='intro'))
		self.sm.add_widget(Calendar(name='calendar'))
		self.sm.add_widget(JournalScreen(name='journalScreen'))

		return self.sm


TestApp().run()

# TODO
# current day on journal entry

# input string, output 0-1

# access which day to input in journal, save data
# calendar shows everyday on array with sentiment 

#46