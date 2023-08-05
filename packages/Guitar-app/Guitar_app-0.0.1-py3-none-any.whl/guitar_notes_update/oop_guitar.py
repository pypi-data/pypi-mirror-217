import turtle
from tkinter import *
import random
import playsound
import os
from sys import exit

screen = turtle.Screen()
screen.title("Fret Board")
screen.setup(1000, 400)
screen.bgpic('1024x510.gif')
note = turtle.Turtle()
note.shapesize(2)
note.penup()
FONT_SIZE = 25
FONT = ("Aarial", FONT_SIZE, "normal")
note.pensize(2)
path = "C:\\Users\\d\\PycharmProjects\\guitar_notes_update\\notes"
noteselected = random.choice(os.listdir(path))
n=str(path+ '\\' + noteselected)
def ui():
    label1 = Label(root, text="option 1 : DISPLAY Guitar notes")
    label2 = Label(root, text="option 2 : Guess The Note")
    label3 = Label(root, text="Enter the note you heard : ")
    label4 = Label(root, text="Correct")
    label5 = Label(root, text="Try again")
    label1.config(font=('Helvatical bold', 20), background='black', foreground='red')
    label2.config(font=('Helvatical bold', 20), background='black', foreground='red')
    label3.config(font=('Helvatical bold', 20), background='black', foreground='red')
    label4.config(font=('Helvatical bold', 40), background='black', foreground='gold')
    label5.config(font=('Helvatical bold', 40), background='black', foreground='gold')
    label1.pack()
    label2.pack()
    button1 = Button(root, text='Number: ', width=50, bg='grey', command=user_in)
    button2 = Button(root, text='Enter a note', width=50, bg='grey', command=guess_the_note)
    button3 = Button(root, text='Quit program', width=50, fg='black', bg='blue', command=exit)
    ent1.config(bg='white', fg='black', font=('Helvatical bold', 20))
    ent2.config(bg='white', fg='black', font=('Helvatical bold', 20))
    label1.pack()
    label2.pack()
    label3.pack()
    button1.bind('<Button-1>')
    button1.pack()
    ent1.pack()
    button2.pack()
    button2.bind('<Button-2>')
    ent2.pack()
    button3.pack()
    button3.bind('<Button-3>')
root = Tk('menu')
root.config(background='black')
root.title("Menu")
root.minsize(1000, 400)
ent1 = Entry(root)
ent2 = Entry(root)
def guess_the_note():
    playsound.playsound(n)
    #print(ent2.get()+n) 'test the note'
    label4 = Label(root, text="Correct")
    label5 = Label(root, text="Try again")
    label4.config(font=('Helvatical bold', 40), background='black', foreground='gold')
    label5.config(font=('Helvatical bold', 40), background='black', foreground='gold')
    if ent2.get().upper().__add__('.mp3') == n.strip(path):
        label4.pack()
    else:
        label5.pack()
