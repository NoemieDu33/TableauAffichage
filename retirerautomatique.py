import os
def automatique():
    while os.path.getsize("retirerauto.txt"):
        print(os.path.getsize("retirerauto.txt"))
        with open ("retirerauto.txt","r") as f:
            prof = f.readlines()
        prof_a_retirer = prof[0]
        with open ("profabsents.txt","r") as f:
            data = f.readlines()
        compteur=0
        ligneasupprimer=0
        prof_a_retirer=prof_a_retirer.replace("\n","")
        with open ("retirerauto.txt","w") as f:
            for line in prof:
                if line.strip("\n")!=prof_a_retirer:
                    f.write(line)
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
    print('Réussi! - retirerauto ')
    data = []
    with open("profabsents.txt","r") as f:
        data = f.readlines()
        para = 000
    with open("parametres.txt","r") as w:
        para = w.readlines()[0]
    with open("parametres.txt","w") as w:
        w.write(para[0])
        w.write(para[1])
        print(len(data))
        if len(data)<10:
            w.write("0")
        elif len(data)>25 and len(data)<=29:
            w.write("2")
        elif len(data)>29:
            w.write("3")
        else:
            w.write("1")
        
    print('Réussi! - parametres ')
