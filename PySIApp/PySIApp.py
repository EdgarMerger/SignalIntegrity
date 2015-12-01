from Tkinter import *

from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from tkFileDialog import askdirectory
import tkMessageBox
import copy
import os

#from idlelib.ToolTip import *

from PartPin import *
from PartPicture import *
from PartProperty import *
from Device import *
from DeviceProperties import *
from DevicePicker import *
from Schematic import *
from PlotWindow import *
from CalculationProperties import *
from Simulator import *
from NetList import *
from SParameterViewerWindow import *
from Files import *
from History import *

class TheMenu(Menu):
    def __init__(self,parent):
        self.parent=parent
        Menu.__init__(self,self.parent.root)
        self.parent.root.config(menu=self)
        self.FileMenu=Menu(self)
        self.add_cascade(label='File',menu=self.FileMenu)
        self.FileMenu.add_command(label="Open Project",command=self.parent.onReadProjectFromFile)
        self.FileMenu.add_command(label="Save Project",command=self.parent.onWriteProjectToFile)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Clear Schematic",command=self.parent.onClearSchematic)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Export NetList",command=self.parent.onExportNetlist)
        self.FileMenu.add_command(label="Export LaTeX (TikZ)",command=self.parent.onExportTpX)

        self.EditMenu=Menu(self)
        self.add_cascade(label='Edit',menu=self.EditMenu)
        self.EditMenu.add_command(label="Undo",command=self.parent.onUndo)
        self.EditMenu.add_command(label="Redo",command=self.parent.onRedo)
        self.EditMenu.add_separator()

        self.PartsMenu=Menu(self)
        self.add_cascade(label='Parts',menu=self.PartsMenu)
        self.PartsMenu.add_command(label='Add Part',command=self.parent.onAddPart)
        self.PartsMenu.add_command(label='Add Port',command=self.parent.onAddPort)
        self.PartsMenu.add_separator()
        self.PartsMenu.add_command(label='Delete Part',command=self.parent.onDeletePart)
        self.PartsMenu.add_separator()
        self.PartsMenu.add_command(label='Edit Properties',command=self.parent.onEditProperties)
        self.PartsMenu.add_command(label='Duplicate Part',command=self.parent.onDuplicate)
        self.PartsMenu.add_command(label='Rotate Part',command=self.parent.onRotatePart)
        self.PartsMenu.add_command(label='Flip Horizontally',command=self.parent.onFlipPartHorizontally)
        self.PartsMenu.add_command(label='Flip Vertically',command=self.parent.onFlipPartVertically)

        self.WireMenu=Menu(self)
        self.add_cascade(label='Wires',menu=self.WireMenu)
        self.WireMenu.add_command(label='Add Wire',command=self.parent.onAddWire)
        self.WireMenu.add_separator()
        self.WireMenu.add_command(label='Delete Vertex',command=self.parent.onDeleteSelectedVertex)
        self.WireMenu.add_command(label='Duplicate Vertex',command=self.parent.onDuplicateSelectedVertex)
        self.WireMenu.add_command(label='Delete Wire',command=self.parent.onDeleteSelectedWire)

        self.ViewMenu=Menu(self)
        self.add_cascade(label='View',menu=self.ViewMenu)
        self.ViewMenu.add_command(label='Zoom In',command=self.parent.onZoomIn)
        self.ViewMenu.add_command(label='Zoom Out',command=self.parent.onZoomOut)
        self.ViewMenu.add_command(label='Pan',command=self.parent.onPan)

        self.CalcMenu=Menu(self)
        self.add_cascade(label='Calculate',menu=self.CalcMenu)
        self.CalcMenu.add_command(label='Calculation Properties',command=self.parent.onCalculationProperties)
        self.CalcMenu.add_command(label='S-parameter Viewer',command=self.parent.onSParameterViewer)
        self.CalcMenu.add_separator()
        self.CalcMenu.add_command(label='Calculate S-parameters',command=self.parent.onCalculateSParameters)
        self.CalcMenu.add_command(label='Simulate',command=self.parent.onSimulate)

