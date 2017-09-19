'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from ToSI import ToSI,FromSI
from ProjectFile import PartPropertyConfiguration

class PartProperty(PartPropertyConfiguration):
    def __init__(self,propertyName,type=None,unit=None,keyword=None,description=None,value=None,hidden=False,visible=False,keywordVisible=True,inProjectFile=True):
        PartPropertyConfiguration.__init__(self)
        self.SetValue('Keyword', keyword)
        self.SetValue('PropertyName',propertyName)
        self.SetValue('Description', description)
        self.SetValue('Value',value)
        self.SetValue('Hidden',hidden)
        self.SetValue('Visible', visible)
        self.SetValue('KeywordVisible', keywordVisible)
        self.SetValue('Type', type)
        self.SetValue('Unit',unit)
        self.SetValue('InProjectFile',inProjectFile)
    def PropertyString(self,stype='raw'):
        if stype=='attr':
            result=''
            if self.GetValue('Visible'):
                if self.GetValue('KeywordVisible'):
                    if self.GetValue('Keyword') != None and self.GetValue('Keyword') != 'None':
                        result=result+self.GetValue('Keyword')+' '
                if self.GetValue('Type')=='string':
                    value = self.GetValue('Value')
                elif self.GetValue('Type')=='file':
                    value=('/'.join(str(self.GetValue('Value')).split('\\'))).split('/')[-1]
                elif self.GetValue('Type')=='int':
                    value = self.GetValue('Value')
                elif self.GetValue('Type')=='float':
                    value = str(ToSI(float(self.GetValue('Value')),self.GetValue('Unit')))
                else:
                    value = str(self.GetValue('Value'))
                result=result+value
            return result
        elif stype == 'raw':
            if self.GetValue('Type')=='string':
                value = self.GetValue('Value')
            elif self.GetValue('Type')=='file':
                value = self.GetValue('Value')
            elif self.GetValue('Type')=='int':
                value = self.GetValue('Value')
            elif self.GetValue('Type')=='float':
                value = str(float(self.GetValue('Value')))
            else:
                value = str(self.GetValue('Value'))
            return value
        elif stype == 'entry':
            if self.GetValue('Type')=='string':
                value = str(self.GetValue('Value'))
            elif self.GetValue('Type')=='file':
                value = str(self.GetValue('Value'))
            elif self.GetValue('Type')=='int':
                value = str(self.GetValue('Value'))
            elif self.GetValue('Type')=='float':
                value = str(ToSI(float(self.GetValue('Value')),self.GetValue('Unit')))
            else:
                value = str(self.GetValue('Value'))
            return value
        else:
            raise ValueError
            return str(self.GetValue('Value'))
    def SetValueFromString(self,string):
        if self.GetValue('Type')=='string':
            self.SetValue('Value', str(string))
        elif self.GetValue('Type')=='file':
            self.SetValue('Value',str(string))
        elif self.GetValue('Type')=='int':
            try:
                self.SetValue('Value',int(string))
            except ValueError:
                self.SetValue('Value',0)
        elif self.GetValue('Type')=='float':
            value = FromSI(string,self.GetValue('Unit'))
            if value is not None:
                self.SetValue('Value',value)
        else:
            raise ValueError
            self.SetValue('Value', str(string))
        return self
    def GetValue(self,name=None):
        if not name is None:
            return PartPropertyConfiguration.GetValue(self,name)

        if self.GetValue('Type')=='int':
            return int(self.GetValue('Value'))
        elif self.GetValue('Type')=='float':
            return float(self.GetValue('Value'))
        else:
            return self.GetValue('Value')

