## package imports
import pygame as pygame
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from scipy.io.wavfile import write
## end of package imports

## global variables
IMAGE = "/Users/wentmich/Documents/codes/ispy.github.io/images/book-store.png"
LEVELNAME = input("What's your level name?: ")
NTOT = int(input("How many total objects are there?: "))
LEVELPATH = "" #"/User/wentmich/Documents/codes/ispy.github.io/" + LEVELNAME + "/"
HTML = LEVELNAME + ".html"
CSS = LEVELNAME + ".css"
JS = LEVELNAME + ".js"
FS = 44100
SECONDS = 3.0

## define object class
class newObject:
    def __init__(self):
        self.left = [] # location and dimensions of the button to be used to locate the object
        self.top = []
        self.height = []
        self.width = []
        self.name = '' # html id of the item (there is a confusing relabeling of name in the write_html_block() function, so be careful
        self.sounds = [] # file location for the sounds to be played when the item is found
        self.NSites = 0 # number of locations for the object (i.e. i spy two stop signs)
        self.num = []
        self.ispy_tag = '' # what appears in the object banner
## end of class

def get_aspect_ratio():
    myImg = pygame.image.load(IMAGE)
    myWidth = myImg.get_width()
    myHeight = myImg.get_height()

    return str(myHeight/myWidth);

## get object traits
def get_newObj_traits():
    # get name, number of sites, and sound files names
    myobject = newObject()
    myobject.left = []
    myobject.top = []
    myobject.height = []
    myobject.width = []
    myobject.sounds = []
    myobject.num = []
    myobject.name = input('Name of New Object: ')
    myobject.NSites = int(input('Number of Sites in Object: '))
    myobject.ispy_tag = input('I spy tag for this object: ')
    for i in range(myobject.NSites):
        myobject.num.append(i + 1)
        myobject.sounds.append(LEVELPATH + "sounds/" + myobject.name + str(i) + ".mp3")

    # set mouse position list
    mouse_positions = []

    # get the position and size of the object
    display_width, display_height = 1300, 800
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    backImg = pygame.image.load(IMAGE)
    backImg = pygame.transform.smoothscale(backImg, (display_width, display_height))
    clock = pygame.time.Clock()

    crashed = False

    while not crashed:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill((255, 255, 255))
        gameDisplay.blit(backImg, (0,0))

        mouse = pygame.mouse.get_pos()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                mouse_positions.append(mouse)

        pygame.display.update()
        clock.tick(60)

    for i in range(myobject.NSites):
        myobject.left.append(mouse_positions[-2*(i+1)][0]*100 / display_width)
        myobject.top.append(mouse_positions[-2*(i+1)][1]*100 / display_height)
        myobject.width.append(abs(mouse_positions[-2*(i+1) + 1][0] - mouse_positions[-2*(i+1)][0])*100 / display_width)
        myobject.height.append(abs(mouse_positions[-2*(i+1) + 1][1] - mouse_positions[-2*(i+1)][1])*100 / display_width)
    
    for i in range(myobject.NSites):
        pygame.mixer.init()
        pygame.mixer.music.load('/Users/wentmich/Documents/codes/ispy.github.io/sounds/bell.mp3')
        pygame.mixer.music.play()

        myrecording = sd.rec(int(SECONDS * FS), samplerate=FS, channels=1)
        sd.wait()  # Wait until recording is finished
        write(myobject.name + str(i) + '.wav', FS, myrecording)
        
        mysound = AudioSegment.from_wav(myobject.name + str(i) + '.wav')
        mysound.export(myobject.name + str(i) + '.mp3', format='mp3') # Save as mp3 file


    return myobject;
## end of function

## get all of the objects into a list
def get_all_objects():
    add_obj = 'y'
    levelObjects = []
    while add_obj == 'y':
        levelObjects.append(get_newObj_traits())
        add_obj = input('Add a new object? (y/n): ')
    
    return levelObjects;
## end of function getting all new objects