class ToolBar(Frame):
    def __init__(self,parent):
        self.parent=parent
        Frame.__init__(self,self.parent)
        self.pack(side=TOP,fill=X,expand=NO)
        filesFrame=self
        self.newProjectButtonIcon = PhotoImage(file='./icons/png/16x16/actions/document-new-3.gif')
        self.newProjectButton = Button(filesFrame,command=self.parent.onClearSchematic,image=self.newProjectButtonIcon)
        self.newProjectButton.pack(side=LEFT,fill=NONE,expand=NO)
        #ToolTip(self.newProjectButton, 'New Project')
        self.openProjectButtonIcon = PhotoImage(file='./icons/png/16x16/actions/document-open-2.gif')
        self.openProjectButton = Button(filesFrame,command=self.parent.onReadProjectFromFile,image=self.openProjectButtonIcon)
        self.openProjectButton.pack(side=LEFT,fill=NONE,expand=NO)
        #ToolTip(self.openProjectButton, 'Open Project')
        self.saveProjectButtonIcon = PhotoImage(file='./icons/png/16x16/actions/document-save-2.gif')
        self.saveProjectButton = Button(filesFrame,command=self.parent.onWriteProjectToFile,image=self.saveProjectButtonIcon)
        self.saveProjectButton.pack(side=LEFT,fill=NONE,expand=NO)
        #ToolTip(self.saveProjectButton, 'Save Project')
        separator=Frame(self,bd=2,relief=SUNKEN)
        separator.pack(side=LEFT,fill=X,padx=5,pady=5)
        editFrame=self
        self.addPartButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-add-2.gif')
        self.addPartButton = Button(editFrame,command=self.parent.onAddPart,image=self.addPartButtonIcon)
        self.addPartButton.pack(side=LEFT,fill=NONE,expand=NO)
        #ToolTip(self.addPartButton, 'Add Part')
        self.deletePartButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-delete-6.gif')
        self.deletePartButton = Button(editFrame,command=self.parent.onDeleteSelected,image=self.deletePartButtonIcon)
        self.deletePartButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.addWireButtonIcon = PhotoImage(file='./icons/png/16x16/actions/draw-line-3.gif')
        self.addWireButton = Button(editFrame,command=self.parent.onAddWire,image=self.addWireButtonIcon)
        self.addWireButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.duplicatePartButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-copy-3.gif')
        self.duplicatePartButton = Button(editFrame,command=self.parent.onDuplicateSelected,image=self.duplicatePartButtonIcon)
        self.duplicatePartButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.rotatePartButtonIcon = PhotoImage(file='./icons/png/16x16/actions/object-rotate-left-4.gif')
        self.rotatePartButton = Button(editFrame,command=self.parent.onRotatePart,image=self.rotatePartButtonIcon)
        self.rotatePartButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.flipPartHorizontallyButtonIcon = PhotoImage(file='./icons/png/16x16/actions/object-flip-horizontal-3.gif')
        self.flipPartHorizontallyButton = Button(editFrame,command=self.parent.onFlipPartHorizontally,image=self.flipPartHorizontallyButtonIcon)
        self.flipPartHorizontallyButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.flipPartVerticallyButtonIcon = PhotoImage(file='./icons/png/16x16/actions/object-flip-vertical-3.gif')
        self.flipPartVerticallyButton = Button(editFrame,command=self.parent.onFlipPartVertically,image=self.flipPartVerticallyButtonIcon)
        self.flipPartVerticallyButton.pack(side=LEFT,fill=NONE,expand=NO)
        separator=Frame(self,height=2,bd=2,relief=RAISED).pack(side=LEFT,fill=X,padx=5,pady=5)
        self.zoomInButtonIcon = PhotoImage(file='./icons/png/16x16/actions/zoom-in-3.gif')
        self.zoomInButton = Button(editFrame,command=self.parent.onZoomIn,image=self.zoomInButtonIcon)
        self.zoomInButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.zoomOutButtonIcon = PhotoImage(file='./icons/png/16x16/actions/zoom-out-3.gif')
        self.zoomOutButton = Button(editFrame,command=self.parent.onZoomOut,image=self.zoomOutButtonIcon)
        self.zoomOutButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.panButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-move.gif')
        self.panButton = Button(editFrame,command=self.parent.onPan,image=self.panButtonIcon)
        self.panButton.pack(side=LEFT,fill=NONE,expand=NO)
        separator=Frame(self,height=2,bd=2,relief=RAISED).pack(side=LEFT,fill=X,padx=5,pady=5)
        self.calcPropertiesButtonIcon = PhotoImage(file='./icons/png/16x16/actions/tooloptions.gif')
        self.calcPropertiesButton = Button(editFrame,command=self.parent.onCalculationProperties,image=self.calcPropertiesButtonIcon)
        self.calcPropertiesButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.calculateButtonIcon = PhotoImage(file='./icons/png/16x16/actions/system-run-3.gif')
        self.calculateButton = Button(editFrame,command=self.parent.onCalculate,image=self.calculateButtonIcon)
        self.calculateButton.pack(side=LEFT,fill=NONE,expand=NO)

        undoFrame=Frame(self)
        undoFrame.pack(side=RIGHT,fill=NONE,expand=NO,anchor=E)
        self.undoButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-undo-3.gif')
        self.undoButton = Button(undoFrame,command=self.parent.onUndo,image=self.undoButtonIcon)
        self.undoButton.pack(side=LEFT,fill=NONE,expand=NO,anchor=E)
        self.redoButtonIcon = PhotoImage(file='./icons/png/16x16/actions/edit-redo-3.gif')
        self.redoButton = Button(undoFrame,command=self.parent.onRedo,image=self.redoButtonIcon)
        self.redoButton.pack(side=LEFT,fill=NONE,expand=NO,anchor=E)

