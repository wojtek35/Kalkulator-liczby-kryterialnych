from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import math


root=Tk()
root.title('Kalkulator liczb kryterialnych')
root.iconbitmap('wind.ico')
root.geometry("400x400")





# Tworzenie bazy danych (lub połączenie się z bazą danych)
baza_danych = sqlite3.connect('parametry_liczb_kryterialnych.db')

# Tworzenie kursora
c = baza_danych.cursor()

# Tworzenie tabeli
c.execute("""CREATE TABLE IF NOT EXISTS dane_wejsciowe (
        natezenie_przeplywu_Q real,
        temperatura_T real,
        srednica_d real,
        bok_b real,
        bok_h real
        )""")





# Fukcja do wysyłania danych do bazy
def submit():

    # Stworzenie bazy danych 
    baza_danych = sqlite3.connect('parametry_liczb_kryterialnych.db')

    # Tworzenie kursora
    c = baza_danych.cursor()

    # Wprowadzenie danych do tabeli
    c.execute("DELETE from dane_wejsciowe")
    c.execute("INSERT INTO dane_wejsciowe VALUES (:natezenie_przeplywu_Q, :temperatura_T, :srednica_d, :bok_b, :bok_h)",
            {
                'natezenie_przeplywu_Q':  natezenie_przeplywu_Q.get(),
                'temperatura_T':  temperatura_T.get(),
                'srednica_d':  srednica_d.get(),
                'bok_b':  bok_b.get(),
                'bok_h':  bok_h.get(),
            }
        )

    # Wprowadzenie zmian
    baza_danych.commit()

    # Odłączenie od bazy danych
    baza_danych.close()

przekroj = IntVar()
czynnik = IntVar()
czynnik.set("1")
przekroj.set("1")

Radiobutton(root,text='Przekrój kołowy', variable=przekroj, value=1).grid(row=2,column=2)
Radiobutton(root,text='Przekrój prostokątny', variable=przekroj, value=2).grid(row=4,column=2)

Radiobutton(root,text='Woda', variable=czynnik, value=1).grid(row=2,column=7)
Radiobutton(root,text='Powietrze', variable=czynnik, value=2).grid(row=4,column=7)



def query():
    # Połączenie się z bazą danych
    baza_danych = sqlite3.connect('parametry_liczb_kryterialnych.db')

    # Tworzenie kursora
    c = baza_danych.cursor()

    # Pobranie danych
    c.execute("SELECT * ,oid FROM dane_wejsciowe")

    d_wejsciowe= c.fetchone()
    

    z_listy_Q=d_wejsciowe[0]
    z_listy_T=d_wejsciowe[1]
    z_listy_d=d_wejsciowe[2]
    z_listy_b=d_wejsciowe[3]
    z_listy_h=d_wejsciowe[4]

    mi=IntVar()
    ro=IntVar()
    kin_wsp_lepkosci=IntVar() 
    V=IntVar()   
    Re=IntVar() 
    de=IntVar() 

#rew
    
    if czynnik.get() == 1:
        mi=0.00179/(1+0.337*z_listy_T+0.002211*z_listy_T**2)
        ro = 997.07
        kin_wsp_lepkosci = mi/ro


    if czynnik.get()== 2:
        mi=((0.0000168*385)*((z_listy_T/273)**(1.5)))/(z_listy_T+112)
        ro =1.2
        kin_wsp_lepkosci = mi/ro

    if przekroj.get() ==1:
        de=z_listy_d
        V=4*z_listy_Q/de
        
        
    if przekroj.get() ==2:
        de=(4*z_listy_b*z_listy_h)/(2*z_listy_b+2*z_listy_h)
        V=4*z_listy_Q/de
        
    
    Re=V*de/kin_wsp_lepkosci
    Fr=V**2/9.81*de
    Ga=9.81*(ro**2)*(de**3)/mi**2

    wynik=Label(root, text=Re).grid(row=8, column=8)
    wynik=Label(root, text=Fr).grid(row=9, column=8)
    wynik=Label(root, text=Ga).grid(row=10, column=8)
    


    # Wprowadzenie zmian
    baza_danych.commit()

    # Odłączenie od bazy danych
    baza_danych.close()







# Pola do wprowadzenia danych
natezenie_przeplywu_Q = Entry(root, width=10)
natezenie_przeplywu_Q.grid(row=3, column=1, padx=10)

temperatura_T = Entry(root, width=10)
temperatura_T.grid(row=4, column=1)

srednica_d = Entry(root, width=10)
srednica_d.grid(row=3, column=3)

bok_b = Entry(root, width=10)
bok_b.grid(row=5, column=3)

bok_h = Entry(root, width=10)
bok_h.grid(row=6, column=3)

# Opisy pól 
natezenie_przeplywu_Q_opis = Label(root, text="Natężenie przepływu Q")
natezenie_przeplywu_Q_opis.grid(row=3, column=0)

temperatura_T_opis = Label(root, text="Temperatura T")
temperatura_T_opis.grid(row=4, column=0)

srednica_d_opis = Label(root, text="Średnica d")
srednica_d_opis.grid(row=3, column=2)

bok_b_opis = Label(root, text="Bok b")
bok_b_opis.grid(row=5, column=2)

bok_h_opis = Label(root, text="Bok h")
bok_h_opis.grid(row=6, column=2)

# Tworzenie przycisku do potwierdzenia wprowadzonych danych

wprowadz_dane = Button(root, text="Wprowadź dane", command=submit)
wprowadz_dane.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# Ściągnięcie danych z bazy i liczenie 
przycisk_licz = Button(root, text='Licz', command=query)
przycisk_licz.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


# Wprowadzenie zmian
baza_danych.commit()

# Odłączenie od bazy danych
baza_danych.close()

root.mainloop()