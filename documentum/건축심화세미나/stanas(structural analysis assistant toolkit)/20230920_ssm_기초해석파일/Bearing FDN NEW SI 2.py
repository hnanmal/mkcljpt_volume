from sympy import Symbol, solve, re

qa = 150 # 허용지내력 kPa
h_BOFDN = 2.4 # 기초 저면 m
S = 10 # Surcharge Load kN/m^2
w_c = 24 #콘크리트 단중 kN/m^3
w_s = 17 # 흙 단중 kN/m^3
fc = 32 #콘크리트 압축강도MPa
fy = 420 #철근 항복강도 MPa
Cx = 0.5 #기둥치수 x m
Cy = 0.8 #기둥치수 y m
cc = 75 #피복두께 mm


Dc = 16 # 기둥 Pedestal 주근 mm
D = 16 # 기초 배근 mm

ldb = max(0.25*Dc*fy/(fc)**0.5, 0.043*Dc*fy) #기둥 철근의 압축 정착 길이

Ps = 850
Pu = 1235.9
Msx = 150
Msy = 120
Mux = 230
Muy = 207.2

#흙과 기초 평균 두께에 의한 유효 허용 지내력 산정
qe = qa - (w_c+w_s)/2*h_BOFDN-S 
a = qe
b = 0
c = -Ps
d = -6*Msx-6*Msy

x = Symbol('x')
eq = a*x**3+b*x**2+c*x+d
kk = solve (eq)
x1 = kk[0]
x2 = kk[1]
x3 = kk[2]

if round(re(x1),1) > 0:
	Lx = round(re(x1),2)
elif round(re(x2),1) > 0:
	Lx = round(re(x2),2)
elif round(re(x3),1) > 0:
	Lx = round(re(x3),2)

import math
Lx = max(math.ceil(Lx*10)/10,Cx) 
Ly = max(Lx, Cy) 

#1면 전단에 의한 두께 산정 d1, d2
d1 = ((Ly/2-Cy/2)*(6*Mux/(Lx*Ly**2)+Pu/(Lx*Ly)))*Lx/(0.75*0.17*fc**0.5*Lx*1000+6*Mux/(Lx*Ly**2)*Lx+Pu/(Lx*Ly)*Lx)
d2 = ((Lx/2-Cx/2)*(6*Muy/(Ly*Lx**2)+Pu/(Lx*Ly)))*Ly/(0.75*0.17*fc**0.5*Ly*1000+6*Muy/(Ly*Lx**2)*Ly+Pu/(Lx*Ly)*Ly)

#2면 전단에 의한 두께 산정 d3
s1 = (Pu)/(Lx*Ly)+Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)
s2 = (Pu)/(Lx*Ly)+Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
s3 = (Pu)/(Lx*Ly)-Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
s4 = (Pu)/(Lx*Ly)-Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)

s_max = max(s1, s2, s3, s4)
s_min = min(s1, s2, s3, s4)
s_avg = (s_max+s_min)/2

a = s_avg-0.75*0.33*fc**0.5*4*1000
b = (Cx + Cy)*s_avg-0.75*0.33*fc**0.5*2*(Cx+Cy)*1000
c = (Lx*Ly-Cx*Cy)*s_avg

x1 = (-b+(b**2-4*a*c)**0.5)/(2*a)
x2 = (-b-(b**2-4*a*c)**0.5)/(2*a)

if x1 <= 0:
	d3 = x2
elif x2 <= 0:
	d3 = x1

#기초 두께 산정
d4 = max(d1*1000, d2*1000, d3*1000, ldb)
H = math.ceil((d4+cc)/100)*100

#기초 두께에 따른 허용 지내력 재산정 / 기초 크기 재산정
qe = qa - (H/1000*w_c+(h_BOFDN-H/1000)*w_s*(Lx*Ly-Cx*Cy)/(Lx*Ly)+Cx*Cy/(Lx*Ly)*(h_BOFDN-H/1000)*(w_c))-S
a = qe
b = 0
c = -Ps
d = -6*Msx-6*Msy

