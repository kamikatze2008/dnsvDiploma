from protorpc import message_types
from protorpc import messages
from protorpc import remote

import main


class AgentMessage(messages.Message):
    isAlive = messages.BooleanField(1, required=True)
    coordX = messages.IntegerField(2, required=True)
    coordY = messages.IntegerField(3, required=True)


class AgentResponseMessage(messages.Message):
    isAgentCreated = messages.BooleanField(1, required=True)


class RegisterAgent(remote.Service):
    # Add the remote decorator to indicate the service methods
    @remote.method(AgentMessage, AgentResponseMessage)
    def register(self, request):
        # If the Note instance has a timestamp, use that timestamp
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            if (main.Agent.isPresentInFollowingCell(tempAgent)):
                return AgentResponseMessage(isAgentCreated=False)
            else:
                main.Agent.appendToAgentsList(tempAgent)
                return AgentResponseMessage(isAgentCreated=True)
        else:
            return AgentResponseMessage(isAgentCreated=False)

    @remote.method(message_types.VoidMessage, AgentMessage)
    def empty(self, request):
        return AgentMessage(isAlive=True, coordX=-1, coordY=-1)
