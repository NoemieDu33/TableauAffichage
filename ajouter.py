from tkinter import *
from tkinter import messagebox, ttk
import os
import time
from tkinter import filedialog
import datetime
import calendar
import sys
from distutils.version import StrictVersion as Version
from tkinter_custom_button import TkinterCustomButton
import pickle
from pathlib import Path
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
from retirerautomatique import automatique
#-----------------------------------------
root = Tk()
root.geometry("620x400")
root.configure(background="#1f1f1f")
#-----------------------------------------
en_tete = Label(root, text ='Gérer les profs absents',font = "50") 
en_tete.grid(row=0, column=0)
en_tete.configure(background="#1f1f1f", foreground='white')
#-----------------------------------------    
ddvar=StringVar()
dfvar=StringVar()
#-----------------------------------------  
hlist = ["08:05","09:05","10:15","11:15","13:45","14:45","15:55","16:55","17:50"]
#-----------------------------------------  
hdvar = ttk.Combobox(root, values = hlist)
hdvar.set("Heure de début")
hdvar.grid(row=3, column=3, padx=5, pady=5)
#-----------------------------------------  
hfvar = ttk.Combobox(root, values = hlist)
hfvar.set("Heure de fin")
hfvar.grid(row=3, column=5, padx = 5, pady = 5)
#-----------------------------------------
mylist = Listbox(root, exportselection=0 , height=20)
listeprofs=[]
with open('listfile.data', 'rb') as filehandle:
    listeprofs = pickle.load(filehandle)
for line in range(len(listeprofs)):
    mylist.insert(END,listeprofs[line])
mylist.grid(row=1,column=0,rowspan=10)
#-----------------------------------------
T = Text(root, height = 5, width = 50)
l = Label(root, text = "",background="#1f1f1f", foreground='white')
l.grid(row = 6, column = 3)
Th = Text(root, height = 5, width = 50)
lh = Label(root, text = "",background="#1f1f1f", foreground='white')
lh.grid(row = 6, column = 5, columnspan = 2)
#-----------------------------------------  
today = datetime.date.today()
mindate = today - datetime.timedelta(days=365)
maxdate = today + datetime.timedelta(days=365)
#-----------------------------------------  
caldebut = DateEntry(root, selectmode='day', locale='fr_FR',
                mindate=mindate, maxdate=maxdate, disabledforeground='red', year=today.year, month=today.month, day=today.day, textvariable = ddvar)
caldebut.grid(row=2, column=3, padx=5, pady=5)
#-----------------------------------------  
calfin = DateEntry(root,  selectmode='day', locale='fr_FR',
                mindate=mindate, maxdate=maxdate, disabledforeground='red', year=today.year, month=today.month, day=today.day, textvariable = dfvar)
