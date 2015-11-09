"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb

# import pprint
from apiclient.discovery import build

WEB_CLIENT_ID = '141815902829-9brrjl3uhogcqhnl111uvm9u556op701.apps.googleusercontent.com'
ANDROID_CLIENT_ID = '141815902829-g950g3rrmjef0v5op1ggj5aq9oauuoj2.apps.googleusercontent.com'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Hello'

# Insert function to create a Game

# Function to perform query, parse JSON, retrieve distinct Image and storing into a Level
def queryM():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyAN3l_irEsAG2kT3isRzL8R-baMkOcZgZs")
  res = service.cse().list(
        q='cat',
        cx='008947772147471846402:fdhywbjbitw',
        num='3',
        imgColorType='color',
        imgSize='medium', 
        safe='high'
        rights='cc_publicdomain'
      ).execute()

    # TODO: parse JSON, create Level with the Image(s)

# Game model which contains Level models
# class Game(ndb.Model):

# Level model which has Image models
# class Level(ndb.Model):

# Image model which has a title, whether it is the correct answer or not, and the image
class Image(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    correct = ndb.BooleanProperty()
    image = ndb.BlobProperty()

# Tutorial stuff below
class Greeting(messages.Message):
	"""Greeting that stores a message"""
	message = messages.StringField(1)

class GreetingCollection(messages.Message):
	"""Collection of Greetings."""
	items = messages.MessageField(Greeting, 1, repeated=True) 

STORED_GREETINGS = GreetingCollection(items=[
	Greeting(message='hello world!'),
	Greeting(message='goodbye world!'),
])

@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class HelloWorldApi(remote.Service):
  """Helloworld API v1."""

  @endpoints.method(message_types.VoidMessage, GreetingCollection,
                    path='hellogreeting', http_method='GET',
                    name='greetings.listGreeting')
  def greetings_list(self, unused_request):
    return STORED_GREETINGS

  MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
      Greeting,
      times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                required=True))

  @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                    path='hellogreeting/{times}', http_method='POST',
                    name='greetings.multiply')
  def greetings_multiply(self, request):
    return Greeting(message=request.message * request.times)

  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, Greeting,
                    path='hellogreeting/{id}', http_method='GET',
                    name='greetings.getGreeting')
  def greeting_get(self, request):
    try:
      return STORED_GREETINGS.items[request.id]
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('Greeting %s not found.' %
                                        (request.id,))

  @endpoints.method(message_types.VoidMessage, Greeting,
                  path='authed', http_method='POST',
                  name='greetings.authed')
  def greeting_authed(self, request):
    current_user = endpoints.get_current_user()
    email = (current_user.email() if current_user is not None
             else 'Anonymous')
    return Greeting(message='hello %s' % (email,))

APPLICATION = endpoints.api_server([HelloWorldApi])


