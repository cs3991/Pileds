#!/usr/bin/python3

import cherrypy
import DataProcessing


class Root(object):

    #    def __init__(self):
    #        self.strip = led_strip_control.NeoPixel(pin_num=led_strip_control.LED_PIN,
    #                                       n=led_strip_control.LED_COUNT,
    #                                       test=False,
    #                                       overwrite_line=False,
    #                                       target="adafruit")

    @cherrypy.expose
    def index(self):
        indoor_temp, outdoor_temp, indoor_temp2, outdoor_temp2 = DataProcessing.generate_graph()
        with open("/home/famille/dev/Pileds/index.html") as file:
            html = ''
            for l in file:
                html += l
        return html.format(in1=str(round(indoor_temp, 1)).replace('.', ','),
                           out1=str(round(outdoor_temp, 1)).replace('.', ','),
                           in2=str(round(indoor_temp2, 1)).replace('.', ','),
                           out2=str(round(outdoor_temp2, 1)).replace('.', ','))

    @cherrypy.expose
    def refresh(self):
        indoorTemp, outdoorTemp = DataProcessing.generate_complete_data()
        with open("/home/famille/dev/Pileds/current_temp.txt", 'w') as file:
            file.write(str(indoorTemp) + " " + str(outdoorTemp))
        print(indoorTemp, outdoorTemp)
        raise cherrypy.HTTPRedirect("/")


#   @cherrypy.expose
#   def ledOn(self):
#       led_strip_control.linearGradient((0, 255, 0), (255, 0, 0), self.strip, 90)
#       raise cherrypy.HTTPRedirect("/")

#    @cherrypy.expose
#    def ledOff(self):
#        self.strip.fadeout()
#        raise cherrypy.HTTPRedirect("/")

if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', "app.conf")
