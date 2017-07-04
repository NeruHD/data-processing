from tkinter import *
import re

#import
data = []
V_Unom = []
R_RA = []
tClose = []
with open("dat.txt", 'rt') as f:
    data.clear()
    for line in f:
        if re.findall(r'V_Unom', line):
            V_Unom.clear()
            V_Unom.append([str(x) for x in line.split()])
        if re.findall(r'R_RA', line):
            R_RA.clear()
            R_RA.append([str(x) for x in line.split()])
        if re.findall(r'tClose=', line):
            tClose.append([str(x) for x in line.split()])
        if re.findall(r'E-0', line) or re.findall(r'E+0', line):
            data.append([str(x) for x in line.split()])
    temp = (float(V_Unom[0][3]) * float(V_Unom[0][3])) / float(R_RA[0][3]) / 2500
    NS = int(temp)
    PH = int((temp - NS)*10)
   # TZ = re.findall(r'[0-99]', tClose[0][5])  re.findall(r'[0-99]', tClose[1][5])
print(V_Unom)
print(R_RA)
print(tClose)
print(NS)
print(PH)
print(data.__len__())

#const
Tn = 0.014

root = Tk()
root.title("")
root.geometry("800x600")

root.mainloop()

