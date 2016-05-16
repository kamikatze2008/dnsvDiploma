# from protorpc import messages
# from protorpc import remote
#
# import main
#
#
# class AgentMessage(messages.Message):
#     isAlive = messages.BooleanField(1, required=True)
#     coordX = messages.IntegerField(2, required=True)
#     coordY = messages.IntegerField(3, required=True)
#
#
# class PostService(remote.Service):
#     # Add the remote decorator to indicate the service methods
#     @remote.method(AgentMessage, AgentMessage)
#     def post_note(self, request):
#         # If the Note instance has a timestamp, use that timestamp
#         if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
#             main.Agent(request.isAlive, request.coordX, request.coordY)
#
#         #
#         # # Else use the current time
#         # else:
#         #     when = datetime.datetime.now()
#         # note = guestbook.Greeting(content=request.text, date=when, parent=guestbook.guestbook_key)
#         # note.put()
#         return AgentMessage(isAlive=True, coordX=-1, coordY=-1)

from protorpc import messages
from protorpc import remote


# Create the request string containing the user's name
class HelloRequest(messages.Message):
    my_name = messages.StringField(1, required=True)


# Create the response string
class HelloResponse(messages.Message):
    hello = messages.StringField(1, required=False)


# Create the RPC service to exchange messages
class PostService(remote.Service):
    @remote.method(HelloRequest, HelloResponse)
    def hello(self, request):
        return HelloResponse(hello='Hello there, %s!' % request.my_name)
