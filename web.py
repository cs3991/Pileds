import cherrypy
import DataProcessing
import led_strip_control


class Root(object):

    def __init__(self):
        self.strip = led_strip_control.NeoPixel(pin_num=led_strip_control.LED_PIN,
                                       n=led_strip_control.LED_COUNT,
                                       test=False,
                                       overwrite_line=False,
                                       target="adafruit")

    @cherrypy.expose
    def index(self):
        with open("/home/pi/Developpement/pyled/current_temp.txt") as file:
            text = file.readline()
            text_split = text.split(' ')
            indoorTemp = text_split[0]
            outdoorTemp = text_split[1]
        with open("/tmp/pycharm_project_313/index.html") as file:
            html = ''
            for l in file:
                html += l
        return html.format(indoorTemp, outdoorTemp)

    @cherrypy.expose
    def refresh(self):
        indoorTemp, outdoorTemp = DataProcessing.main()
        with open("/home/pi/Developpement/pyled/current_temp.txt", 'w') as file:
            file.write(str(indoorTemp) + " " + str(outdoorTemp))
        print(indoorTemp, outdoorTemp)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def ledOn(self):
        led_strip_control.linearGradient((0, 255, 0), (255, 0, 0), self.strip, 90)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def ledOff(self):
        self.strip.fadeout()
        raise cherrypy.HTTPRedirect("/")

if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', "app.conf")