x = Symbol('x')
eq = a*x**3+b*x**2+c*x+d
kk = solve (eq)
x1 = kk[0]
x2 = kk[1]
x3 = kk[2]

if round(re(x1),1) > 0:
	Lx = round(re(x1),2)
elif round(re(x2),1) > 0:
	Lx = round(re(x2),2)
elif round(re(x3),1) > 0:
	Lx = round(re(x3),2)

import math
Lx = max(math.ceil(Lx*10)/10,Cx) 
Ly = max(Lx, Cy) 
print("")

#편심 제한 기준
while Lx/6 < Msy/Ps:
	Lx = Lx + 0.1
print ("Lx = ", round(Lx,1), "m")

while Ly/6 < Msx/Ps:
	Ly = Ly + 0.1
print ("Ly = ", round(Ly,1), "m")


#1면 전단에 의한 두께 재산정 d1, d2
d1 = ((Ly/2-Cy/2)*(6*Mux/(Lx*Ly**2)+Pu/(Lx*Ly)))*Lx/(0.75*0.17*fc**0.5*Lx*1000+6*Mux/(Lx*Ly**2)*Lx+Pu/(Lx*Ly)*Lx)
d2 = ((Lx/2-Cx/2)*(6*Muy/(Ly*Lx**2)+Pu/(Lx*Ly)))*Ly/(0.75*0.17*fc**0.5*Ly*1000+6*Muy/(Ly*Lx**2)*Ly+Pu/(Lx*Ly)*Ly)

#2면 전단에 의한 두께 재산정 d3
s1 = (Pu)/(Lx*Ly)+Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)
s2 = (Pu)/(Lx*Ly)+Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
s3 = (Pu)/(Lx*Ly)-Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
s4 = (Pu)/(Lx*Ly)-Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)

s_max = max(s1, s2, s3, s4)
s_min = min(s1, s2, s3, s4)
s_avg = (s_max+s_min)/2

a = s_avg-0.75*0.33*fc**0.5*4*1000
b = (Cx + Cy)*s_avg-0.75*0.33*fc**0.5*2*(Cx+Cy)*1000
c = (Lx*Ly-Cx*Cy)*s_avg

x1 = (-b+(b**2-4*a*c)**0.5)/(2*a)
x2 = (-b-(b**2-4*a*c)**0.5)/(2*a)

if x1 < 0:
	d3 = x2
elif x2 < 0:
	d3 = x1


print ("")
d4 = max(d1*1000, d2*1000, d3*1000, ldb)
print ("Required FDN Effective Depth = ", round(d4,1), "mm")
H = math.ceil((d4+cc+D)/100)*100
print ("FDN Full Depth = ", H, "mm")
print ("")
#요구모멘트산정
Mux1 = (Ly/2-Cy/2)**2/2*(Pu/(Lx*Ly)+abs(Mux/(Lx*Ly**2/6)))
Muy1 = (Lx/2-Cx/2)**2/2*(Pu/(Lx*Ly)+abs(Muy/(Ly*Lx**2/6)))
print ("Mux =", round(Mux1,2), "kNm/m")
print ("    = ", round(Mux1 * Lx,2), "kNm")
print ("Muy =", round(Muy1,2), "kNm/m")
print ("    = ", round(Muy1 * Ly,2), "kNm")


#방향별 모멘트 크기에 따른 주근과 부근 유효 깊이 산정
if Mux1 < Muy1:
	dx = H-cc-3/2*D
	dy = H-cc-1/2*D
else:
	dy = H-cc-3/2*D
	dx = H-cc-1/2*D

print ("")
print ("dx = ", round(dx, 4), "mm")
print ("dy = ", round(dy, 4), "mm")
print ("")

#각 방향별 휨 철근 설계
b = Lx*1000
d = dx
Mu = Mux1*10**6

