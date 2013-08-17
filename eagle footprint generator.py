#!/usr/bin/python2
# Made by Cruz Monrreal II
# Last modified: 09:15pm, 05/31/2012
# Copyright CC-By-SA


from Tkinter import *
from ttk import *
from xml.dom.minidom import Document

class Part:
    def __init__(self, width, length, pinWidth, pinLength, pinPitch, pinCountY, pinCountX, smdPadWidth, smdPadLength, smdPadOffset, thermalPadWidth, thermalPadLength, innerPins):
        self.width = width
        self.length = length

        self.pinWidth = pinWidth
        self.pinLength = pinLength
        self.pinPitch = pinPitch

        self.pinCountY = pinCountY
        self.pinCountX = pinCountX

        self.smdPadWidth = smdPadWidth
        self.smdPadLength = smdPadLength
        self.smdPadOffset = smdPadOffset

        self.thermalPadWidth = thermalPadWidth
        self.thermalPadLength = thermalPadLength

        self.innerPins = innerPins

# Set some defaults based off TI parts
defaults={}
defaults['QFN']  = [3.0, 3.0, .24,   .4,  .5,  4,  4, .38,  .85, 0.4, 1.7, 1.7, True]   #TPS62133
defaults['LQFP'] = [7.0, 7.0, .22,  1.0,  .5, 12, 12, .36, 1.07, 0.0, 0.0, 0.0, False]  #LM3S811
#defaults['SOIC'] = [4.0, 4.0,  .3, .625, .65,  8,  0, .44, .765, 0.0, 0.0, 0.0, False]  #