class PartPropertyXMLClassFactory(PartProperty):
    def __init__(self,xml):
        propertyName=''
        keyword=None
        description=None
        value=None
        hidden=False
        visible=False
        ptype='string'
        unit=None
        keywordVisible=False
        for item in xml:
            if item.tag == 'keyword':
                keyword = item.text
            elif item.tag == 'property_name':
                propertyName = item.text
                # this fixes a misspelling I corrected but breaks
                # lots of old projects
                if propertyName == 'resistence':
                    propertyName = 'resistance'
                if propertyName == 'Resistance':
                    propertyName = 'resistance'
            elif item.tag == 'description':
                description = item.text
            elif item.tag == 'value':
                value = item.text
            elif item.tag == 'hidden':
                hidden = eval(item.text)
            elif item.tag == 'visible':
                visible = eval(item.text)
            elif item.tag == 'keyword_visible':
                keywordVisible = eval(item.text)
            elif item.tag == 'type':
                ptype = item.text
            elif item.tag == 'unit':
                unit = item.text
        # legacy change - all part properties must have keywords
        if propertyName == 'portnumber':
            keyword='pn'
            keywordVisible=False
        elif propertyName == 'reference':
            keyword='ref'
            keywordVisible=False
        elif propertyName == 'defaultreference':
            keyword='defref'
            keywordVisible=False
        elif propertyName == 'ports':
            keyword='ports'
            keywordVisible=False
        elif propertyName == 'filename':
            keyword='file'
            keywordVisible=False
        elif propertyName == 'type':
            keyword='partname'
            keywordVisible=False
        elif propertyName == 'category':
            keyword='cat'
            keywordVisible=False
        elif propertyName == 'description':
            keyword='desc'
            keywordVisible=False
        elif propertyName == 'waveformfilename':
            keyword='wffile'
            keywordVisible=False

        if keyword is None:
            raise
        # hack because stupid xml outputs none for empty string
        if ptype == 'float' and (unit is None or unit == 'None'):
            unit = ''
        self.result=PartProperty(propertyName,ptype,unit,keyword,description,value,hidden,visible,keywordVisible)

class PartPropertyFromProject(PartProperty):
    def __init__(self,partPropertyProject):
        propertyName=partPropertyProject.GetValue('PropertyName')
        keyword=partPropertyProject.GetValue('Keyword')
        description=partPropertyProject.GetValue('Description')
        value=partPropertyProject.GetValue('Value')
        hidden=partPropertyProject.GetValue('Hidden')
        visible=partPropertyProject.GetValue('Visible')
        ptype=partPropertyProject.GetValue('Type')
        unit=partPropertyProject.GetValue('Unit')
        keywordVisible=partPropertyProject.GetValue('KeywordVisible')
        inProjectFile=partPropertyProject.GetValue('InProjectFile')
        # hack because stupid xml outputs none for empty string
        if ptype == 'float' and (unit is None or unit == 'None'):
            unit = ''
        self.result=PartProperty(propertyName,ptype,unit,keyword,description,value,hidden,visible,keywordVisible,inProjectFile)

class PartPropertyReadOnly(PartProperty):
    def __init__(self,propertyName,type=None,unit=None,keyword=None,description=None,value=None,hidden=False,visible=False,keywordVisible=True):
        inProjectFile=False
        PartProperty.__init__(self,propertyName,type,unit,keyword,description,value,hidden,visible,keywordVisible,inProjectFile)

class PartPropertyPortNumber(PartProperty):
    def __init__(self,portNumber):
        PartProperty.__init__(self,'portnumber',type='int',unit=None,keyword='pn',description='port number',value=portNumber,visible=True, keywordVisible=False)

class PartPropertyReferenceDesignator(PartProperty):
    def __init__(self,referenceDesignator=''):
        PartProperty.__init__(self,'reference',type='string',unit=None,keyword='ref',description='reference designator',value=referenceDesignator,visible=False,keywordVisible=False)

class PartPropertyDefaultReferenceDesignator(PartPropertyReadOnly):
    def __init__(self,referenceDesignator=''):
        PartPropertyReadOnly.__init__(self,'defaultreference',type='string',unit=None,keyword='defref',description='default reference designator',value=referenceDesignator,hidden=True,visible=False,keywordVisible=False)

class PartPropertyPorts(PartProperty):
    def __init__(self,numPorts=1,hidden=True):
        PartProperty.__init__(self,'ports',type='int',unit=None,description='ports',keyword='ports',value=numPorts,hidden=hidden)