calfin.grid(row=2, column=5, padx = 5, pady = 5)
#-----------------------------------------  
def verifier_la_date(date_a_comparer):
    j1,j2,j,m1,m2,m,h1,h2,h,mi1,mi2,mi,y1,y2,y3,y4,y = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    bon = True
    if len(date_a_comparer)==16:
        for i in range(len(date_a_comparer)):
            if i==2 or i==5:
                if date_a_comparer[i]=="/":
                    continue
                else:
                    lh['text']="Erreur sur les slash!"
                    bon = False
                    break
            elif i==10:
                if date_a_comparer[i]==" ":
                    continue
                else:
                    lh['text']="Erreur sur l'espace!"
                    bon = False
                    break
            elif i==13:
                if date_a_comparer[i]==":":
                    continue
                else:
                    lh['text']="Erreur sur les deux points!"
                    bon = False
                    break
            else:
                if (isinstance(int(date_a_comparer[i]), int)):
                    if i==0:
                        j1=date_a_comparer[i]
                    elif i==1:
                        j2=date_a_comparer[i]
                        j=j1+j2
                    elif i==3:
                        m1=date_a_comparer[i]
                    elif i==4:
                        m2=date_a_comparer[i]
                        m=m1+m2
                    elif i==6:
                       y1=date_a_comparer[i]
                    elif i==7:
                        y2=date_a_comparer[i]
                    elif i==8:
                        y3=date_a_comparer[i]
                    elif i==9:
                        y4=date_a_comparer[i]
                        y=y1+y2+y3+y4  
                    elif i==11:
                        h1=date_a_comparer[i]
                    elif i==12:
                        h2=date_a_comparer[i]
                        h=h1+h2
                    elif i==14:
                        mi1=date_a_comparer[i]
                    elif i==15:
                        mi2=date_a_comparer[i]
                        mi=mi1+mi2
                else:
                    lh['text']="Erreur sur les chiffres!"
                    bon = False
                    break
    else:
        lh['text']="Erreur sur la saisie!" 
        bon = False   
    y = int(y)
    j = int(j)
    m = int(m)
    h = int(h)
    mi = int(mi)
    if m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12:
        if j>31:
            bon=False
    elif m==2 and y%4==0:
        if j>29:
            bon=False
    elif m==2 and y%4!=0:
        if j>28:
            bon=False
    else:
        if j>30:
            bon=False       
    if m>12:
        bon=False
    if h>23 or h<0:
        bon = False
    if mi>59 or mi<0:
        bon = False
    if not bon:      
        lh['text']="La date saisie est impossible!"
    else:
        lh['text']="Date valide."
        return True
#-----------------------------------------   
def comparer_dates(x,y):
    if x[6:10]==y[6:10]:
        if x[3:5]==y[3:5]:
            if x[0:2] == y[0:2]:
                if x[11:13]==y[11:13]:
                    if x[14:] == y[14:]:
                        lh['text']="Les deux dates\nsont égales!"
                        return False
                    elif x[14:] > y[14:]:
                        lh['text']="La minute de début est \nplus grande que celle de fin!"
                        return False
                elif x[11:13] > y[11:13]:
                    lh['text']="l'heure de début est \nplus grande que celle de fin!"
                    return False
            elif x[0:2] > y[0:2]:
                lh['text']="Le jour de début est \nplus grand que celui de fin!"
                return False
        elif x[3:5]>y[3:5]:
            lh['text']="Le mois de début est \nplus grand que celui de fin!"
            return False
    elif x[6:10] > y[6:10]:
        lh['text']="L'année de début est \nplus grande que celle de fin!"
        return False                 
    return True
#-----------------------------------------
def ajouter():
    automatique()
    l['text']=""
    lh['text']=""
    date_debut=ddvar.get()
    date_fin=dfvar.get()
    heure_debut=hdvar.get()
    heure_fin=hfvar.get()
    horaire_debut=date_debut+" "+heure_debut
    horaire_fin=date_fin+" "+heure_fin
    if (verifier_la_date(horaire_debut) and verifier_la_date(horaire_fin)) and comparer_dates(horaire_debut,horaire_fin):
        for i in mylist.curselection():
            prof_a_ajouter = mylist.get(i)+"\n"
            with open ("profabsents.txt","r") as f:
                data = f.readlines()
            if prof_a_ajouter in data:
                if prof_a_ajouter[0:3]=="Mme":
                    genre="ajoutée"
                else:
                    genre="ajouté"
                texte = prof_a_ajouter+"est déjà "+genre+"!"
                l['text']=texte 
            else:
                f = open("profabsents.txt", "a")
                f.write(prof_a_ajouter)
                f.close()
                if prof_a_ajouter[0:3]=="Mme":
                    genre="ajoutée"
                else:
                    genre="ajouté"
                texte = prof_a_ajouter+"a correctement été "+genre+"."
                for i in range(len(horaire_debut)-1):
                    if horaire_debut[i]=="/":
                        horaire_debut=horaire_debut.replace("/","-")
                horaire_debut+="\n"
                f = open("datedebut.txt", "a")
                f.write(horaire_debut)
                f.close()
                for i in range(len(horaire_fin)-1):
                    if horaire_fin[i]=="/":
                        horaire_fin=horaire_fin.replace("/","-")
                horaire_fin+="\n"
                f = open("datefin.txt", "a")
                f.write(horaire_fin)
                f.close()
                l['text']=texte     