## css block function
def get_obj_pos_print_css_block(object, n):
    pos_str = ""
    for i in range(object.NSites):
        pos_str += ("#loc" + str(object.num[i] + n) + "{\n" + \
                   "\t/* position button */\n" + \
                   "\tposition: absolute;\n" + \
                   "\tleft:" + str(object.left[i]) + "%;\n" + \
                   "\ttop:" + str(object.top[i]) + "%;\n" + \
                   "\theight:" + str(object.height[i]) + "%;\n" + \
                   "\twidth:" + str(object.width[i]) + "%;\n" + \
                   "\t/* color button */\n" + \
                   "\tborder-radius: 100%;\n" + \
                   "\tborder: none;\n" + \
                   "\tbackground-color: var(--locBtnColor);\n" + \
                   "\t/* object attributes */" + \
                   "\t--name:" + object.name + ";\n")

        for j in range(object.NSites):
            pos_str += "\t--sound" + str(j + 1) + ":" + object.sounds[j] + ";\n"

        pos_str += ("\t--number:" + str(object.NSites) + ";\n" + \
                    "\t--found:0;\n" + \
                    "\t--color: var(--unfound);\n" + \
                    "}\n" + \
                    "#loc" + str(object.num[i] + n) + ":focus { outline-style: none; }\n\n\n")

    pos_str += ("#" + object.name.replace(" ","_").replace("'","_") + "{\n" + \
                "\tcolor: var(--black);\n" + \
                "\tfont-weight: normal;\n" + \
                "\t--number:0;\n" + \
                "}\n\n\n")

    return pos_str;
## end of css block function

############# Write the css file (most different btw levels) ###################
def write_css_file(levelObjects):
    css_str = (":root{\n" + \
               "\t--image:" + IMAGE + ";\n" + \
               "\t--aspectRatio: " + get_aspect_ratio() + ";\n" + \
               "\t--green: #00FF00;\n" + \
               "\t--white: #ffffff;\n" + \
               "\t--black: #000000;\n" + \
               "\t--locBtnColor: none;\n" + \
               "\t--fontsize: auto;\n" + \
               "}\n\n" + \
               "*{\n" + \
               "\tcolor: var(--fontColor);\n" + \
               "\tfont-family: fantasy;\n" + \
               "}\n\n" + \
               "/* add background for entire page */\n" + \
               "body{\n" + \
               "\tbackground-image: url('/Users/wentmich/Documents/codes/ispy.github.io/images/background.jpg');\n" +
               "\tbackground-repeat: no-repeat;\n" + \
               "\tbackground-position: left top;\n" + \
               "\tbackground-attachment: fixed;\n" + \
               "\tbackground-size: 100vw 100vh;\n" + \
               "}\n\n" + \
               "/* header for top of page */\n" + \
               ".header{\n" + \
               "\tposition: fixed;\n" + \
               "\tmargin-top: 0%;\n" + \
               "\tmargin-left: 0%;\n" + \
               "\twidth: 100vw;\n" + \
               "\theight: 8vh;\n" + \
               "\tleft: 0;\n" + \
               "\ttop: 0;\n" + \

               "\tbackground-color: #c4a67b;\n" + \

               "\tz-index: -1;\n" + \
               "\t}\n\n" + \

               "/* add image for the current level */\n" + \
               ".lvlImg{" + \
               "\tposition: relative;\n" + \
               "\twidth: 70vw;\n" + \
               "\theight: calc(70vw * var(--aspectRatio));\n" + \
               "\ttop: 15vh;\n" + \
               "\tleft: 50vw;\n" + \
               "\tmargin: 0 0 0 -35vw;\n" + \

               "\tbackground-image: url('" + IMAGE + "');\n" + \
               "\tbackground-size: 100% auto;\n" + \
               "\tbackground-repeat: no-repeat;\n" + \
               "}\n\n" + \

               "/* add list of objects */\n" + \
               "#objBanner{\n" + \
               "\tposition: absolute;\n" + \
               "\tbox-sizing: border-box;\n" + \
               "\tleft: 50%;\n" + \
               "\ttop: 90%;\n" + \
               "\theight: 10%;\n" + \
               "\twidth: 90%;\n" + \
               "\tpadding-top: 2%;\n" + \
               "\tpadding-bottom: 2%;\n" + \
               "\tpadding-left: 1%;\n" + \
               "\tpadding-right: 1%;\n" + \
               "\tmargin: 0 0 0 -45%;\n" + \

               "\tbackground-image: url('../images/parchment.jpg');\n" + \
               "\tbackground-size: 100% 100%;\n" + \
               "\tbackground-repeat: no-repeat;\n" + \

               "\t--Ntot: " + str(NTOT) + ";\n" + \
               "\t--Nfound: 0;\n" + \
               "}\n\n" + \

               "#ispy{\n" + \
               "\tcolor: var(--black);\n" + \
               "\tfont-weight: normal;\n" + \
               "}\n\n" + \

               "/* add buttons for each object in the level.\n" + \
               "These will be positioned relative to the level image. */\n" + \
               ".location{\n" + \
               "\tborder-radius: 100%;\n" + \
               "\tborder: none;\n" + \
               "\tbackground-color: var(--locBtnColor);\n" + \
               "}\n\n")

    for i in range(len(levelObjects)):
        css_str += get_obj_pos_print_css_block(levelObjects[i], i)

    css_str += (".blankSpace{\n" + \
                "\tposition: relative;\n" + \
                "\tleft: 0;\n" + \
                "\ttop: 5vh;\n" + \
                "\theight: 5vh;\n" + \
                "\twidth: 100vw;\n" + \
                "\tbackground-color: none;\n" + \
                "\tborder: none;\n" + \
                "}\n")


    f_css = open(CSS, "a")
    f_css.write(css_str)
    f_css.close()


