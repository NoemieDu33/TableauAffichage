from tkinter import *
from tkinter import messagebox, ttk
import os
from tkinter import filedialog
import sys
from distutils.version import StrictVersion as Version
from tkinter_custom_button import TkinterCustomButton
import pickle
from random import randint
from PIL import Image, ImageTk
from retirerautomatique import automatique
#-----------------------------------------
root = Tk()
root.geometry("600x400")
root.configure(background="#1f1f1f")
#-----------------------------------------
en_tete = Label(root, text ='Modifier la liste des profs',font = "50") 
en_tete.configure(background="#1f1f1f", foreground='white')
en_tete.grid(row=0, column=0)
#-----------------------------------------  
nom_du_prof_strvar=StringVar()
ndp_entry = Entry(root,textvariable = nom_du_prof_strvar,width=30)
nom_du_prof_strvar.set("Entrer le nom du prof:")
ndp_entry.grid(row=2, column=3, padx=5, pady=5)
#-----------------------------------------
T = Text(root, height = 10, width = 5)
l = Label(root, text = "")
l.configure(background="#1f1f1f", foreground='white')
l.grid(row = 7, column = 3)
#-----------------------------------------   
def removeprefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string
#-----------------------------------------
def remove_gender_prefix(name):
    name = removeprefix(name, 'M. ')
    name = removeprefix(name, 'Mme. ')
    return name
#-----------------------------------------
def ajouter():
    automatique()
    with open('listfile.data', 'rb') as filehandle:
        listeprofs = pickle.load(filehandle)
    nom_du_prof = nom_du_prof_strvar.get()
    if not "Mme. " in nom_du_prof and not "M. " in nom_du_prof:
        l['text']="Il y a un problème!\nVérifie bien l'ortographe!"
        return
    if nom_du_prof[0:3]=="Mme":
        if not nom_du_prof[5:].isupper():
            nom_du_prof = nom_du_prof[0:5] + nom_du_prof[5:].upper()
        genre="ajoutée"
    else:
        if not nom_du_prof[3:].isupper():
            nom_du_prof = nom_du_prof[0:3] + nom_du_prof[3:].upper()
        genre="ajouté"
    if nom_du_prof not in listeprofs:
        texte = nom_du_prof+" \na correctement été "+genre+"." 
        listeprofs.append(nom_du_prof)
        listeprofs = sorted(listeprofs, key=remove_gender_prefix)
        with open('listfile.data', 'wb') as filehandle:
            pickle.dump(listeprofs, filehandle)
        print(listeprofs)
    else:
        texte = nom_du_prof+" est déjà "+genre+"!"
    l['text']=texte 
#----------------------------------------- 
def retirer():
    automatique()
    with open('listfile.data', 'rb') as f:
        listeprofs = pickle.load(f)
    nom_du_prof = nom_du_prof_strvar.get()
    if not "Mme. " in nom_du_prof and not "M. " in nom_du_prof:
        l['text']="Il y a un problème!\nVérifie bien l'ortographe!"
        return
    if nom_du_prof[0:3]=="Mme":
        if not nom_du_prof[5:].isupper():
            nom_du_prof = nom_du_prof[0:5] + nom_du_prof[5:].upper()
        genre="retirée"
    else:
        if not nom_du_prof[3:].isupper():
            nom_du_prof = nom_du_prof[0:3] + nom_du_prof[3:].upper()
        genre="retiré"
    if nom_du_prof in listeprofs:
        listeprofs.remove(nom_du_prof)
        with open('listfile.data', 'wb') as filehandle:
            pickle.dump(listeprofs, filehandle)
        print(listeprofs)
        texte = nom_du_prof+" \na correctement été "+genre+"."
    else:
        texte = nom_du_prof+" n'est pas "+genre+"!"
    l['text']=texte 
#-----------------------------------------   
def afficher():
    automatique()
    with open('listfile.data', 'rb') as f:
        listeprofs = pickle.load(f)
    with open('liste_dump.txt','w') as f:
        for element in listeprofs:
            element+="\n"
            f.write(element)
    os.system("notepad.exe liste_dump.txt")
    l['text']=""
#-----------------------------------------    
btna = TkinterCustomButton(bg_color=None,fg_color="#5fc96f",hover_color="#4e9458",text_font=None,text="Ajouter",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=ajouter)
btna.grid(row=4, column=3)
#----------------------------------------- 
btnr = TkinterCustomButton(bg_color=None,fg_color="#a8434a",hover_color="#823c41",text_font=None,text="Retirer",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=retirer)
btnr.grid(row=5,column=3)
#----------------------------------------- 
btno = TkinterCustomButton(bg_color=None,fg_color="#5d7fc9",hover_color="#51699e",text_font=None,text="Ouvrir la liste",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=afficher)
btno.grid(row=6,column=3)
#----------------------------------------- 
test = ImageTk.PhotoImage(file="Logo.png")
label1 = Label(image=test)
label1.image = test
label1.grid(row=8, column=3,pady = 5, padx = 5)
#----------------------------------------- 
root.resizable(False, False) 
root.mainloop()
