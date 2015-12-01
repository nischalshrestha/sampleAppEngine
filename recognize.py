import webapp2

import os
import time
import jinja2

from models import Game
from models import Question
from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Eventually query the list of Games, and their Questions to dynamically populate page
    	game = Game.query().order(-Game.date) # Order by recently added
    	template_values = {	
    		'game_store': game
        }
        template = JINJA_ENVIRONMENT.get_template('match.html')
      	self.response.write(template.render(template_values))

class DisplayGame(webapp2.RequestHandler):
	def get(self):
		# TODO: Need to look at the particular id of the game
		game = Game.query().order(-Game.date) # Order by recently added
		template_values = {	
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		# self.response.write("id: "+self.request.GET['id'])
		self.response.write(template.render(template_values))

class CreateGame(webapp2.RequestHandler):
	def get(self):
		game = Game()
		# games = Game.query().order(-Game.date) # Order by recently added
		template_values = {
			'game': game
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write(template.render(template_values))

class EditGame(webapp2.RequestHandler):
	def get(self):
		urlstring = self.request.GET['id']
		game_key = ""
		if urlstring:
			game_key = ndb.Key(urlsafe=urlstring)

		game = Game()
		if game_key:
			game = game_key.get()
		
		# games = Game.query().order(-Game.date) # Order by recently added
		template_values = {
			'game': game
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write(template.render(template_values))

class CreateQuestion(webapp2.RequestHandler):
	def get(self):
		# TODO Need to acquire game passed from Match
		game = Game.query().order(-Game.date) # Order by recently added
		template_values = {	
			'game': game
		}
		template = JINJA_ENVIRONMENT.get_template('question.html')
		# self.response.write("id: "+self.request.GET['id'])
		self.response.write(template.render(template_values))

class StoreQuestion(webapp2.RequestHandler):
	def post(self):
# 		question = Question(title=self.request.get('question'), parent=game)
#     	answer = self.request.POST.get('correct_answer')
#     	images = self.request.get('image', allow_multiple=True)
#     	image_list = []
#     	# self.response.out.write("title: "+game.title+" question: "+question.title+"\nanswers: "+str(answer) 
#     	#	+ " images: "+str(len(images)))
#     	for i in range(4):
#     		img = Image()
#     		img.image = images[i]
#     		if int(answer) == i:
#     			img.title = "correct_answer_"+str(i)
#     			img.correct = True
#     		else:
#     			img.title = "incorrect_answer_"+str(i)
#     			img.correct = False
#     		question.images.append(img)	
		self.response.write('question stored!')

class StoreGame(webapp2.RequestHandler):
    def post(self):
    	""" TODO Change code so that we:
    	- retrieve the Game from Create
    	- retrieve all Question(s)
    	- set Question's parent as the Game
    	"""
    	game = Game(title=self.request.get('game'), category=self.request.get('category'))
    	question = Question(title=self.request.get('question'), parent=game)
    	answer = self.request.POST.get('correct_answer')
    	images = self.request.get('image', allow_multiple=True)
    	image_list = []
    	# self.response.out.write("title: "+game.title+" question: "+question.title+"\nanswers: "+str(answer) 
    	#	+ " images: "+str(len(images)))
    	for i in range(4):
    		img = Image()
    		img.image = images[i]
    		if int(answer) == i:
    			img.title = "correct_answer_"+str(i)
    			img.correct = True
    		else:
    			img.title = "incorrect_answer_"+str(i)
    			img.correct = False
    		question.images.append(img)

		game.put()
		question.put()
		# TODO: redirect to create i.e. redirect back to /create to refresh that page with the newly created 
		# game with its titles, and list of questions 
		time.sleep(0.1)
		self.redirect('/match')

app = webapp2.WSGIApplication([('/upload', StoreGame),
							   ('/uploadq', StoreQuestion),
							   ('/match', MainPage),
							   ('/match/view', DisplayGame), # TODO: Combine Display and Create
							   ('/create', CreateGame),
							   ('/question', CreateQuestion)],
								debug=True)