############ Write the html file (some is different btw levels) ################
def write_html_file(levelObjects):
    html_str = ("<!DOCTYPE html>\n" + \
                "<html lang='en'>\n" + \
                "<head>\n" + \
                "\t<meta charset='UTF-8'>\n" + \
                "\t<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n" + \
                "\t<title>Main Street</title>\n" + \
                "\t<link rel='stylesheet' href='" + str(LEVELNAME) + ".css'>\n" + \
                "\t<link rel='stylesheet' href='../main.css'>\n" + \
                "</head>\n" + \
                "<body>\n" + \
                "<!-- header -->\n" + \
                "\t<div class='header'>\n" + \
                "\t\t<h1 id='headerTxt'>East Liberty and State</h1>\n" + \
                "\t\t<!-- add a button for the home page -->\n" + \
                "\t\t<a href='../index.html' class='lvlBtn'>\n" + \
                "\t\t\t<h1 class='btnTxt'>Home</h1>\n" + \
                "\t\t</a>\n" + \
                "\t</div>\n\n" + \

                "\t<!-- image for the level -->\n" + \
                "\t<div class='lvlImg'>\n" + \
                "\t\t<!-- set of buttons for each object -->\n")

    NList = len(levelObjects)
    print("Length of NList = " + str(NList))
    currentNumberWritten = 0

    for i in range(NList):
        for j in range(levelObjects[i].NSites):
            html_str += "\t\t<button id='loc" + str(int(currentNumberWritten + 1)) + "' class='location'></button>\n"
            currentNumberWritten += 1

    html_str += ("\n" + \
                "\t\t<!-- add the object list -->\n" + \
                "\t\t<div id='objBanner'>\n")

    list_ids = []
    list_ids.append('ispy')
    list_names = []
    list_names.append('I spy ')
    for i in range(NList):
        list_ids.append(levelObjects[i].name)
        list_names.append(levelObjects[i].ispy_tag)

    for i in range(NList):
        html_str += "\t\t\t<span id='" + list_ids[i] + "'>" + list_names[i] + "</span>\n"

    html_str += "\t\t</div>\n"
    html_str += "\t</div>\n\n"

    html_str += ("\t<!-- add some blank space at the bottom of the page -->\n" + \
                "\t<p class='blankSpace'></p>\n\n" + \
                "\t<!-- load javascript -->\n" + \
                "\t<script src='../textFit-master/textFit.js'></script>\n" + \
                "\t<script src='" + JS + "'></script>\n" + \
                "\t<noscript>You must enable javascript to view the full webpage.</noscript>\n" + \
                "</body>\n" + \
                "</html>")

    f_html = open(HTML, "a")
    f_html.write(html_str)
    f_html.close()
## end of write html file function

