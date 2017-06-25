'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from CalculationPropertiesProject import PropertiesDialog,CalculationPropertySI,CalculationProperty
from ToSI import nextHigher12458

class CalculationPropertiesDialog(PropertiesDialog):
    def __init__(self,parent):
        PropertiesDialog.__init__(self,parent,parent.project,parent,'Calculation Properties')
        self.endFrequencyFrame=CalculationPropertySI(self.propertyListFrame,'End Frequency',self.onendFrequencyEntered,None,self.project,'CalculationProperties.EndFrequency','Hz')
        self.frequencyPointsFrame=CalculationProperty(self.propertyListFrame,'Frequency Points',self.onfrequencyPointsEntered,None,self.project,'CalculationProperties.FrequencyPoints')
        self.frequencyResolutionFrame=CalculationPropertySI(self.propertyListFrame,'Frequency Resolution',self.onfrequencyResolutionEntered,None,self.project,'CalculationProperties.FrequencyResolution','Hz')
        self.userSampleRateFrame=CalculationPropertySI(self.propertyListFrame,'User Sample Rate',self.onuserSampleRateEntered,None,self.project,'CalculationProperties.UserSampleRate','S/s')
        self.baseSampleRateFrame=CalculationPropertySI(self.propertyListFrame,'Base Sample Rate',self.onbaseSampleRateEntered,None,self.project,'CalculationProperties.BaseSampleRate','S/s')
        self.timePointsFrame=CalculationProperty(self.propertyListFrame,'Time Points',self.ontimePointsEntered,None,self.project,'CalculationProperties.TimePoints')
        self.impulseResponseLengthFrame=CalculationPropertySI(self.propertyListFrame,'Impulse Response Length',self.onimpulseLengthEntered,None,self.project,'CalculationProperties.ImpulseResponseLength','s')  
        self.Finish()

    def onendFrequencyEntered(self,event):
        self.project.SetValue('CalculationProperties.EndFrequency',nextHigher12458(self.project.GetValue('CalculationProperties.EndFrequency')))
        self.project.SetValue('CalculationProperties.BaseSampleRate',2*self.project.GetValue('CalculationProperties.EndFrequency'))
        self.project.SetValue('CalculationProperties.FrequencyPoints',int(nextHigher12458(self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyResolution'))))
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def onfrequencyPointsEntered(self,event):
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def onfrequencyResolutionEntered(self,event):
        self.project.SetValue('CalculationProperties.FrequencyPoints',int(nextHigher12458(self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyResolution'))))
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def onuserSampleRateEntered(self,event):
        self.project.SetValue('CalculationProperties.UserSampleRate',nextHigher12458(self.project.GetValue('CalculationProperties.UserSampleRate')))
        self.UpdateStrings()

    def onbaseSampleRateEntered(self,event):
        self.project.SetValue('CalculationProperties.EndFrequency',nextHigher12458(self.project.GetValue('CalculationProperties.BaseSampleRate')*2.))
        self.project.SetValue('CalculationProperties.BaseSampleRate',2*self.project.GetValue('CalculationProperties.EndFrequency'))
        self.project.SetValue('CalculationProperties.FrequencyPoints',int(nextHigher12458(self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyResolution'))))
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def ontimePointsEntered(self,event):
        self.project.SetValue('CalculationProperties.FrequencyPoints',int(nextHigher12458(self.project.GetValue('CalculationProperties.TimePoints')/2)))
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def onimpulseLengthEntered(self,event):
        self.project.SetValue('CalculationProperties.TimePoints',int(self.project.GetValue('CalculationProperties.ImpulseResponseLength')*self.project.GetValue('CalculationProperties.BaseSampleRate')+0.5))
        self.project.SetValue('CalculationProperties.FrequencyPoints',int(nextHigher12458(self.project.GetValue('CalculationProperties.TimePoints')/2)))
        self.project.SetValue('CalculationProperties.FrequencyPoints',max(1,self.project.GetValue('CalculationProperties.FrequencyPoints')))                              
        self.project.SetValue('CalculationProperties.TimePoints',self.project.GetValue('CalculationProperties.FrequencyPoints')*2)
        self.project.SetValue('CalculationProperties.FrequencyResolution',self.project.GetValue('CalculationProperties.EndFrequency')/self.project.GetValue('CalculationProperties.FrequencyPoints'))
        self.project.SetValue('CalculationProperties.ImpulseResponseLength',1./self.project.GetValue('CalculationProperties.FrequencyResolution'))
        self.UpdateStrings()

    def UpdateStrings(self):
        self.endFrequencyFrame.UpdateStrings()
        self.frequencyPointsFrame.UpdateStrings()
        self.frequencyResolutionFrame.UpdateStrings()
        self.userSampleRateFrame.UpdateStrings()
        self.baseSampleRateFrame.UpdateStrings()
        self.timePointsFrame.UpdateStrings()
        self.impulseResponseLengthFrame.UpdateStrings()