#----------------------------------------- 
def retirer():
    automatique()
    l['text']=""
    lh['text']=""
    for i in mylist.curselection():
        prof_a_retirer = mylist.get(i)+"\n"
        with open ("profabsents.txt","r") as f:
            data = f.readlines()
        if prof_a_retirer not in data:
            if prof_a_retirer[0:3]=="Mme":
                genre="ajoutée"
            else:
                genre="ajouté"
            texte=prof_a_retirer+"n'est pas "+genre+"!"
            l['text']=texte
        else:
            compteur=0
            ligneasupprimer=0
            prof_a_retirer=prof_a_retirer.replace("\n","")
            with open ("profabsents.txt","w") as f:
                for line in data:
                    if line.strip("\n")!=prof_a_retirer:
                        f.write(line)
                        compteur+=1
                    else:
                        ligneasupprimer=compteur
            with open("datedebut.txt", "r") as infile:
                lines = infile.readlines()
            compteur=0
            with open("datedebut.txt", "w") as outfile:
                for line in lines:
                    if compteur != ligneasupprimer:
                        outfile.write(line)
                    compteur+=1
            with open("datefin.txt", "r") as infile:
                lines = infile.readlines()
            compteur=0
            with open("datefin.txt", "w") as outfile:
                for line in lines:
                    if compteur != ligneasupprimer:
                        outfile.write(line)
                    compteur+=1
                    if prof_a_retirer[0:3]=="Mme":
                        genre="retirée"
                    else:
                        genre="retiré"
                    texte = prof_a_retirer+" \na correctement été "+genre+"."
                    l['text']=texte  
#----------------------------------------- 
def effacer():
    automatique()
    l['text']=""
    lh['text']=""
    MsgBox = messagebox.askquestion ('Tout effacer','Êtes-vous sûr de tout vouloir effacer?',icon = 'warning')
    if MsgBox == 'yes':
        f = open('profabsents.txt', 'r+')
        f.truncate(0)
        f.close()
        f = open('datedebut.txt', 'r+')
        f.truncate(0)
        f.close()
        f = open('datefin.txt', 'r+')
        f.truncate(0)
        f.close()
        l['text']="Tout a correctement \nété effacé."
#-----------------------------------------   
def actu():
    automatique()
    l['text']=""
    lh['text']=""
#-----------------------------------------    
btna = TkinterCustomButton(bg_color=None,fg_color="#5fc96f",hover_color="#4e9458",text_font=None,text="Ajouter",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=ajouter)
btna.grid(row=4, column=3)
#----------------------------------------- 
btnr = TkinterCustomButton(bg_color=None,fg_color="#a8434a",hover_color="#823c41",text_font=None,text="Retirer",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=retirer)
btnr.grid(row=4,column=5)
#----------------------------------------- 
btne = TkinterCustomButton(bg_color=None,fg_color="#ffffff",hover_color="#a8a8a8",text_font=None,text="Tout effacer",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=effacer)
btne.grid(row=5,column=5)
#----------------------------------------- 
btno = TkinterCustomButton(bg_color=None,fg_color="#5d7fc9",hover_color="#51699e",text_font=None,text="Actualiser",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=actu)
btno.grid(row=5,column=3)
#----------------------------------------- 
test = ImageTk.PhotoImage(file="Logo.png")
label1 = Label(image=test)
label1.image = test
label1.grid(row=7, column=3, columnspan = 4,pady = 5, padx = 5)
#----------------------------------------- 
root.resizable(False, False) 
root.mainloop()
