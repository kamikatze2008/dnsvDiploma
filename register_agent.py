from google.appengine.api import memcache
from protorpc import message_types
from protorpc import messages
from protorpc import remote

import main


class AgentMessage(messages.Message):
    isAlive = messages.BooleanField(1, required=True)
    coordX = messages.IntegerField(2, required=True)
    coordY = messages.IntegerField(3, required=True)


class AgentUpdateMessage(messages.Message):
    isAlive = messages.BooleanField(1, required=True)
    coordX = messages.IntegerField(2, required=True)
    coordY = messages.IntegerField(3, required=True)
    newIsAlive = messages.BooleanField(4, required=True)


class AgentResponseMessage(messages.Message):
    isAgentCreated = messages.BooleanField(1, required=True)


class AgentMessages(messages.Message):
    agentMessage = messages.MessageField(AgentMessage, 1, repeated=True)


class LifeGame(remote.Service):


    @remote.method(AgentMessage, AgentResponseMessage)
    def register(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            # if (main.Agent.isPresentInFollowingCell(tempAgent)):
            #     return AgentResponseMessage(isAgentCreated=False)
            # else:
            main.Agent.appendToAgentsList(tempAgent)
            return AgentResponseMessage(isAgentCreated=True)
        else:
            return AgentResponseMessage(isAgentCreated=False)

    @remote.method(AgentUpdateMessage, AgentResponseMessage)
    def update(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            # if main.Agent.isPresentInFollowingCell(tempAgent):
            if (memcache.get('agentToUpdate') is None):
                agentsToUpdate = [[None, None, None, None, None], [None, None, None, None, None],
                                  [None, None, None, None, None],
                                  [None, None, None, None, None], [None, None, None, None, None]]
                agentsToUpdate[tempAgent.coordX][tempAgent.coordY] = main.Agent(request.newIsAlive,
                                                                                         request.coordX,
                                                                                         request.coordY)
                memcache.add('agentToUpdate', agentsToUpdate)
            else:
                agentsToUpdate = memcache.get('agentToUpdate')
                agentsToUpdate[tempAgent.coordX][tempAgent.coordY] = main.Agent(request.newIsAlive,
                                                                                         request.coordX,
                                                                                         request.coordY)
                memcache.replace('agentToUpdate', agentsToUpdate)
            noneFlag = 0
            for agentToUpdate in agentsToUpdate:
                if agentToUpdate.__contains__(None):
                    noneFlag += 1
            # print memcache.get('knownAgents')
            if noneFlag == 0:
                memcache.replace('knownAgents', agentsToUpdate)
                agentsToUpdate = [[None, None, None, None, None], [None, None, None, None, None],
                                           [None, None, None, None, None],
                                           [None, None, None, None, None], [None, None, None, None, None]]
                memcache.replace('agentToUpdate', agentsToUpdate)
                return AgentResponseMessage(isAgentCreated=request.newIsAlive)
            else:
                return AgentResponseMessage(isAgentCreated=not request.newIsAlive)

        else:
            return AgentResponseMessage(isAgentCreated=not request.newIsAlive)

    @remote.method(AgentMessage, AgentMessages)
    def process(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            agents = main.Agent.getSurroundedAgents(main.Agent(request.isAlive, request.coordX, request.coordY))
            agentMessageList = []
            for tempAgent in agents:
                # print tempAgent
                agentMessageList.append(AgentMessage(isAlive=tempAgent.isAlive, coordX=tempAgent.coordX,
                                                     coordY=tempAgent.coordY))
            return AgentMessages(agentMessage=agentMessageList)
        else:
            return AgentMessages(agentMessage=None)  # @remote.method(AgentMessage, AgentResponseMessage)

    @remote.method(AgentMessage, message_types.VoidMessage)
    def unregister(self, request):
        if request.isAlive is not None and request.coordX is not None and request.coordY is not None:
            tempAgent = main.Agent(request.isAlive, request.coordX, request.coordY)
            if main.MainHandler.knownAgents.__contains__(tempAgent):
                main.MainHandler.knownAgents.remove(tempAgent)
                return message_types.VoidMessage()

    @remote.method(message_types.VoidMessage, AgentMessage)
    def empty(self):
        return AgentMessage(isAlive=True, coordX=-1, coordY=-1)
