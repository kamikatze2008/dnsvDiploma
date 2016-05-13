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
import webapp2
import jinja2
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'agents': [
                [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
                [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
                [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
                [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)],
                [Agent(True), Agent(False), Agent(True), Agent(False), Agent(True)]
            ],
            'temp': Agent(False, 2, 2).getSurroundedAgents(),
            'temp1': Agent(False, 0, 0).getSurroundedAgents(),
            'temp2': Agent(False, 4, 4).getSurroundedAgents(),
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

    def getSurroundedAgents(self):
        surroundedAgents = list()
        i = self.coordX - 1
        j = self.coordY - 1
        for i in range(self.coordX - 1, self.coordX + 2, 1):
            for j in range(self.coordY - 1, self.coordY + 2, 1):
                if i >= 0 and j >= 0 and i<=4 and j<=4 and not (i == self.coordX and j == self.coordY):
                    surroundedAgents.append(Agent(True, i, j))
        print surroundedAgents
        logging.debug(surroundedAgents)
        return surroundedAgents


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
