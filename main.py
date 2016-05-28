#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2
import webapp2
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def getKnownAgents():
    return memcache.get('knownAgents')


class MainHandler(webapp2.RequestHandler):
    knownAgents = [
        [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None],
        [None, None, None, None, None], [None, None, None, None, None]]

    def get(self):
        if memcache.get('knownAgents') is None:
            memcache.add('knownAgents', MainHandler.knownAgents)
        template_values = {
            'agents':
                memcache.get('knownAgents'),
            # MainHandler.knownAgents,
            # [
            # [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
            # [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
            # [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
            # [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
            # [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)]
            # ],
            'global': memcache.get('knownAgents')
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Agent:
    def __init__(self, isAlive, coordX=0, coordY=0):
        self.isAlive = isAlive
        self.coordX = coordX
        self.coordY = coordY

    def __str__(self):
        return "Agent:\nisAlive = %s\ncoordX = %s\ncoordY = %s" % (self.isAlive, self.coordX, self.coordY)

    def __eq__(self, other):
        if isinstance(other, Agent):
            return self.coordX == other.coordX and self.coordY == other.coordY
        else:
            return False

    def isPresentInFollowingCell(self):
        # if not MainHandler.knownAgents or self not in MainHandler.knownAgents:
        #     return False
        # else:
        return False

    def appendToAgentsList(self):
        if memcache.get('knownAgents') is None:
            MainHandler.knownAgents[self.coordX][self.coordY] = self
            memcache.add('knownAgents', MainHandler.knownAgents)
        else:
            MainHandler.knownAgents = memcache.get('knownAgents')
            MainHandler.knownAgents[self.coordX][self.coordY] = self
            memcache.replace('knownAgents', MainHandler.knownAgents)

    def getSurroundedAgents(self):
        surroundedAgents = list()
        for i in range(self.coordX - 1, self.coordX + 2, 1):
            for j in range(self.coordY - 1, self.coordY + 2, 1):
                if i >= 0 and j >= 0 and i <= 4 and j <= 4 and not (i == self.coordX and j == self.coordY) and memcache.get('knownAgents')[i][j] is not None:
                    surroundedAgents.append(memcache.get('knownAgents')[i][j])
        return surroundedAgents


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