a1 = ((-0.9*0.85*fc*b*d)+((0.9*0.85*fc*b*d)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
a2 = ((-0.9*0.85*fc*b*d)-((0.9*0.85*fc*b*d)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))

if a1 < 0:
	a = a2
elif a2 < 0:
	a = a1
elif a1 > d:
	a = a2
elif a2 > d:
	a = a1

Asx = max(0.85*fc*a*b/fy, 0.0018*1000*H)
print ("Asx = ", round(Asx,1), "mm2/m")
print ("    = ", round(Asx,1)* Lx, "mm2")
sx = int(1000/(Asx/((D/2)**2*3.141))/50)*50
print ("D",D,"@",sx)
print ("")

b = Ly*1000
d = dy
Mu = Muy1*10**6

a1 = ((-0.9*0.85*fc*b*d)+((0.9*0.85*fc*b*d)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
a2 = ((-0.9*0.85*fc*b*d)-((0.9*0.85*fc*b*d)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))

if a1 < 0:
	a = a2
elif a2 < 0:
	a = a1
elif a1 > d:
	a = a2
elif a2 > d:
	a = a1

Asy = max(0.85*fc*a*b/fy, 0.0018*1000*H)
print ("Asy = ", round(Asy,1), "mm2/m")
print ("    = ", round(Asy,1) * Ly, "mm2")
sy = int(1000/(Asy/((D/2)**2*3.141592))/50)*50
print ("D",D,"@",sy)

#허용지내력 만족 여부 검토
W_c = (Lx*Ly*H/1000+Cx*Cy*(h_BOFDN-H/1000))*w_c
W_s = (Lx*Ly-Cx*Cy)*(h_BOFDN-H/1000)*w_s

a1 = (Ps+W_c+W_s)/(Lx*Ly)+Msx/(Lx*Ly**2/6)+Msy/(Ly*Lx**2/6)+S
a2 = (Ps+W_c+W_s)/(Lx*Ly)+Msx/(Lx*Ly**2/6)-Msy/(Ly*Lx**2/6)+S
a3 = (Ps+W_c+W_s)/(Lx*Ly)-Msx/(Lx*Ly**2/6)-Msy/(Ly*Lx**2/6)+S
a4 = (Ps+W_c+W_s)/(Lx*Ly)-Msx/(Lx*Ly**2/6)+Msy/(Ly*Lx**2/6)+S

print ("")
print ("Service Soil Pressure = ", round(max(a1, a2, a3, a4),2), "kPa")
print ("Factored Soil Pressure = ", round(max(s1, s2, s3, s4),2), "kPa")
print ("")

#1방향/2방향 전단검토
dxy = (dx+dy)/2

Vux = (Ly/2-Cy/2-dx/1000)*(max(Mux/(Lx*Ly**2/6),-Mux/(Lx*Ly**2/6))+Pu/(Lx*Ly))*Lx
print ("Vux =" , round(Vux,2), "kN")
phiVcx = 0.75*0.17*(fc)**0.5*Lx*1000*dx/1000
print("phiVcx =" , round(phiVcx,2), "kN")
print ("")

Vuy = (Lx/2-Cx/2-dy/1000)*(max(Muy/(Ly*Lx**2/6),-Muy/(Ly*Lx**2/6))+Pu/(Lx*Ly))*Ly
print ("Vuy =", round(Vuy,2), "kN")
phiVcy = 0.75*0.17*(fc)**0.5*Ly*1000*dy/1000
print("phiVcy =", round(phiVcy,2), "kN")
print ("")

Vup = (Lx*Ly-(Cx+dy/1000)*(Cy+dx/1000))*s_avg
print ("Vup =", round(Vup,2), "kN")
phiVcp = 0.75*0.33*(fc)**0.5*(2*Cx+2*Cy+4*dxy/1000)*dxy/1000*1000
print ("phiVcp =", round(phiVcp,2), "kN")
print ("")