class PartPropertyFileName(PartProperty):
    def __init__(self,fileName=''):
        PartProperty.__init__(self,'filename',type='file',unit=None,keyword='file',description='file name',value=fileName)

class PartPropertyWaveformFileName(PartProperty):
    def __init__(self,fileName=''):
        PartProperty.__init__(self,'waveformfilename',type='file',unit=None,keyword='wffile',description='file name',value=fileName)

class PartPropertyResistance(PartProperty):
    def __init__(self,resistance=50.,keyword='r',descriptionPrefix=''):
        PartProperty.__init__(self,'resistance',type='float',unit='Ohm',keyword=keyword,description=descriptionPrefix+'resistance (Ohms)',value=resistance,visible=True,keywordVisible=False)

class PartPropertyCapacitance(PartProperty):
    def __init__(self,capacitance=1e-12,keyword='c',descriptionPrefix=''):
        PartProperty.__init__(self,'capacitance',type='float',unit='F',keyword=keyword,description=descriptionPrefix+'capacitance (F)',value=capacitance,visible=True,keywordVisible=False)

class PartPropertyInductance(PartProperty):
    def __init__(self,inductance=1e-9,keyword='l',descriptionPrefix=''):
        PartProperty.__init__(self,'inductance',type='float',unit='H',keyword=keyword,description=descriptionPrefix+'inductance (H)',value=inductance,visible=True,keywordVisible=False)

class PartPropertyConductance(PartProperty):
    def __init__(self,conductance=0.,keyword='g',descriptionPrefix=''):
        PartProperty.__init__(self,'conductance',type='float',unit='S',keyword=keyword,description=descriptionPrefix+'conductance (S)',value=conductance,visible=True,keywordVisible=False)

class PartPropertyPartName(PartPropertyReadOnly):
    def __init__(self,partName=''):
        PartPropertyReadOnly.__init__(self,'type',type='string',unit=None,keyword='partname',description='part type',value=partName,hidden=True)

class PartPropertyCategory(PartPropertyReadOnly):
    def __init__(self,category=''):
        PartPropertyReadOnly.__init__(self,'category',type='string',unit=None,keyword='cat',description='part category',value=category,hidden=True)

class PartPropertyDescription(PartPropertyReadOnly):
    def __init__(self,description=''):
        PartPropertyReadOnly.__init__(self,'description',type='string',unit=None,keyword='desc',description='part description',value=description,hidden=True)

class PartPropertyVoltageGain(PartProperty):
    def __init__(self,voltageGain=1.0):
        PartProperty.__init__(self,'gain',type='float',unit='',keyword='gain',description='voltage gain (V/V)',value=voltageGain,visible=True)

class PartPropertyCurrentGain(PartProperty):
    def __init__(self,currentGain=1.0):
        PartProperty.__init__(self,'gain',type='float',unit='',keyword='gain',description='current gain (A/A)',value=currentGain,visible=True)

class PartPropertyTransconductance(PartProperty):
    def __init__(self,transconductance=1.0):
        PartProperty.__init__(self,'transconductance',type='float',unit='A/V',keyword='gain',description='transconductance (A/V)',value=transconductance,visible=True)

class PartPropertyTransresistance(PartProperty):
    def __init__(self,transresistance=1.0):
        PartProperty.__init__(self,'transresistance',type='float',unit='V/A',keyword='gain',description='transresistance (V/A)',value=transresistance,visible=True)

class PartPropertyInputImpedance(PartProperty):
    def __init__(self,inputImpedance=1e8):
        PartProperty.__init__(self,'inputimpedance',type='float',unit='Ohm',keyword='zi',description='input impedance (Ohms)',value=inputImpedance,visible=True)

class PartPropertyOutputImpedance(PartProperty):
    def __init__(self,outputImpedance=0.):
        PartProperty.__init__(self,'outputimpedance',type='float',unit='Ohm',keyword='zo',description='output impedance (Ohms)',value=outputImpedance,visible=True)

class PartPropertyHorizontalOffset(PartProperty):
    def __init__(self,horizontalOffset=-100e-9):
        PartProperty.__init__(self,'horizontaloffset',type='float',unit='s',keyword='ho',description='horizontal offset (s)',value=horizontalOffset,visible=False)

