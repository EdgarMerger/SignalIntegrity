import SignalIntegrity.Lib as si

ssps=si.sd.SystemSParametersSymbolic()
ssps.AddDevice('S',2)
ssps.AddDevice('\\Gamma_l',1)
ssps.AddDevice('\\Gamma_s',1)
ssps.ConnectDevicePort('\\Gamma_s',1,'S',1)
ssps.ConnectDevicePort('S',2,'\\Gamma_l',1)
ssps.AssignM('\\Gamma_s',1,'m1')
ssps.LaTeXSystemEquation().Emit()
ssps.AssignSParameters('\\Gamma_s',si.sy.ShuntZ(1,'Zs'))
ssps.AssignSParameters('\\Gamma_l',si.sy.ShuntZ(1,'Zl'))
ssps.Clear().LaTeXSystemEquation().Emit()