## write javascript file function. js is the same for all levels
def write_javascript_file():
    js_str = ("'use strict'\n\n" + \
            "// function for clicking on any object\n" + \
            "function findObj(event){\n" + \
            "\t// play the bell sound for found objects\n" + \
            "\tvar myAudio = new Audio('../sounds/click1.mp3');\n" + \
            "\tmyAudio.play();\n\n" + \

            "\t// get object properties\n" + \
            "\tvar myId = event.target.id;\n" + \
            "\tvar name = getComputedStyle(document.getElementById(myId)).getPropertyValue('--name');\n" + \
            "\tvar NObjs = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--number') );\n" + \
            "\tvar found = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--found') );\n" + \
            "\tvar number = parseInt( getComputedStyle(document.getElementById(name)).getPropertyValue('--number') );\n" + \
            "\tvar Ntot = parseInt( getComputedStyle(document.getElementById('objBanner')).getPropertyValue('--Ntot') );\n" + \
            "\tvar Nfound = parseInt( getComputedStyle(document.getElementById('objBanner')).getPropertyValue('--Nfound') );\n\n" + \

            "\t// play the objects individual sound\n" + \
            "\tif (found == parseInt(0)){\n" + \
            "\t\tvar soundName = '';\n" + \
            "\t\tsoundName += '--sound';\n" + \
            "\t\tsoundName += String(parseInt(number + 1));\n" + \
            "\t\tconsole.log(soundName);\n" + \
            "\t\tmyAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue(soundName));}\n" + \
            "\telse{\n" + \
            "\t\tvar soundName = '';\n" + \
            "\t\tsoundName += '--sound';\n" + \
            "\t\tsoundName += String(parseInt(number));\n" + \
            "\t\tconsole.log(soundName);\n" + \
            "\t\tmyAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue(soundName));}\n" + \
            "\tsetTimeout(() => { myAudio.play(); }, 100);\n\n" + \

            "\t// update found status, update number of found obj, update color of text\n" + \
            "\tif (found == parseInt(0)){\n" + \
            "\t\tdocument.getElementById(myId).style.setProperty('--found', 1);\n" + \
            "\t\tdocument.getElementById(name).style.setProperty('--number', parseInt(number + 1));\n" + \
            "\t\tdocument.getElementById('objBanner').style.setProperty('--Nfound', parseInt(Nfound + 1));\n" + \
            "\tif (parseInt(number + 1) >= NObjs){\n" + \
            "\t\tdocument.getElementById(name).style.setProperty('font-weight', 'bolder');}\n" + \
            "\t}\n\n" + \

            "\t// check for a win\n" + \
            "\tif (parseInt(Nfound + 1) == Ntot){\n" + \
            "\t\tvar newAudio = new Audio('../sounds/victory.mp3');\n" + \
            "\t\tsetTimeout(() => { newAudio.play(); }, 2000);}\n" + \
            "}\n\n" + \

            "// resize the text inside the object banner\n" + \
            "function resetText(){\n" + \
            "\ttextFit(document.getElementById('objBanner'), {alignHoriz: true, alignVert: true});\n" + \
            "\twindow.addEventListener('resize', resetText);\n" + \
            "}\n\n" + \

            "// resize the main image to preserve aspect ratio\n" + \
            "function setAspectRatio() {\n" + \
            "\tvar img = new Image();\n" + \
            "\timg.src = getComputedStyle(document.documentElement).getPropertyValue('--image');\n\n" + \

            "\timg.onload = function(){\n" + \
            "\t\tvar width = img.width;\n" + \
            "\t\tvar height = img.height;\n" + \
            "\t\tvar aspectRatio = height / width;\n" + \
            "\t\tconsole.log('Aspect Ratio: ' + aspectRatio)\n" + \

            "\t\tdocument.documentElement.style.setProperty('--aspectRatio', aspectRatio);\n" + \
            "\t}\n" + \
            "}\n\n" + \

            "// play the intro reading if banner is clicked\n" + \
            "function playBanner() {\n" + \
            "\tvar myAudio = new Audio('../sounds/theater/ispy-theater.mp3');\n" + \
            "\tmyAudio.play();\n" + \
            "}\n\n" + \

            "//Execution of functions\n\n" + \

            "// Adjust the sizes of some stuff to make it look nice.\n" + \
            "setAspectRatio();\n" + \
            "resetText();\n" + \
            "textFit(document.getElementsByClassName('header'), {alignVert: true});\n\n" + \

            "var elements = document.getElementsByClassName('location');\n" + \
            "for (var i = 0; i < elements.length; i++) {\n" + \
            "\telements[i].addEventListener('click', findObj);}\n\n" + \

            "var banner = document.getElementById('objBanner');\n" + \
            "banner.addEventListener('click', playBanner);\n")

    f_js = open(JS, "a")
    f_js.write(js_str)
    f_js.close()
## end of javascript function


############## execute the program ###############
levelObjects = get_all_objects()
write_css_file(levelObjects)
write_html_file(levelObjects)
write_javascript_file()