class guitar_string:
    def __init__(self):
        note.color('blue')
    def Top_E(self):
        F = [-432.0, -141.0]
        FS = [-374.0, -142.0]
        G = [-295.0, -142.0]
        Ab = [-240.0, -145.0]
        A = [-153.0, -145.0]
        Bb = [-100.0, -145.0]
        B = [-9.0, -142.0]
        C = [48.0, -143.0]
        CS = [120.0, -143.0]
        D = [191.0, -143.0]
        Eb = [260.0, -141.0]
        E = [322.0, -141.0]
        #############################TOP E string######################################
        note.goto(F)
        note.write('F', font=FONT)
        playsound.playsound('notes/TE1.mp3')
        note.goto(FS)
        note.write('F#', font=FONT)
        playsound.playsound('notes/TE2.mp3')
        note.goto(G)
        note.write('G', font=FONT)
        playsound.playsound('notes/TE3.mp3')
        note.goto(Ab)
        note.write('Ab', font=FONT)
        playsound.playsound('notes/TE4.mp3')
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/TE5.mp3')
        note.goto(Bb)
        note.write('Bb', font=FONT)
        playsound.playsound('notes/TE6.mp3')
        note.goto(B)
        note.write('B', font=FONT)
        playsound.playsound('notes/TE7.mp3')
        note.goto(C)
        note.write('C', font=FONT)
        playsound.playsound('notes/TE8.mp3')
        note.goto(CS)
        note.write('C#', font=FONT)
        playsound.playsound('notes/TE9.mp3')
        note.goto(D)
        note.write('D', font=FONT)
        playsound.playsound('notes/TE10.mp3')
        note.goto(Eb)
        note.write('Eb', font=FONT)
        playsound.playsound('notes/TE11.mp3')
        note.goto(E)
        note.write('E', font=FONT)
        playsound.playsound('notes/TE12.mp3')



         ####################################################################
          # #########################A_string##################################
    def A_string(self):
           note.color('red')
           Bb = [-435.0, -86.0]
           B = [-365.0, -85.0]
           C = [-295.0, -85.0]
           CS = [-240.0, -85.0]
           D = [-152.0, -84.0]
           Eb = [-100.0, -84.0]
           E = [-8.0, -84.0]
           F = [48.0, -84.0]
           FS = [105.0, -84.0]
           G = [186.0, -83.0]
           Ab = [249.0, -84.0]
           A = [322.0, -85.0]

           note.goto(Bb)
           note.write('Bb', font=FONT)
           playsound.playsound('notes/A1.mp3')
           note.goto(B)
           note.write('B', font=FONT)
           playsound.playsound('notes/A2.mp3')
           note.goto(C)
           note.write('C', font=FONT)
           playsound.playsound('notes/A3.mp3')
           note.goto(CS)
           note.write('C#', font=FONT)
           playsound.playsound('notes/A4.mp3')
           note.goto(D)
           note.write('D', font=FONT)
           playsound.playsound('notes/A5.mp3')
           note.goto(Eb)
           note.write('Eb', font=FONT)
           playsound.playsound('notes/A6.mp3')
           note.goto(E)
           note.write('E', font=FONT)
           playsound.playsound('notes/A7.mp3')
           note.goto(F)
           note.write('F', font=FONT)
           playsound.playsound('notes/A8.mp3')
           note.goto(FS)
           note.write('F#', font=FONT)
           playsound.playsound('notes/A9.mp3')
           note.goto(G)
           note.write('G', font=FONT)
           playsound.playsound('notes/A10.mp3')
           note.goto(Ab)
           note.write('Ab', font=FONT)
           playsound.playsound('notes/A11.mp3')
           note.goto(A)
           note.write('A', font=FONT)
           playsound.playsound('notes/A12.mp3')
    def D_string(self):
        ##############################################################################
        #############################D_string#################################################
        Eb = [-434.0, -27.0]
        E = [-362.0, -30.0]
        F = [-284.0, -29.0]
        FS = [-240.0, -29.0]
        G = [-158.0, -30.0]
        Ab = [-89.0, -28.0]
        A = [-11.0, -28.0]
        Bb = [53.0, -30.0]
        B = [108.0, -30.0]
        C = [180.0, -29.0]
        CS = [248.0, -29.0]
        D = [319.0, -29.0]

        note.color('orange')
        note.goto(Eb)
        note.write('Eb', font=FONT)
        playsound.playsound('notes/D1.mp3')
        note.goto(E)
        note.write('E', font=FONT)
        playsound.playsound('notes/D2.mp3')
        note.goto(F)
        note.write('F', font=FONT)
        playsound.playsound('notes/D3.mp3')
        note.goto(FS)
        note.write('F#', font=FONT)
        playsound.playsound('notes/D4.mp3')
        note.goto(G)
        note.write('G', font=FONT)
        playsound.playsound('notes/D5.mp3')
        note.goto(Ab)
        note.write('Ab', font=FONT)
        playsound.playsound('notes/D6.mp3')
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/D7.mp3')
        note.goto(Bb)
        note.write('Bb', font=FONT)
        playsound.playsound('notes/D8.mp3')
        note.goto(B)
        note.write('B', font=FONT)
        playsound.playsound('notes/D9.mp3')
        note.goto(C)
        note.write('C', font=FONT)
        playsound.playsound('notes/D10.mp3')
        note.goto(CS)
        note.write('C#', font=FONT)
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/D11.mp3')
        note.goto(D)
        note.write('D', font=FONT)
        playsound.playsound('notes/D12.mp3')
    def G_string(self):
        ###################################################################################
        ##################################G_string#################################################
        Ab = [-438.0, 28.0]
        A = [-358.0, 28.0]
        Bb = [-295.0, 30.0]
        B = [-222.0, 31.0]
        C = [-155.0, 31.0]
        CS = [-98.0, 29.0]
        D = [-15.0, 30.0]
        Eb = [44.0, 30.0]
        E = [112.0, 30.0]
        F = [182.0, 31.0]
        FS = [254.0, 30.0]
        G = [320.0, 31.0]
        note.color('green')
        note.goto(Ab)
        note.write('Ab', font=FONT)
        playsound.playsound('notes/G1.mp3')
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/G2.mp3')
        note.goto(Bb)
        note.write('Bb', font=FONT)
        playsound.playsound('notes/G3.mp3')
        note.goto(B)
        note.write('B', font=FONT)
        playsound.playsound('notes/G4.mp3')
        note.goto(C)
        note.write('C', font=FONT)
        playsound.playsound('notes/G5.mp3')
        note.goto(CS)
        note.write('C#', font=FONT)
        playsound.playsound('notes/G6.mp3')
        note.goto(D)
        note.write('D', font=FONT)
        playsound.playsound('notes/G7.mp3')
        note.goto(Eb)
        note.write('Eb', font=FONT)
        playsound.playsound('notes/G8.mp3')
        note.goto(E)
        note.write('E', font=FONT)
        playsound.playsound('notes/G9.mp3')
        note.goto(F)
        note.write('F', font=FONT)
        playsound.playsound('notes/G10.mp3')
        note.goto(FS)
        note.write('F#', font=FONT)
        playsound.playsound('notes/G11.mp3')
        note.goto(G)
        note.write('G', font=FONT)
        playsound.playsound('notes/G12.mp3')
    def B_string(self):
        #######################################################################################
        #####################################B_String##########################################

        C = [-435.0, 87.0]
        CS = [-374.0, 87.0]
        D = [-302.0, 87.0]
        Eb = [-234.0, 87.0]
        E = [-150.0, 86.0]
        F = [-91.0, 87.0]
        FS = [-33.0, 86.0]
        G = [56.0, 87.0]
        Ab = [120.0, 88.0]
        A = [187.0, 86.0]
        Bb = [254.0, 86.0]
        B = [322.0, 87.0]
        note.color('grey')
        note.goto(C)
        note.write('C', font=FONT)
        playsound.playsound('notes/B1.mp3')
        note.goto(CS)
        note.write('C#', font=FONT)
        playsound.playsound('notes/B2.mp3')
        note.goto(D)
        note.write('D', font=FONT)
        playsound.playsound('notes/B3.mp3')
        note.goto(Eb)
        note.write('Eb', font=FONT)
        playsound.playsound('notes/B4.mp3')
        note.goto(E)
        note.write('E', font=FONT)
        playsound.playsound('notes/B5.mp3')
        note.goto(F)
        note.write('F', font=FONT)
        playsound.playsound('notes/B6.mp3')
        note.goto(FS)
        note.write('F#', font=FONT)
        playsound.playsound('notes/B7.mp3')
        note.goto(G)
        note.write('G', font=FONT)
        playsound.playsound('notes/B8.mp3')
        note.goto(Ab)
        note.write('Ab', font=FONT)
        playsound.playsound('notes/B9.mp3')
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/B10.mp3')
        note.goto(Bb)
        note.write('Bb', font=FONT)
        playsound.playsound('notes/B11.mp3')
        note.goto(B)
        note.write('B', font=FONT)
        playsound.playsound('notes/B12.mp3')
    def e_string(self):
        #######################################################################################
        #################################e_string##############################################
        F = [-435.0, 143.0]
        FS = [-368.0, 144.0]
        G = [-293.0, 142.0]
        Ab = [-235.0, 142.0]
        A = [-170.0, 140.0]
        Bb = [-103.0, 144.0]
        B = [-22.0, 141.0]
        C = [55.0, 141.0]
        CS = [110.0, 141.0]
        D = [180.0, 141.0]
        Eb = [247.0, 141.0]
        E = [315.0, 140.0]
        note.color('yellow')

        note.goto(F)
        note.write('F', font=FONT)
        playsound.playsound('notes/E1.mp3')
        note.goto(FS)
        note.write('F#', font=FONT)
        playsound.playsound('notes/E2.mp3')
        note.goto(G)
        note.write('G', font=FONT)
        playsound.playsound('notes/E3.mp3')
        note.goto(Ab)
        note.write('Ab', font=FONT)
        playsound.playsound('notes/E4.mp3')
        note.goto(A)
        note.write('A', font=FONT)
        playsound.playsound('notes/E5.mp3')
        note.goto(Bb)
        note.write('Bb', font=FONT)
        playsound.playsound('notes/E6.mp3')
        note.goto(B)
        note.write('B', font=FONT)
        playsound.playsound('notes/E7.mp3')
        note.goto(C)
        note.write('C', font=FONT)
        playsound.playsound('notes/E8.mp3')
        note.goto(CS)
        note.write('C#', font=FONT)
        playsound.playsound('notes/E9.mp3')
        note.goto(D)
        note.write('D', font=FONT)
        playsound.playsound('notes/E10.mp3')
        note.goto(Eb)
        note.write('Eb', font=FONT)
        playsound.playsound('notes/E11.mp3')
        note.goto(E)
        note.write('E', font=FONT)
        playsound.playsound('notes/E12.mp3')

def animation1():
    gu=guitar_string()
    gu.Top_E(),\
        gu.A_string(),\
        gu.D_string(),\
        gu.G_string(),\
        gu.B_string(),\
        gu.e_string()
def user_in():
    if int(ent1.get()) == 1:
        animation1()
    if int (ent1.get()) == 2:
        guess_the_note()
ui()
screen.mainloop()


