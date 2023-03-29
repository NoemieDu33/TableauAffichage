from time import sleep
from tkinter import *
from tkinter import messagebox, ttk
import os
from tkinter import filedialog
import sys
from distutils.version import StrictVersion as Version
from tkinter_custom_button import TkinterCustomButton
import pickle
from random import randint
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import shutil
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from pathlib import Path
from retirerautomatique import automatique
#-----------------------------------------
root = Tk()
root.geometry("620x400")
root.configure(background="#1f1f1f")
#-----------------------------------------
en_tete = Label(root, text ='Modifier l\'affichage',font = "50") 
en_tete.configure(background="#1f1f1f", foreground='white')
en_tete.grid(row=0, column=0, rowspan = 2) 
#-----------------------------------------  
hlist = ["","1: Image","2: Dernière image utilisée","3: Texte"]
tlist = ["","1: Sombre","2: Dégradé Bleu Clair","3: Fancy","4: À venir... (Ne cliquez pas)"]
#-----------------------------------------  
tdvar = ttk.Combobox(root, values = tlist)
tdvar.set("Thème")
tdvar.grid(row=3, column=4, padx=5, pady=5)
#-----------------------------------------  
hdvar = ttk.Combobox(root, values = hlist)
hdvar.set("Type d'affichage")
hdvar.grid(row=3, column=3, padx=5, pady=5)
#-----------------------------------------  
T = Text(root, height = 10, width = 5)
l = Label(root, text = "")
l.configure(background="#1f1f1f", foreground='white')
l.grid(row = 7, column = 3, columnspan = 2, pady=5)
#-----------------------------------------   
def changer():
    l['text']=''
    changement_theme=False
    changement_affi=False
    automatique()
    theme = tdvar.get()
    if theme!="Thème" and theme!="":
        theme = theme[0]
        changement_theme=True
    choix = hdvar.get()
    if choix!="Type d'affichage" and choix!="":
        choix = choix[0]
        changement_affi=True
    with open('parametres.txt','r') as f:
        data=f.readlines()
        global sauvegardetheme
        global sauvegardechoix
        data = data[0]
        print(len(data))
        print(data)
        if len(data)>1 and (data[0]=='1' or data[0]=='2' or data[0]=='3'):
            sauvegardechoix=data[0]
        sauvegardetheme = data[1]
        if changement_theme:
            if sauvegardetheme == theme:
                l['text']="Le thème est déjà appliqué!"
                return
            sauvegardetheme=theme
            with open('parametres.txt','r') as f:
                verif = f.readlines()
                if changement_theme and not changement_affi:
                    l['text']='Changement de thème réussi!'
        if changement_affi:
            if choix=='1':
                filename = filedialog.askopenfilename(initialdir = "/",title = "Choisir l'image à afficher",
                filetypes = (("Image PNG","*.png*"),("Image JPG","*.jpg*"),("Fichier PDF","*.pdf")))
                if filename == "":
                    l['text']="Aucun fichier n'a\nété sélectionné!"
                    return    
                l['text']="Fichier choisi: \n"+filename
                if os.path.exists('image/image.png'):
                    os.remove('image/image.png')
                elif os.path.exists('image/image.jpg'):
                    os.remove('image/image.jpg')
                elif os.path.exists('image/image.pdf'):
                    os.remove('image/image.pdf')
                shutil.copy(filename,'image',follow_symlinks=True)
                dir_list = os.listdir('image')
                nom_fichier=dir_list[0] #--------------------------------------!
                old_file = os.path.join('image', nom_fichier)
                if ".png" in nom_fichier:
                    new_file = os.path.join('image', "image.png")
                    os.rename(old_file, new_file)
                elif ".jpg" in nom_fichier:
                    new_file = os.path.join('image', "image.jpg")
                    os.rename(old_file, new_file)
                    os.chdir('image')
                    img = Image.open("image.jpg")
                    img.save("image.png")
                    os.remove("image.jpg")
                    os.chdir('../')
                elif ".pdf" in nom_fichier:
                    new_file = os.path.join('image', "image.pdf")
                    os.rename(old_file, new_file)
                    os.chdir('image')
                    images = convert_from_path('image.pdf')
                    for i in range(len(images)):
                        images[i].save('image.png', 'PNG')
                    os.remove("image.pdf")
                    os.chdir('../')
                else:
                    l['text']='Erreur! Vérifiez le format de fichier (.png ou .jpg valide)'
                os.chdir('image')
                file_path = Path('image.png')
                print(file_path)
                os.chdir('../')
                if not changement_theme:
                    l['text']='Changement de l\'affichage réussi!'
                else:
                    l['text']='Changements réussis!'
            elif choix=='2':
                sauvegardechoix = 2
                if not changement_theme:
                    l['text']='Changement de l\'affichage réussi!'
                else:
                    l['text']='Changements réussis!'
            elif choix=='3':
                os.system('notepad.exe image/texte.txt')
                if os.path.getsize("image/texte.txt")!=0:
                    if not changement_theme:
                        l['text']='Changement de l\'affichage réussi!'
                    else:
                        l['text']='Changements réussis!'
                else:
                    l['text']="Le fichier texte est vide!"
            else:
                l['text']='Il y a eu un problème avec le choix...'
            sauvegardechoix = choix
    para3=0
    with open("parametres.txt","r") as w:
        para3 = int(w.readlines()[0][2])
    with open('parametres.txt','w') as f:
        f.write(sauvegardechoix)
        f.write(sauvegardetheme)
        f.write(str(para3))
        f.close()


#-----------------------------------------  
btna = TkinterCustomButton(bg_color=None,fg_color="#5fc96f",hover_color="#4e9458",text_font=None,text="Mettre à jour",
text_color="black",corner_radius=0,width=120,height=40,hover=True,command=changer)
btna.grid(row=4, column=3, columnspan = 2, pady = 20)
#----------------------------------------- 
test = ImageTk.PhotoImage(file="Logo.png")
label1 = Label(image=test)
label1.image = test
label1.grid(row=8, column=2, columnspan = 4,rowspan = 3,pady = 5, padx = 5)
#----------------------------------------- 
root.resizable(False, False) 
root.mainloop()
