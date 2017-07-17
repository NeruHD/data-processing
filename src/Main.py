import tkinter as tk
import tkinter.ttk as ttk
import re
import pylab as a
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#import

#const
elements = 55
select = []
V_Unom_mas = 100

Tn = 0.014
Tkk = 0.0143
Tk_n = V_Unom_mas - (0.1 * V_Unom_mas)
Tk_k = V_Unom_mas + (0.1 * V_Unom_mas)

def mas_name(name):
    V_Unom = []
    R_RA = []
    tClose = []
    with open('data/' + name, 'rt') as f:
        for line in f:
            if re.findall(r'V_Unom', line):
                V_Unom.clear()
                V_Unom.append([str(x) for x in line.split()])
            if re.findall(r'R_RA', line):
                R_RA.clear()
                R_RA.append([str(x) for x in line.split()])
            if re.findall(r'X_SwStart', line):
                tClose.append([str(x) for x in line.split()])
            if re.findall(r'X_U1', line):
                tClose.append([str(x) for x in line.split()])
    temp = (float(V_Unom[0][3]) * float(V_Unom[0][3])) / float(R_RA[0][3]) / 2500
    NS = int(temp)
    PH = int((temp - NS) * 10)
    TZ_1 = re.findall('(\d+)', tClose[0][5])
    TZ_2 = re.findall(r'\d+\.*\d*', tClose[1][5])
    TZ = float(TZ_1[0]) - float(TZ_2[0])
    if TZ == 0.0:
        TZ = '00'
    else:
        TZ = int(float("{0:.2f}".format(int(TZ) - TZ))*100)
        if TZ < 10:
            TZ = '0' + str(TZ)
    name = re.findall('(\d+)', name)
    if int(name[0]) < 10:
        name = '00' + str(name[0])
    else:
        name = '0' + str(name[0])
    name_mas = str(NS) + '_' + str(PH) + '_' + str(TZ) + '_' + name
    f.close()
    return str(name_mas)

def import_file(name):
    data = []
    with open('data/' + name, 'rt') as f:
        data.clear()
        for line in f:
            if re.findall(r'E-0', line) or re.findall(r'E+0', line):
                data.append([str(x) for x in line.split()])
    f.close()
    return data
Pn = []
def import_file_outs(name):
    data = []
    with open('outs/' + name, 'rt') as f:
        data.clear()
        for line in f:
            if re.findall(r'\d+\.*\d*', line):
                data.append([str(x) for x in line.split()])
            if re.findall(r'Pn', line):
                Pn.append([str(x) for x in line.split()])
        if data[0][:] == Pn[0][:]:
            data.__delitem__(0)
        if data[-1][:] == Pn[1][:]:
            data.__delitem__(-1)
    f.close()
    return data

def export_file(masn, massiv):
    V = []
    I = []
    f = open('outs/' + masn + '.txt', 'w')
    f.write('TIME              V(N27236)         I(R_RK2)              Pn \n\n')
    for i in range(massiv.__len__()):
        V.append(float(massiv[i][1]))
        I.append(float(massiv[i][4]))
        f.writelines(str(float(massiv[i][0])) + '          ' + str(float(massiv[i][1])) + '          ' + str(float(massiv[i][4])) + '          ' + str(round(float(massiv[i][1]) * float(massiv[i][4]), 5)) + '\n')
    V_av = sum(V) / float(len(V))
    I_av = sum(I) / float(len(I))
    Pn = V_av * I_av
    f.write('\n Pn     ' + str(round(Pn, 5)))
    f.close()
    return 1

def obr_mas(mas):
    Tk_v = []
    temp = []
    for i in range(mas.__len__()):
        if (float(mas[i][1]) > Tk_n) and (float(mas[i][1]) < Tk_k):
            if (float(mas[i][0]) > Tkk):
                Tk_v.append(float(mas[i][0]))
    Tk = Tk_v[-1] - Tk_v[0]
    Tk = Tk + Tn
    for j in range(mas.__len__()):
        if ((float(mas[j][0]) > Tn) and (float(mas[j][0]) < Tk)):
            temp.append(mas[j][:])
    return temp

i = 1
for i in range(1 , elements+1):
    massiv = []
    mas_o = []
    name = str(i) + '.txt'
    mas = mas_name(name)
    select.append(mas)
    massiv = import_file(name)
    mas_o = obr_mas(massiv)
    print('process ' + str(i) + ' | ' + str(elements))
    export_file(mas, mas_o)

def button_click(event):
    a.cla()
    xlist.clear()
    ylist.clear()
    name = str(combobox.get()) + '.txt'
    data = import_file_outs(name)
    if data[0][:] == Pn[0][:]:
        data.__delitem__(0)
    if data[-1][:] == Pn[1][:]:
        data.__delitem__(-1)
    for i in range(data.__len__()-1):
        xlist.append(data[i][0])
        ylist.append(data[i][3])
    a.plot(xlist, ylist)
    a.grid(True)
    canvas.draw()


#reconstruct massiv


root = tk.Tk()
root.title("")
root.geometry("800x600")


frame = tk.Frame(root)
frame.pack()
combobox = ttk.Combobox(frame,values = select,height=10)
combobox.set(u"Выбор файла")
combobox.bind('<<ComboboxSelected>>', button_click)
combobox.pack(side='top')
# button=tk.Button(root,text='Cформировать график')
# button.pack(side='top')
# button.bind("<Button-1>", button_click)

#grafik

f = Figure(figsize=(19.2, 10.8), dpi=100)
a = f.add_subplot(111)

#name = '2_2_60_053.txt'
#data = import_file_outs(name)
xlist = []
ylist = []
#for i in range(data.__len__()):
   # xlist.append(data[i][0])
   # ylist.append(data[i][3])

# f = Figure(figsize=(19.2, 10.8), dpi=100)
# a = f.add_subplot(111)
# a.plot(xlist, ylist)
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.show()
# canvas.get_tk_widget().pack(side='left')

canvas = FigureCanvasTkAgg(f, master=root)

canvas.get_tk_widget().pack(side='left')

root.mainloop()

