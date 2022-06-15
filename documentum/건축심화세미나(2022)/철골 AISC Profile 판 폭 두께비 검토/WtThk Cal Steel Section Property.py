#220614

import pandas as pd
from pandas import DataFrame
dfAISC = pd.read_csv('AISC15w.csv', header = 0)
print (dfAISC)

fy = 345 # yield strength in MPa
E = 200000 # Elastic Modulus in MPa

Area = []
Weight = []
Ix = []
Sx = []
Zx = []
rx = []
Iy = []
Sy =[]
Zy = []
ry = []
Cw = []
J = []
rts = []
Flange = []
Web = []

for i in range(len(dfAISC)):
    a = 2*dfAISC.tf[i]*dfAISC.bf[i]+(dfAISC.h[i]-2*dfAISC.tf[i])*dfAISC.tw[i]
    b = a*77.22/10**6
    I1 = (2*(dfAISC.bf[i]*dfAISC.tf[i]**3/12+dfAISC.bf[i]*dfAISC.tf[i]*((dfAISC.h[i]-2*dfAISC.tf[i])/2+dfAISC.tf[i]/2)**2)+dfAISC.tw[i]*(dfAISC.h[i]-2*dfAISC.tf[i])**3/12)
    S1 = I1/(dfAISC.h[i]/2)
    Z1 = dfAISC.bf[i]*dfAISC.tf[i]*(dfAISC.h[i]-dfAISC.tf[i])+0.25*(dfAISC.h[i]-2*dfAISC.tf[i])**2*dfAISC.tw[i]
    r1 = (I1/a)**0.5
    I2 = 2*(dfAISC.tf[i]*(dfAISC.bf[i])**3/12)+(dfAISC.h[i]-2*dfAISC.tf[i])*(dfAISC.tw[i])**3/12
    S2 = I2/(dfAISC.bf[i]/2)
    Z2 = 0.5*(dfAISC.bf[i])**2*dfAISC.tf[i]+0.25*(dfAISC.h[i]-2*dfAISC.tf[i])*(dfAISC.tw[i])**2
    r2 = (I2/a)**0.5
    c = (dfAISC.h[i]-dfAISC.tf[i])**2*dfAISC.bf[i]**3*dfAISC.tf[i]/24
    j = (2*dfAISC.bf[i]*dfAISC.tf[i]**3+(dfAISC.h[i]-dfAISC.tf[i])*dfAISC.tw[i]**3)/3
    r = ((I2*c)**0.5/S1)**0.5
    if dfAISC.bf[i]/2/dfAISC.tf[i] < 0.56*(E/fy)**0.5:
        fl = "nonslender"
    else:
        fl = "slender"
        print (f1)
    if (dfAISC.h[i]-2*dfAISC.k[i])/dfAISC.tw[i] < 1.49*(E/fy)**0.5:
        wb = "nonslender"
    else:
        wb = "slender"
    Area.append (a)
    Weight.append (b)
    Ix.append (I1)
    Sx.append (S1)
    Zx.append (Z1)
    rx.append (r1)
    Iy.append (I2)
    Sy.append (S2)
    Zy.append (Z2)
    ry.append (r2)
    Cw.append (c)
    J.append (j)
    rts.append (r)
    Flange.append (fl)
    Web.append (wb)

df1 = DataFrame (Area, columns = ['Area(mm2)'])
df2 = dfAISC['ID']
df3 = DataFrame (Weight, columns = ['Weight'])
df4 = DataFrame (Ix, columns = ['Ix(mm4)'])
df5 = DataFrame (Sx, columns = ['Sx(mm3)'])
df6 = DataFrame (Zx, columns = ['Zx(mm3)'])
df7 = DataFrame (rx, columns = ['rx(mm)'])
df8 = DataFrame (Iy, columns = ['Iy(mm4)'])
df9 = DataFrame (Sy, columns = ['Sy(mm3)'])
df10 = DataFrame (Zy, columns = ['Zy(mm3)'])
df11 = DataFrame (ry, columns = ['ry(mm)'])
df12 = DataFrame (Cw, columns = ['Cw(mm6)'])
df13 = DataFrame (J, columns = ['J(mm4)'])
df14 = DataFrame (rts,columns = ['rts(mm)'])
df16 = DataFrame (Flange,columns = ['Flange'])
df17 = DataFrame (Web,columns = ['Web'])

df15 = pd.concat([df2, df1, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df16, df17], axis = 1)
print (df15)

df15.to_csv('AISC_Section_Property_220614.csv')