class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class TheApp(Frame):
    def __init__(self):
        self.root = Tk()
        Frame.__init__(self, self.root)
        self.pack(fill=BOTH, expand=YES)

        self.root.title("PySI")

        img = PhotoImage(file='./icons/png/AppIcon2.gif')
        self.root.tk.call('wm', 'iconphoto', self.root._w, '-default', img)

        sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
        foundSignalIntegrity=False
        while not foundSignalIntegrity:
            foundSignalIntegrity = True
            try:
                import SignalIntegrity as si
            except ImportError:
                foundSignalIntegrity = False
                if tkMessageBox.askokcancel('SignalIntegrity Package',
                    'In order to run this application, I need to know where the '+\
                    'SignalIntegrity package is.  Please browse to the directory where '+\
                    'it\'s installed.\n'+'You should only need to do this once'):
                        dirname = askdirectory(parent=self.root,initialdir=os.path.dirname(os.path.abspath(__file__)),
                            title='Please select a directory')
                        sys.path.append(dirname)
                else:
                    exit()

        self.statusbar=StatusBar(self)

        self.menu=TheMenu(self)
        self.toolbar=ToolBar(self)

        self.Drawing=Drawing(self)
        self.Drawing.pack(side=TOP,fill=BOTH,expand=YES)

        self.statusbar.pack(side=BOTTOM,fill=X,expand=NO)
        self.root.bind('<Key>',self.onKey)

        self.simulator = Simulator(self)
        self.calculationProperties=CalculationProperties(self)
        self.filename=None

        self.history=History(self)

        self.root.mainloop()

    def onKey(self,event):
