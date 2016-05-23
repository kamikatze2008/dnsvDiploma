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


class AgentMessages(messages.Message):
    agentMessage = messages.MessageField(AgentMessage, 1, repeated=True)


class RegisterAgent(remote.Service):
    @remote.method(AgentMessage, AgentResponseMessage)
    def register(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            if (main.Agent.isPresentInFollowingCell(tempAgent)):
                return AgentResponseMessage(isAgentCreated=False)
            else:
                main.Agent.appendToAgentsList(tempAgent)
                return AgentResponseMessage(isAgentCreated=True)
        else:
            return AgentResponseMessage(isAgentCreated=False)

    @remote.method(AgentMessage, AgentMessages)
    def processing(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            agents = main.Agent.getSurroundedAgents(main.Agent(request.isAlive, request.coordX, request.coordY))
            agentMessageList = []
            for tempAgent in agents:
                agentMessageList.append(AgentMessage(isAlive=tempAgent.isAlive, coordX=tempAgent.coordX,
                                                     coordY=tempAgent.coordY))
            return AgentMessages(agentMessage=agentMessageList)
        else:
            return AgentMessages(agentMessage=None)  # @remote.method(AgentMessage, AgentResponseMessage)

    @remote.method(AgentMessage, message_types.VoidMessage)
    def unregister(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            if main.knownAgents.__contains__(tempAgent):
                main.knownAgents.remove(tempAgent)
                return message_types.VoidMessage()

    @remote.method(message_types.VoidMessage, AgentMessage)
    def empty(self, request):
        return AgentMessage(isAlive=True, coordX=-1, coordY=-1)