class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(sticky=N+S+W+E)
        self.master = master

        # Allow window resizing to propagate
        top = self.frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.initUI()
        self.reloadUIConfig(0, self.type.get())

    def initUI(self):
    ## Create UI Structure ##

        #  A1
        self.a1 = Frame(self.frame)
        self.a1.grid(row=0, column=0, sticky=N+S+W+E)
        self.a1.rowconfigure(0, weight=1)
        self.a1.columnconfigure(1, weight=1)

        #    B1
        self.b1 = Frame(self.a1)
        self.b1.grid(row=0, column=0, sticky=N+S+W+E)

        #      C1
        self.c1 = Frame(self.b1)
        self.c1.grid(row=0, column=0, columnspan=2, sticky=N+S+W+E)

        Label(self.c1, text="Type:").pack(side=LEFT, padx=3, pady=3)

        self.type = Combobox(self.c1, width=6, state="readonly", values=defaults.keys())
        self.type.pack(side=LEFT, padx=3, pady=3)
        self.type.set(defaults.keys()[0])
        self.type.bind('<<ComboboxSelected>>', self.reloadUIConfig)

        self.add = Button(self.c1, text="Generate XML", command=self.generateXML)
        self.add.pack(side=RIGHT)

        #      C2
        self.c2 = Frame(self.b1)
        self.c2.grid(row=1, column=0, sticky=N+S+W+E)
        self.c2.rowconfigure(1, minsize=10)

        ## Pin/Pad Dimentions ##

        #        D1
        self.d1 = LabelFrame(self.c2, text="Package Dimentions")
        self.d1.grid(row=0, column=0, sticky=N+S+W+E)
        self.d1.columnconfigure(0, minsize=20)
        self.d1.columnconfigure(1, weight=1)

        ## Pin/Pad Count ##

        #        D2
        self.d2 = LabelFrame(self.c2, text="Pin Count")
        self.d2.grid(row=1, column=0, sticky=N+S+W+E)
        self.d2.columnconfigure(0, minsize=20)
        self.d2.columnconfigure(1, weight=1)

        ## Part Dimentions ##

        #        D3
        self.d3 = LabelFrame(self.c2, text="Pin Dimentions")
        self.d3.grid(row=2, column=0, sticky=N+S+W+E)
        self.d3.columnconfigure(0, minsize=20)
        self.d3.columnconfigure(1, weight=1)

        ## SMD Pad ##

        #        D4
        self.d4 = LabelFrame(self.c2, text="SMD Pad")
        self.d4.grid(row=3, column=0, sticky=N+S+W+E)
        self.d4.columnconfigure(0, minsize=20)
        self.d4.columnconfigure(1, weight=1)

        ## Thermal Pad ##

        #        D5
        self.d5 = LabelFrame(self.c2, text="Thermal Pad")
        self.d5.grid(row=4, column=0, sticky=N+S+W+E)
        self.d5.columnconfigure(0, minsize=20)
        self.d5.columnconfigure(1, weight=1)

        #      C3
        self.c3 = Frame(self.b1)
        self.c3.grid(row=1, column=1, sticky=N+S+E)

        self.img = Canvas(self.c3, width=175, height=250, background='white')
        self.img.grid(sticky=N+S+W+E)

        ## Part Image ##

        #    B2
        self.b2 = Frame(self.a1)
        self.b2.grid(row=0, column=1, sticky=N+S+W+E)

        self.preview = Canvas(self.b2, width=300, height=300, background='black')
        self.preview.pack(expand=YES, fill=BOTH)
        self.preview.bind('<Configure>', self.updateCanvas)
        self.centerX, self.centerY = 150, 150;

        #  A2
        self.a2 = Frame(self.frame)
        self.a2.grid(row=1, column=0, sticky=S+W+E)
        self.a2.rowconfigure(0, weight=1)
        self.a2.columnconfigure(1, weight=1)

        #    B3
        self.b3 = LabelFrame(self.a2, text="Eagle Options")
        self.b3.grid(row=0, column=0, sticky=N+S+W)

        Label(self.b3, text="Name:").grid(row=0, column=0, sticky=N+W)
        self.eagle_name = Entry(self.b3, width=16)
        self.eagle_name.grid(row=0, column=1)

        Label(self.b3, text="Description:").grid(row=1, column=0, sticky=N+W)
        self.eagle_desc = Text(self.b3, width=20, height=5)
        self.eagle_desc.grid(row=2, column=0, columnspan=2, sticky=N+S+W+E)

        #    B4
        self.b4 = LabelFrame(self.a2, text="Generated XML")
        self.b4.grid(row=0, column=1, sticky=N+S+W+E)
        self.b4.columnconfigure(0, weight=1)

        self.eagle_xml = Text(self.b4, height=7, width=60, background='white')
        self.eagle_xml.grid(row=0, column=0, sticky=N+S+W+E)

        scrollbar = Scrollbar(self.b4)
        scrollbar.grid(row=0, column=1, sticky=N+S+W+E)
        self.eagle_xml.configure(yscrollcommand=scrollbar.set)

    ## Initialize UI Elements

        ## Part Dimentions ##

        Label(self.d1, text="Width").grid(row=0, column=0, sticky=N+S+W)
        self.ui_partWidth=Spinbox(self.d1, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.width)
        self.ui_partWidth.bind("<Return>", self.updatePart)
        self.ui_partWidth.grid(row=0, column=1, sticky=N+S+E)

        Label(self.d1, text="Length").grid(row=1, column=0, sticky=N+S+W)
        self.ui_partLength=Spinbox(self.d1, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.length)
        self.ui_partLength.bind("<Return>", self.updatePart)
        self.ui_partLength.grid(row=1, column=1, sticky=N+S+E)

        ## Pin/Pad Count ##

        Label(self.d2, text="X:").grid(row=0, column=0, sticky=N+S+W)
        self.ui__pinCountX = Spinbox(self.d2, width=6, from_=0.0, to=99.9, increment=1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.pinCountX)
        self.ui__pinCountX.bind("<Return>", self.updatePart)
        self.ui__pinCountX.grid(row=0, column=1, sticky=N+S+E)

        Label(self.d2, text="Y:").grid(row=1, column=0, sticky=N+S+W)
        self.ui_pinCountY = Spinbox(self.d2, width=6, from_=0.0, to=99.9, increment=1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.pinCountY)
        self.ui_pinCountY.bind("<Return>", self.updatePart)
        self.ui_pinCountY.grid(row=1, column=1, sticky=N+S+E)

        ## Pin/Pad Dimentions ##

        Label(self.d3, text="Width").grid(row=0, column=0, sticky=N+S+W)
        self.ui_pinWidth=Spinbox(self.d3, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.pinWidth)
        self.ui_pinWidth.bind("<Return>", self.updatePart)
        self.ui_pinWidth.grid(row=0, column=1, sticky=N+S+E)

        Label(self.d3, text="Length").grid(row=1, column=0, sticky=N+S+W)
        self.ui_pinLength=Spinbox(self.d3, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.pinLength)
        self.ui_pinLength.bind("<Return>", self.updatePart)
        self.ui_pinLength.grid(row=1, column=1, sticky=N+S+E)

        Label(self.d3, text="Pitch").grid(row=2, column=0, sticky=N+S+W)
        self.ui_pinPitch=Spinbox(self.d3, width=6, from_=0.0, to=99.99, increment=0.01, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.pinPitch)
        self.ui_pinPitch.bind("<Return>", self.updatePart)
        self.ui_pinPitch.grid(row=2, column=1, sticky=N+S+E)

        ## SMD Pad ##

        Label(self.d4, text="Width").grid(row=0, column=0, sticky=N+S+W)
        self.ui_smdPadWidth=Spinbox(self.d4, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.smdPadWidth)
        self.ui_smdPadWidth.bind("<Return>", self.updatePart)
        self.ui_smdPadWidth.grid(row=0, column=1, sticky=N+S+E)

        Label(self.d4, text="Length").grid(row=1, column=0, sticky=N+S+W)
        self.ui_smdPadLength=Spinbox(self.d4, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.smdPadLength)
        self.ui_smdPadLength.bind("<Return>", self.updatePart)
        self.ui_smdPadLength.grid(row=1, column=1, sticky=N+S+E)

        Label(self.d4, text="Offset").grid(row=2, column=0, sticky=N+S+W)
        self.ui_smdPadOffset=Spinbox(self.d4, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.smdPadOffset)
        self.ui_smdPadOffset.bind("<Return>", self.updatePart)
        self.ui_smdPadOffset.grid(row=2, column=1, sticky=N+S+E)

        ## Thermal Pad ##

        Label(self.d5, text="Width").grid(row=0, column=0, sticky=N+S+W)
        self.ui_thermalPadWidth=Spinbox(self.d5, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.thermalPadWidth)
        self.ui_thermalPadWidth.bind("<Return>", self.updatePart)
        self.ui_thermalPadWidth.grid(row=0, column=1, sticky=N+S+E)

        Label(self.d5, text="Length").grid(row=1, column=0, sticky=N+S+W)
        self.ui_thermalPadLength=Spinbox(self.d5, width=6, from_=0.0, to=99.9, increment=0.1, command=self.updatePart, validate="focusout", vcmd=self.updatePart, textvariable=partUI.thermalPadLength)
        self.ui_thermalPadLength.bind("<Return>", self.updatePart)
        self.ui_thermalPadLength.grid(row=1, column=1, sticky=N+S+E)

    ## Part Image  ##

        #self.gif = PhotoImage(file = "images\qfp.gif")
        #self.img.create_image(0, 0, image = self.gif, anchor=NW)

    def updateCanvas(self, event):
        self.centerX, self.centerY = (event.width-4)/2.0, (event.height-4)/2.0
        self.redrawPart()

    def reloadUIConfig(self, event, type=defaults.keys()[0]):
        if (event != 0):
            type=self.type.get()
            print type

        ## Load Default Values ##
        partUI.width.set(defaults[type][0])
        partUI.length.set(defaults[type][1])
        partUI.pinWidth.set(defaults[type][2])
        partUI.pinLength.set(defaults[type][3])
        partUI.pinPitch.set(defaults[type][4])
        partUI.pinCountY.set(defaults[type][5])
        partUI.pinCountX.set(defaults[type][6])
        partUI.smdPadWidth.set(defaults[type][7])
        partUI.smdPadLength.set(defaults[type][8])
        partUI.smdPadOffset.set(defaults[type][9])
        partUI.thermalPadWidth.set(defaults[type][10])
        partUI.thermalPadLength.set(defaults[type][11])
        partUI.innerPins.set(defaults[type][12])

        ## TODO: Load UI Config ##

        ## Refraw Parts
        self.redrawPart()

    def updatePart(self, *args):
        self.redrawPart()
        return True

    def redrawPart(self):
        centerX, centerY = self.centerX, self.centerY
        ratio = 0.9

        # Scale Part
        try:
            if (partUI.innerPins.get() == True):
                if (partUI.width.get()/(2*centerX) > partUI.length.get()/(2*centerY)):
                    zoom = ratio*2*centerX/(partUI.width.get()+2*partUI.smdPadOffset.get())
                else:
                    zoom = ratio*2*centerY/(partUI.length.get()+2*partUI.smdPadOffset.get())
            else:
                if ((partUI.width.get()+2*partUI.pinLength.get())/(2*centerX) > (partUI.length.get()+2*partUI.pinLength.get())/(2*centerY)):
                    zoom = ratio*2*centerX/(partUI.width.get()+2*partUI.pinLength.get())
                else:
                    zoom = ratio*2*centerY/(partUI.length.get()+2*partUI.pinLength.get())

        except ZeroDivisionError:   # When first initialized, most values are 0.0
            zoom = 100.0

        ## Create tmp part (do all get() calls here) ##
        part = Part(partUI.width.get(), partUI.length.get(), partUI.pinWidth.get(), partUI.pinLength.get(), partUI.pinPitch.get(), partUI.pinCountY.get(), partUI.pinCountX.get(), partUI.smdPadWidth.get(), partUI.smdPadLength.get(), partUI.smdPadOffset.get(), partUI.thermalPadWidth.get(), partUI.thermalPadLength.get(), partUI.innerPins.get())

        ## Redraw everythng from scratch ##
        self.preview.delete(ALL)

        ## Draw Part ##
        try:
            ## Drawing Thermal Pad
            if (part.thermalPadWidth * part.thermalPadLength != 0):
                self.preview.create_rectangle(centerX-zoom*part.thermalPadWidth/2.0, centerY-zoom*part.thermalPadLength/2.0, centerX+zoom*part.thermalPadWidth/2.0, centerY+zoom*part.thermalPadLength/2.0, outline="", fill="#AA0000")

            ## Starting offset for pads
            if (part.pinCountY % 2 == 0):
                startY = (part.pinCountY-1)/2*part.pinPitch + part.pinPitch/2.0
            else:
                startY = (part.pinCountY)/2*part.pinPitch

            if (part.pinCountX % 2 == 0):
                startX = (part.pinCountX-1)/2*part.pinPitch + part.pinPitch/2.0
            else:
                startX = (part.pinCountX)/2*part.pinPitch

            ## Drawing SMD Pads
            if (part.innerPins == True):    # Pins Inside
                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX-zoom*(part.width/2.0+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch+part.smdPadWidth/2.0), centerX-zoom*(part.width/2.0-part.smdPadLength+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch-part.smdPadWidth/2.0), outline="", fill="#AA0000")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch+part.smdPadWidth/2.0), centerY+zoom*(part.length/2.0+part.smdPadOffset), centerX-zoom*(startX-i*part.pinPitch-part.smdPadWidth/2.0), centerY+zoom*(part.length/2.0-part.smdPadLength+part.smdPadOffset), outline="", fill="#AA0000")

                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX+zoom*(part.width/2.0+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch-part.smdPadWidth/2.0), centerX+zoom*(part.width/2.0-part.smdPadLength+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch+part.smdPadWidth/2.0), outline="", fill="#AA0000")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch-part.smdPadWidth/2.0), centerY-zoom*(part.length/2.0+part.smdPadOffset), centerX-zoom*(startX-i*part.pinPitch+part.smdPadWidth/2.0), centerY-zoom*(part.length/2.0-part.smdPadLength+part.smdPadOffset), outline="", fill="#AA0000")
            else:                           # Pins Outside
                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX-zoom*(part.width/2.0+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch-part.smdPadWidth/2.0), centerX-zoom*(part.width/2.0+part.smdPadLength+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch+part.smdPadWidth/2.0), outline="", fill="#AA0000")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch-part.smdPadWidth/2.0), centerY+zoom*(part.length/2.0+part.smdPadOffset), centerX-zoom*(startX-i*part.pinPitch+part.smdPadWidth/2.0), centerY+zoom*(part.length/2.0+part.smdPadLength+part.smdPadOffset), outline="", fill="#AA0000")

                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX+zoom*(part.width/2.0+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch-part.smdPadWidth/2.0), centerX+zoom*(part.width/2.0+part.smdPadLength+part.smdPadOffset), centerY-zoom*(startY-i*part.pinPitch+part.smdPadWidth/2.0), outline="", fill="#AA0000")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch-part.smdPadWidth/2.0), centerY-zoom*(part.length/2.0+part.smdPadOffset), centerX-zoom*(startX-i*part.pinPitch+part.smdPadWidth/2.0), centerY-zoom*(part.length/2.0+part.smdPadLength+part.smdPadOffset), outline="", fill="#AA0000")

            ## Drawing Pins/Pads
            if (part.innerPins == True):    # Pins Inside
                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX-zoom*(part.width/2.0), centerY-zoom*(startY-i*part.pinPitch+part.pinWidth/2.0), centerX-zoom*(part.width/2.0-part.pinLength), centerY-zoom*(startY-i*part.pinPitch-part.pinWidth/2.0), outline="",fill="#FFFFFF")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch+part.pinWidth/2.0), centerY+zoom*(part.length/2.0), centerX-zoom*(startX-i*part.pinPitch-part.pinWidth/2.0), centerY+zoom*(part.length/2.0-part.pinLength), outline="", fill="#FFFFFF")

                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX+zoom*(part.width/2.0), centerY-zoom*(startY-i*part.pinPitch-part.pinWidth/2.0), centerX+zoom*(part.width/2.0-part.pinLength), centerY-zoom*(startY-i*part.pinPitch+part.pinWidth/2.0), outline="", fill="#FFFFFF")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch-part.pinWidth/2.0), centerY-zoom*(part.length/2.0), centerX-zoom*(startX-i*part.pinPitch+part.pinWidth/2.0), centerY-zoom*(part.length/2.0-part.pinLength), outline="", fill="#FFFFFF")
            else:                           # Pins Outside
                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX-zoom*(part.width/2.0), centerY-zoom*(startY-i*part.pinPitch+part.pinWidth/2.0), centerX-zoom*(part.width/2.0+part.pinLength), centerY-zoom*(startY-i*part.pinPitch-part.pinWidth/2.0), outline="",fill="#FFFFFF")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch+part.pinWidth/2.0), centerY+zoom*(part.length/2.0), centerX-zoom*(startX-i*part.pinPitch-part.pinWidth/2.0), centerY+zoom*(part.length/2.0+part.pinLength), outline="", fill="#FFFFFF")

                for i in range(part.pinCountY):
                    self.preview.create_rectangle(centerX+zoom*(part.width/2.0), centerY-zoom*(startY-i*part.pinPitch-part.pinWidth/2.0), centerX+zoom*(part.width/2.0+part.pinLength), centerY-zoom*(startY-i*part.pinPitch+part.pinWidth/2.0), outline="", fill="#FFFFFF")

                for i in range(part.pinCountX):
                    self.preview.create_rectangle(centerX-zoom*(startX-i*part.pinPitch-part.pinWidth/2.0), centerY-zoom*(part.length/2.0), centerX-zoom*(startX-i*part.pinPitch+part.pinWidth/2.0), centerY-zoom*(part.length/2.0+part.pinLength), outline="", fill="#FFFFFF")

            # Drawing guide lines
            self.preview.create_line(centerX - zoom*part.width/2, centerY, centerX + zoom*part.width/2, centerY, fill="#AAAA00", dash="2")
            self.preview.create_line(centerX, centerY - zoom*part.length/2, centerX, centerY + zoom*part.length/2, fill="#AAAA00", dash="2")

            # Drawing outline of part
            self.preview.create_rectangle(centerX - zoom*part.width/2, centerY - zoom*part.length/2, centerX + zoom*part.width/2, centerY + zoom*part.length/2, fill="", outline="#FFFFFF", width=str(0.1*zoom))


        except ValueError:
            print "OFuck."

    def generateXML(self, *args):
        # Clear XML
        self.eagle_xml.delete(0.0, END)

        # Check for name
        if (len(str(self.eagle_name.get())) == 0):
            self.eagle_xml.insert(0.0, "Part name required.")
        else:
            ## Create tmp part (do all get() calls here) ##
            part = Part(partUI.width.get(), partUI.length.get(), partUI.pinWidth.get(), partUI.pinLength.get(), partUI.pinPitch.get(), partUI.pinCountY.get(), partUI.pinCountX.get(), partUI.smdPadWidth.get(), partUI.smdPadLength.get(), partUI.smdPadOffset.get(), partUI.thermalPadWidth.get(), partUI.thermalPadLength.get(), partUI.innerPins.get())


            ## Create XML ##
            doc = Document()
            package = doc.createElement("package")
            package.setAttribute("name", self.eagle_name.get())
            doc.appendChild(package)


            # Create Part Outline
            self.xmlAppendWire(doc, package, -part.width/2.0, part.length/2.0, part.width/2.0, part.length/2.0)
            self.xmlAppendWire(doc, package, part.width/2.0, part.length/2.0, part.width/2.0, -part.length/2.0)
            self.xmlAppendWire(doc, package, part.width/2.0, -part.length/2.0, -part.width/2.0, -part.length/2.0)
            self.xmlAppendWire(doc, package, -part.width/2.0, -part.length/2.0, -part.width/2.0, part.length/2.0)


            # Create pins/pads
            if (part.pinCountY % 2 == 0):
                startY = (part.pinCountY-1)/2*part.pinPitch + part.pinPitch/2.0
            else:
                startY = (part.pinCountY)/2*part.pinPitch

            if (part.pinCountX % 2 == 0):
                startX = (part.pinCountX-1)/2*part.pinPitch + part.pinPitch/2.0
            else:
                startX = (part.pinCountX)/2*part.pinPitch

            if (part.innerPins == True):    # Pins Inside
                for i in range(part.pinCountY):
                    self.xmlAppendRectangle(doc, package, -part.width/2.0, -(startY-i*part.pinPitch+part.pinWidth/2.0), -(part.width/2.0-part.pinLength), -(startY-i*part.pinPitch-part.pinWidth/2.0))
                for i in range(part.pinCountX):
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.pinWidth/2.0), part.length/2.0, -(startX-i*part.pinPitch-part.pinWidth/2.0), part.length/2.0-part.pinLength)
                for i in range(part.pinCountY):
                    self.xmlAppendRectangle(doc, package, part.width/2.0, -(startY-i*part.pinPitch-part.pinWidth/2.0), part.width/2.0-part.pinLength, -(startY-i*part.pinPitch+part.pinWidth/2.0))
                for i in range(part.pinCountX):
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.pinWidth/2.0), -(part.length/2.0), -(startX-i*part.pinPitch+part.pinWidth/2.0), -(part.length/2.0-part.pinLength))
            else:                           # Pins Outside
                for i in range(part.pinCountY):
                    self.xmlAppendRectangle(doc, package, -part.width/2.0, -(startY-i*part.pinPitch+part.pinWidth/2.0), -(part.width/2.0+part.pinLength), -(startY-i*part.pinPitch-part.pinWidth/2.0))
                for i in range(part.pinCountX):
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.pinWidth/2.0), part.length/2.0, -(startX-i*part.pinPitch-part.pinWidth/2.0), part.length/2.0+part.pinLength)
                for i in range(part.pinCountY):
                    self.xmlAppendRectangle(doc, package, part.width/2.0, -(startY-i*part.pinPitch-part.pinWidth/2.0), part.width/2.0+part.pinLength, -(startY-i*part.pinPitch+part.pinWidth/2.0))
                for i in range(part.pinCountX):
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.pinWidth/2.0), -(part.length/2.0), -(startX-i*part.pinPitch+part.pinWidth/2.0), -(part.length/2.0+part.pinLength))


            # Create SMD Pads
            name = 1
            if (part.innerPins == True):    # Pins Inside
                for i in range(part.pinCountY):
                    self.xmlAppendSmd(doc, package, str(name), -part.width/2.0-part.smdPadOffset+part.smdPadLength/2.0, startY-i*part.pinPitch, part.smdPadLength, part.smdPadWidth, angle=0)
                    self.xmlAppendRectangle(doc, package, -(part.width/2.0+part.smdPadOffset), -(startY-i*part.pinPitch+part.smdPadWidth/2.0), -(part.width/2.0-part.smdPadLength+part.smdPadOffset), -(startY-i*part.pinPitch-part.smdPadWidth/2.0),29)
                    self.xmlAppendRectangle(doc, package, -(part.width/2.0+part.smdPadOffset), -(startY-i*part.pinPitch+part.smdPadWidth/2.0), -(part.width/2.0-part.smdPadLength+part.smdPadOffset), -(startY-i*part.pinPitch-part.smdPadWidth/2.0),31)
                    name += 1
                for i in range(part.pinCountX):
                    self.xmlAppendSmd(doc, package, str(name), -startX+i*part.pinPitch, -part.length/2.0-part.smdPadOffset+part.smdPadLength/2.0, part.smdPadLength, part.smdPadWidth, angle=90)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.smdPadWidth/2.0), part.length/2.0+part.smdPadOffset, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), part.length/2.0-part.smdPadLength+part.smdPadOffset,29)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.smdPadWidth/2.0), part.length/2.0+part.smdPadOffset, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), part.length/2.0-part.smdPadLength+part.smdPadOffset,31)
                    name += 1
                for i in range(part.pinCountY):
                    self.xmlAppendSmd(doc, package, str(name), part.width/2.0+part.smdPadOffset-part.smdPadLength/2.0, -startY+i*part.pinPitch, part.smdPadLength, part.smdPadWidth, angle=180)
                    self.xmlAppendRectangle(doc, package, part.width/2.0+part.smdPadOffset, -(startY-i*part.pinPitch-part.smdPadWidth/2.0), part.width/2.0-part.smdPadLength+part.smdPadOffset, -(startY-i*part.pinPitch+part.smdPadWidth/2.0),29)
                    self.xmlAppendRectangle(doc, package, part.width/2.0+part.smdPadOffset, -(startY-i*part.pinPitch-part.smdPadWidth/2.0), part.width/2.0-part.smdPadLength+part.smdPadOffset, -(startY-i*part.pinPitch+part.smdPadWidth/2.0),31)
                    name += 1
                for i in range(part.pinCountX):
                    self.xmlAppendSmd(doc, package, str(name), startX-i*part.pinPitch, part.length/2.0+part.smdPadOffset-part.smdPadLength/2.0, part.smdPadLength, part.smdPadWidth, angle=270)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadOffset), -(startX-i*part.pinPitch+part.smdPadWidth/2.0), -(part.length/2.0-part.smdPadLength+part.smdPadOffset),29)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadOffset), -(startX-i*part.pinPitch+part.smdPadWidth/2.0), -(part.length/2.0-part.smdPadLength+part.smdPadOffset),31)
                    name += 1
            else:                           # Pins Outside
                for i in range(part.pinCountY):
                    self.xmlAppendSmd(doc, package, str(name), -part.width/2.0-part.smdPadOffset-part.smdPadLength/2.0, startY-i*part.pinPitch, part.smdPadLength, part.smdPadWidth, angle=0)
                    self.xmlAppendRectangle(doc, package, -(part.width/2.0+part.smdPadOffset), -(startY-i*part.pinPitch+part.smdPadWidth/2.0), -(part.width/2.0+part.smdPadLength+part.smdPadOffset), -(startY-i*part.pinPitch-part.smdPadWidth/2.0),29)
                    self.xmlAppendRectangle(doc, package, -(part.width/2.0+part.smdPadOffset), -(startY-i*part.pinPitch+part.smdPadWidth/2.0), -(part.width/2.0+part.smdPadLength+part.smdPadOffset), -(startY-i*part.pinPitch-part.smdPadWidth/2.0),31)
                    name += 1
                for i in range(part.pinCountX):
                    self.xmlAppendSmd(doc, package, str(name), -startX+i*part.pinPitch, -part.length/2.0-part.smdPadOffset-part.smdPadLength/2.0, part.smdPadLength, part.smdPadWidth, angle=90)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.smdPadWidth/2.0), part.length/2.0+part.smdPadOffset, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), part.length/2.0+part.smdPadLength+part.smdPadOffset,29)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch+part.smdPadWidth/2.0), part.length/2.0+part.smdPadOffset, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), part.length/2.0+part.smdPadLength+part.smdPadOffset,31)
                    name += 1
                for i in range(part.pinCountY):
                    self.xmlAppendSmd(doc, package, str(name), part.width/2.0+part.smdPadOffset+part.smdPadLength/2.0, -startY+i*part.pinPitch, part.smdPadLength, part.smdPadWidth, angle=180)
                    self.xmlAppendRectangle(doc, package, part.width/2.0+part.smdPadOffset, -(startY-i*part.pinPitch-part.smdPadWidth/2.0), part.width/2.0+part.smdPadLength+part.smdPadOffset, -(startY-i*part.pinPitch+part.smdPadWidth/2.0),29)
                    self.xmlAppendRectangle(doc, package, part.width/2.0+part.smdPadOffset, -(startY-i*part.pinPitch-part.smdPadWidth/2.0), part.width/2.0+part.smdPadLength+part.smdPadOffset, -(startY-i*part.pinPitch+part.smdPadWidth/2.0),31)
                    name += 1
                for i in range(part.pinCountX):
                    self.xmlAppendSmd(doc, package, str(name), startX-i*part.pinPitch, part.length/2.0+part.smdPadOffset+part.smdPadLength/2.0, part.smdPadLength, part.smdPadWidth, angle=270)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadOffset), -(startX-i*part.pinPitch+part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadLength+part.smdPadOffset),29)
                    self.xmlAppendRectangle(doc, package, -(startX-i*part.pinPitch-part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadOffset), -(startX-i*part.pinPitch+part.smdPadWidth/2.0), -(part.length/2.0+part.smdPadLength+part.smdPadOffset),31)
                    name += 1


            # Create Thermal Pad
            if (part.thermalPadWidth * part.thermalPadLength != 0):
                self.xmlAppendSmd(doc, package, "pad", 0, 0, part.thermalPadWidth, part.thermalPadLength, angle=0)
                self.xmlAppendRectangle(doc, package, -part.thermalPadWidth/2.0, part.thermalPadLength/2.0, part.thermalPadWidth/2.0, -part.thermalPadLength/2.0, 29)
                # Cream Layer
                self.xmlAppendRectangle(doc, package, -0.6*part.thermalPadWidth/2.0, 0.6*part.thermalPadLength/2.0, 0.6*part.thermalPadWidth/2.0, -0.6*part.thermalPadLength/2.0, 31)

            # Direction Indicator
            self.xmlAppendRectangle(doc, package, -part.width/2.0, part.length/2.0, 0, 0, 51)

            # Print XML
            self.eagle_xml.insert(0.0, doc.toprettyxml(indent=""))

    def xmlAppendWire(self, doc, package, x1, y1, x2, y2, width=0.1, layer=21):
        line = doc.createElement("wire")
        line.setAttribute("x1", str(x1))
        line.setAttribute("y1", str(y1))
        line.setAttribute("x2", str(x2))
        line.setAttribute("y2", str(y2))
        line.setAttribute("width", str(width))
        line.setAttribute("layer", str(layer))
        package.appendChild(line);

    def xmlAppendRectangle(self, doc, package, x1, y1, x2, y2, layer=21):
        rect = doc.createElement("rectangle")
        rect.setAttribute("x1", str(x1))
        rect.setAttribute("y1", str(y1))
        rect.setAttribute("x2", str(x2))
        rect.setAttribute("y2", str(y2))
        rect.setAttribute("layer", str(layer))
        package.appendChild(rect);

    def xmlAppendSmd(self, doc, package, name, x, y, dx, dy, angle, layer=1, stop="no", cream="no"):
        smd = doc.createElement("smd")
        smd.setAttribute("name", name)
        smd.setAttribute("x", str(x))
        smd.setAttribute("y", str(y))
        smd.setAttribute("dx", str(dx))
        smd.setAttribute("dy", str(dy))
        smd.setAttribute("layer", str(layer))
        smd.setAttribute("stop", stop)
        smd.setAttribute("cream", cream)
        smd.setAttribute("rot", "R" + str(angle))
        package.appendChild(smd)

root = Tk()
partUI = Part(DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), IntVar(), IntVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), BooleanVar())

app = App(root)
root.title("Eagle 6 Footprint Generator")
root.minsize(800, 300)

root.mainloop()