#       print "pressed", repr(event.keycode), repr(event.keysym)
        if event.keysym == 'Delete': # delete
            self.Drawing.DeleteSelected()

    def onUndo(self):
        self.history.Undo()
        self.Drawing.DrawSchematic()

    def onRedo(self):
        self.history.Redo()
        self.Drawing.DrawSchematic()

    def onReadProjectFromFile(self):
        self.Drawing.stateMachine.Nothing()
        extension='.xml'
        filename=askopenfilename(filetypes=[('xml', extension)])
        if filename == '':
            return
        filenametokens=filename.split('.')
        if len(filenametokens)==0:
            return
        if len(filenametokens)==1:
            filename=filename+extension
        filename=ConvertFileNameToRelativePath(filename)
        tree=et.parse(filename)
        root=tree.getroot()
        for child in root:
            if child.tag == 'drawing':
                self.Drawing.InitFromXml(child)
            elif child.tag == 'calculation_properties':
                self.calculationProperties.InitFromXml(child, self)
        self.filename=filename
        self.Drawing.DrawSchematic()
        self.history.Event('read project')

    def onWriteProjectToFile(self):
        self.Drawing.stateMachine.Nothing()
        extension='.xml'
        if self.filename == None:
            filename=asksaveasfilename(filetypes=[('xml', extension)],defaultextension='.xml',initialdir=os.getcwd())
        else:
            filename=asksaveasfilename(filetypes=[('xml', extension)],defaultextension='.xml',initialfile=self.filename)
        if filename=='':
            return
        self.filename=filename
        projectElement=et.Element('Project')
        drawingElement=self.Drawing.xml()
        calculationPropertiesElement=self.calculationProperties.xml()
        projectElement.extend([drawingElement,calculationPropertiesElement])
        et.ElementTree(projectElement).write(filename)

    def onClearSchematic(self):
        self.Drawing.stateMachine.Nothing()
        self.Drawing.schematic.Clear()
        self.history.Event('new project')
        self.Drawing.DrawSchematic()
        self.filename=None

    def onExportNetlist(self):
        self.Drawing.stateMachine.Nothing()
        nld = NetListDialog(self,self.Drawing.schematic.NetList().Text())

    def onExportTpX(self):
        from TpX import TpX
        from TikZ import TikZ
        self.Drawing.stateMachine.Nothing()
        extension='.TpX'
        if self.filename == None:
            filename=asksaveasfilename(filetypes=[('tpx', extension)],defaultextension='.TpX',initialdir=os.getcwd())
        else:
            filename=asksaveasfilename(filetypes=[('tpx', extension)],defaultextension='.TpX',initialfile=self.filename.replace('.xml','.TpX'))
        if filename=='':
            return
        try:
            tpx=self.Drawing.DrawSchematic(TpX()).Finish()
            tikz=self.Drawing.DrawSchematic(TikZ()).Finish()
            #tikz.Document()
            tpx.lineList=tpx.lineList+tikz.lineList
            tpx.WriteToFile(filename)
        except:
            tkMessageBox.showerror('Export LaTeX','LaTeX could not be generated or written ')

    def onAddPart(self):
        self.Drawing.stateMachine.Nothing()
        dpd=DevicePickerDialog(self)
        if dpd.result != None:
            devicePicked=copy.deepcopy(DeviceList[dpd.result])
            devicePicked.AddPartProperty(PartPropertyReferenceDesignator(''))
            defaultProperty = devicePicked[PartPropertyDefaultReferenceDesignator().propertyName]
            if defaultProperty != None:
                defaultPropertyValue = defaultProperty.GetValue()
                uniqueReferenceDesignator = self.Drawing.schematic.NewUniqueReferenceDesignator(defaultPropertyValue)
                if uniqueReferenceDesignator != None:
                    devicePicked[PartPropertyReferenceDesignator().propertyName].SetValueFromString(uniqueReferenceDesignator)
            dpe=DevicePropertiesDialog(self,devicePicked)
            if dpe.result != None:
                self.Drawing.partLoaded = dpe.result
                self.Drawing.stateMachine.PartLoaded()
    def onDeletePart(self):
        self.Drawing.DeleteSelectedDevice()
    def onDeleteSelected(self):
        self.Drawing.DeleteSelected()
    def onEditProperties(self):
        self.Drawing.EditSelectedDevice()
    def onRotatePart(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            self.Drawing.deviceSelected.partPicture.current.Rotate()
            self.Drawing.DrawSchematic()
    def onFlipPartHorizontally(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            orientation = self.Drawing.deviceSelected.partPicture.current.orientation
            mirroredHorizontally = self.Drawing.deviceSelected.partPicture.current.mirroredHorizontally
            mirroredVertically = self.Drawing.deviceSelected.partPicture.current.mirroredVertically
            self.Drawing.deviceSelected.partPicture.current.ApplyOrientation(orientation,not mirroredHorizontally,mirroredVertically)
            self.Drawing.DrawSchematic()
    def onFlipPartVertically(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            orientation = self.Drawing.deviceSelected.partPicture.current.orientation
            mirroredHorizontally = self.Drawing.deviceSelected.partPicture.current.mirroredHorizontally
            mirroredVertically = self.Drawing.deviceSelected.partPicture.current.mirroredVertically
            self.Drawing.deviceSelected.partPicture.current.ApplyOrientation(orientation,mirroredHorizontally,not mirroredVertically)
            self.Drawing.DrawSchematic()
    def onDuplicateSelected(self):
        self.Drawing.DuplicateSelected()
    def onDuplicate(self):
        self.Drawing.DuplicateSelectedDevice()
    def onAddWire(self):
        self.Drawing.wireLoaded=Wire([Vertex((0,0))])
        self.Drawing.schematic.wireList.append(self.Drawing.wireLoaded)
        self.Drawing.stateMachine.WireLoaded()
    def onAddPort(self):
        self.Drawing.stateMachine.Nothing()
        portNumber=1
        for device in self.Drawing.schematic.deviceList:
            if device['type'].GetValue() == 'Port':
                if portNumber <= int(device['portnumber'].GetValue()):
                    portNumber = int(device['portnumber'].GetValue())+1
        dpe=DevicePropertiesDialog(self,Port(portNumber))
        if dpe.result != None:
            self.Drawing.partLoaded = dpe.result
            self.Drawing.stateMachine.PartLoaded()

    def onZoomIn(self):
        self.Drawing.grid = self.Drawing.grid*2
        self.Drawing.DrawSchematic()

    def onZoomOut(self):
        self.Drawing.grid = max(1,self.Drawing.grid/2)
        self.Drawing.DrawSchematic()

    def onPan(self):
        self.Drawing.stateMachine.Panning()

    def onDeleteSelectedVertex(self):
        self.Drawing.DeleteSelectedVertex()

    def onDuplicateSelectedVertex(self):
        self.Drawing.DuplicateSelectedVertex()

    def onDeleteSelectedWire(self):
        self.Drawing.DeleteSelectedWire()

    def onCalculateSParameters(self):
        #self.onCalculationProperties()
        self.Drawing.stateMachine.Nothing()
        netList=self.Drawing.schematic.NetList().Text()
        import SignalIntegrity as si
        spnp=si.p.SystemSParametersNumericParser(
            si.fd.EvenlySpacedFrequencyList(
                self.calculationProperties.endFrequency,
                self.calculationProperties.frequencyPoints))
        spnp.AddLines(netList)
        try:
            sp=spnp.SParameters()
        except si.PySIException as e:
            if e == si.PySIExceptionCheckConnections:
                tkMessageBox.showerror('S-parameter Calculator','Unconnected devices error: '+e.message)
            elif e == si.PySIExceptionSParameterFile:
                tkMessageBox.showerror('S-parameter Calculator','s-parameter file error: '+e.message)
            elif e == si.PySIExceptionNumeric:
                tkMessageBox.showerror('S-parameter Calculator','S-parameter Calculator Numerical Error: '+e.message)
            elif e == si.PySIExceptionSystemDescriptionBuildError:
                tkMessageBox.showerror('S-parameter Calculator','Schematic Error: '+e.message)
            else:
                tkMessageBox.showerror('S-parameter Calculator','Unhandled PySI Exception: '+str(e)+' '+e.message)
            return
        SParametersDialog(self,sp)

    def onCalculationProperties(self):
        self.Drawing.stateMachine.Nothing()
        self.calculationProperties.ShowCalculationPropertiesDialog()

    def onSimulate(self):
        self.Drawing.stateMachine.Nothing()
        self.simulator.Simulate()

    def onCalculate(self):
        self.Drawing.stateMachine.Nothing()
        foundAPort=False
        foundASource=False
        foundAnOutput=False
        for deviceIndex in range(len(self.Drawing.schematic.deviceList)):
            device = self.Drawing.schematic.deviceList[deviceIndex]
            deviceType = device['type'].GetValue()
            if  deviceType == 'Port':
                foundAPort = True
            elif deviceType == 'Output':
                foundAnOutput = True
            else:
                netListLine = device.NetListLine()
                if not netListLine is None:
                    firstToken=netListLine.strip().split(' ')[0]
                    if firstToken == 'voltagesource':
                        foundASource = True
                    elif firstToken == 'currentsource':
                        foundASource = True
        canSimulate = foundASource and foundAnOutput and not foundAPort
        canCalculateSParameters = foundAPort and not foundAnOutput
        canCalculate = canSimulate or canCalculateSParameters
        if canCalculate:
            if canSimulate:
                self.onSimulate()
            elif canCalculateSParameters:
                self.onCalculateSParameters()

    def onSParameterViewer(self):
        import SignalIntegrity as si
        filetypes = [('s-parameter files', ('*.s*p'))]
        filename=askopenfilename(filetypes=filetypes,parent=self)
        if filename == '':
            return
        filenametokens=filename.split('.')
        if len(filenametokens)==0:
            return

        filename=ConvertFileNameToRelativePath(filename)
        sp=si.sp.File(filename)
        SParametersDialog(self,sp)

def main():
    app=TheApp()

if __name__ == '__main__':
    main()