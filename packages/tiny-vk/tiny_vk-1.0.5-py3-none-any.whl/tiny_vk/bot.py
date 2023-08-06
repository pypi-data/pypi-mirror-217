import vk_api 
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import threading
import uuid
import inspect,types
import requests,json

from io import BytesIO

from .exceptions import *
from .database import database


def _check_token(token):
  if token is None:
    raise TokenError(f"Token is required")
  if not isinstance(token,str):
    raise TypeError(f"Token must be a string")
  else : return token

def add_to_loop(_object : object):
    """
Add functions or objects to the loop execution.

Args:
    _object (object): The object or function to be added to the loop.

Description:
    - If `_object` is a function, it is added to the `_builder` object with
      the name as a string representation of the function.
    - If `_object` is not a function, it iterates over the attributes of
      the object and selects only the functions (excluding the
      `add_to_loop` function itself). Each selected function is then added
      to the `_builder` object with the name as a string representation
      of the function.
    """
    if isinstance(_object,types.FunctionType):
      setattr(_builder,str(_object),_object)
    else :
      funcs = [func for func in _object.__dict__.values() if inspect.isfunction(func) and func != _builder.add_to_loop]
      for function in funcs:
        setattr(_builder,str(function),function)

class _builder:
  """
An empty class to which functions are passed for execution
  """

class _handlers:
  
  @staticmethod
  def state(*states: str) -> None:
    def inner(function):
      def wrapper(self):
        if self.state in states:
          return function(self)
      _builder.add_to_loop(wrapper)
      return wrapper
    return inner

  @staticmethod
  def message(*commands:str) -> None:
    def inner(function):
      def wrapper(self):
        if self.text in commands:
          return function(self)
        elif not commands:
          return function(self)
      add_to_loop(wrapper)
      return wrapper
    return inner

  @staticmethod
  def multiply(commands : list[str], states : list[str])-> None:
    def inner(function):
      def wrapper(self):
        if self.state in states and self.text in commands:
          return function(self)
      add_to_loop(wrapper)
      return wrapper
    return inner

  @staticmethod
  def empty(condition : str) -> None:
    """
    This decorator takes a single argument called condition, 
    which should be a string that is suitable for use in the eval() function.
    """
    def inner(function):
      def wrapper(self):
        if eval(condition):
          return function(self)
      add_to_loop(wrapper)
      return wrapper
    return inner

class _utils:

  def __init__(self, __token : str, __id : int | str, __chat : bool) -> None:
    self.__vk = vk_api.VkApi(token=__token)
    self.__id = __id
    self.chat = __chat

  def __get_file(self,URI : str):
    from urllib.parse import urlparse
    parsed = urlparse(URI)
    if parsed.scheme and parsed.netloc:
        link_type = "URL"
    else:
        link_type = "PATH"
          
    match link_type:
      case "PATH":
        with open(URI, 'rb') as f:
          buffer = BytesIO(f.read())
      case "URL":
        request = requests.get(URI)
        buffer = BytesIO(request.content)
        
    return buffer
  
  def __upload_link(self,URL : list):
    attachments = ''
    for link in URL:
      attachments+=f'link,{link},'
    return attachments
  
  def __upload_doc(self,URI : dict) -> str:
    attachments = ''
    for filename,uri in URI.items():
      vk = self._vk.get_api()
      upload_url = vk.docs.getMessagesUploadServer(type='doc', peer_id=self._id)['upload_url']
      files = {'file': (filename,self.__get_file(uri).getvalue())}
      result = json.loads(requests.post(upload_url, files=files).text)
      doc = vk.docs.save(file=result['file'],title = filename.split('.'[0]))
      attachments += f"doc{doc['doc']['owner_id']}_{doc['doc']['id']},"
      
    return attachments 
  
  def __upload_photo(self,URI : list) -> str :
    attachments = ''
    upload = VkUpload(self.__vk)
    for uri in URI:
      photo = upload.photo_messages(photos=self.__get_file(uri), peer_id=self.__id)[0]
      attachments += f'photo{photo["owner_id"]}_{photo["id"]},'
    return attachments
  
  def __upload_voice(self,URI : str ) -> str :

    vk = self.__vk.get_api()
    
    upload_url = self.vk.docs.getMessagesUploadServer(type='audio_message',peer_id=self.__id)['upload_url']
    files = {'file': (f'{str(uuid.uuid4())}.mp3', self.__get_file(URI).getvalue())}
    result = json.loads(requests.post(upload_url, files=files).text)
    doc = vk.docs.save(file=result['file'])['audio_message']
    
    return f"doc{doc['owner_id']}_{doc['id']}_{doc['access_key']},"

  def user_message(self,__message : str = None , id : int | str = None, keyboard:dict = None,
                  link : str = None,
                  file : dict = None,
                  photo: list = None,
                  voice: str = None):
    
    if self.chat == 0 and id is None:
      id = self.__id
    if id is None:
      raise EmptyValueError("User id is not defined")
    
    attachments = ''
    if file : attachments += self.__upload_doc(file)
    if photo : attachments += self.__upload_photo(photo)
    if voice : attachments += self.__upload_voice(voice)
    if link : attachments += self.__upload_link(link)
    self.__vk.method('messages.send',{'user_id': int(id), 'message': __message, 'random_id': 0, 'keyboard' : keyboard,'attachment' : attachments})

  def chat_message(self,__message : str = None , id : int | str = None,
                  link : str = None,
                  file : dict = None,
                  photo: list = None,
                  voice: str = None):
    
    if self.chat == 1 and id is None:
      id = self.__id
    if id is None:
      raise EmptyValueError("Chat id is not defined")
    
    attachments = ''
    if file : attachments += self.__upload_doc(file)
    if photo : attachments += self.__upload_photo(photo)
    if voice : attachments += self.__upload_voice(voice)
    if link : attachments += self.__upload_link(link)
    
    self.__vk.method('messages.send',{'chat_id': int(id), 'message': __message, 'random_id': 0,'attachment' : attachments})

class Bot:

  def __init__(self, __token : str = None, group_id : int = None, dbfile : str = 'TinyVK.db',table_name : str  = 'Bot', columns : dict = {}, ) -> None:

    self.__token = _check_token(__token)
    self.chat = 1 if group_id else 0
    
    session = vk_api.VkApi(token=self.__token)
    self.longpoll = VkBotLongPoll(session, group_id=group_id) if self.chat else VkLongPoll(session)
    
    
    # Initializing the database file
    table_name = ['User','Chat'][self.chat]+'Bot'
    self.db = database(dbfile,table_name)

    col = [{"id":"INT"},{"id" : "INT", "state" : "TEXT"}][self.chat] 
    self.db.create_table(col | columns)
    
    # Initializing handlers
    self.on = _handlers()

  def __loop(self) -> None:
    
    # Launching additional utilities
    self.utils = _utils(self.__token, self.id,self.chat)
    
    # Initializing the table
    self.db._one_loop_(self.id)
    
    # Getting attributes for id by database tags
    data = self.db.get_information()
    for name,value in data.items():
      setattr(Bot,name,value)

    # Getting handler functions
    funcs = [func for func in _builder.__dict__.values() if inspect.isfunction(func)]
    for execute_function in funcs:
      execute_function(self)

  def start(self) -> None:
    """Start the bot"""
    if self.chat == 0:
      for event in self.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
          self.id = event.user_id
          self.text = event.text
          
          #Starting a thread with handlers
          threading.Thread(target=self.__loop).start()
    else:
      for event in self.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
          self.id = event.chat_id
          self.text = event.message['text']
          
          #Starting a thread with handlers
          threading.Thread(target=self.__loop).start()