class PartPropertyDuration(PartProperty):
    def __init__(self,duration=200e-9):
        PartProperty.__init__(self,'duration',type='float',unit='s',keyword='dur',description='duration (s)',value=duration,visible=False)

class PartPropertySampleRate(PartProperty):
    def __init__(self,sampleRate=40e9):
        PartProperty.__init__(self,'sampleRate',type='float',unit='S/s',keyword='fs',description='Sample Rate (S/s)',value=sampleRate,visible=False)

class PartPropertyStartTime(PartProperty):
    def __init__(self,startTime=0.):
        PartProperty.__init__(self,'starttime',type='float',unit='s',keyword='t0',description='start time (s)',value=startTime,visible=True)

class PartPropertyVoltageAmplitude(PartProperty):
    def __init__(self,voltageAmplitude=1.):
        PartProperty.__init__(self,'voltageamplitude',type='float',unit='V',keyword='a',description='voltage amplitude (V)',value=voltageAmplitude,visible=True)

class PartPropertyVoltageRms(PartProperty):
    def __init__(self,voltagerms=0.):
        PartProperty.__init__(self,'voltagerms',type='float',unit='Vrms',keyword='vrms',description='voltage (Vrms)',value=voltagerms,visible=True)

class PartPropertyCurrentAmplitude(PartProperty):
    def __init__(self,currentAmplitude=1.):
        PartProperty.__init__(self,'currentamplitude',type='float',unit='A',keyword='a',description='current amplitude (A)',value=currentAmplitude,visible=True)

class PartPropertyPulseWidth(PartProperty):
    def __init__(self,pulseWidth=1e-9):
        PartProperty.__init__(self,'pulsewidth',type='float',unit='s',keyword='w',description='pulse width (s)',value=pulseWidth,visible=True)

class PartPropertyFrequency(PartProperty):
    def __init__(self,frequency=1e6):
        PartProperty.__init__(self,'frequency',type='float',unit='Hz',keyword='f',description='frequency (Hz)',value=frequency,visible=True)

class PartPropertyPhase(PartProperty):
    def __init__(self,phase=0.):
        PartProperty.__init__(self,'phase',type='float',unit='deg',keyword='ph',description='phase (degrees)',value=phase,visible=True)

class PartPropertyTurnsRatio(PartProperty):
    def __init__(self,ratio=1.):
        PartProperty.__init__(self,'turnsratio',type='float',unit='',keyword='tr',description='turns ratio (S/P)',value=ratio,visible=True,keywordVisible=False)

class PartPropertyVoltageOffset(PartProperty):
    def __init__(self,voltageOffset=0.0):
        PartProperty.__init__(self,'offset',type='float',unit='V',keyword='offset',description='voltage offset (V)',value=voltageOffset,visible=True)

class PartPropertyDelay(PartProperty):
    def __init__(self,delay=0.0):
        PartProperty.__init__(self,'delay',type='float',unit='s',keyword='td',description='delay (s)',value=delay,visible=True)

class PartPropertyCharacteristicImpedance(PartProperty):
    def __init__(self,characteristicImpedance=50.):
        PartProperty.__init__(self,'characteristicimpedance',type='float',unit='Ohm',keyword='zc',description='characteristic impedance (Ohms)',value=characteristicImpedance,visible=True)

class PartPropertySections(PartProperty):
    def __init__(self,sections=1):
        PartProperty.__init__(self,'sections',type='int',unit='',keyword='sect',description='sections',value=sections,visible=True,keywordVisible=False)

class PartPropertyWeight(PartProperty):
    def __init__(self,weight=1.0):
        PartProperty.__init__(self,'weight',type='float',unit='',keyword='weight',description='weight',value=weight,visible=False)

class PartPropertyReferenceImpedance(PartProperty):
    def __init__(self,impedance=50.,keyword='z0',):
        PartProperty.__init__(self,'impedance',type='float',unit='Ohm',keyword=keyword,description='reference impedance (Ohms)',value=impedance,visible=True,keywordVisible=True)
