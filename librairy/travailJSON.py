import json

class jsonWork : 
    def __init__(self,file):
        self.fichier = file
        
    def lectureJSON(self,flag): # Permet de lire la valeur du flag defini a l'appel de la fonction
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            dict = json.load(openfile)[flag]
        return str(dict)
    
    def lectureJSONMultiFlag(self,flag1,flag2):
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            dict = json.load(openfile)[flag1][flag2]
        return str(dict)
    
    def lectureJSONList(self,flag):
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            liste = json.load(openfile)[flag]
        return list(liste)
    
    def lectureJSONDict(self,flag):
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            dictionnaire = json.load(openfile)[flag]
        return dict(dictionnaire)
     
    def EcritureJSON(self,flag,valeur):#Permet d'ecrire une nouvelle valeur a flag definie
        openfile = open(self.fichier, 'r' , encoding='utf-8')
        dict = json.load(openfile)
        openfile.close()
        writeFile = open(self.fichier, 'w', encoding='utf-8')
        dict[flag] = valeur
        json.dump(dict,writeFile,indent=2)
    
    def dictJson(self):
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            dict = json.load(openfile)
        return dict
       
    def compteurFlagJSON(self):
        openfile = open(self.fichier, 'r' , encoding='utf-8')
        dict = json.load(openfile)
        openfile.close()
        return len(dict)
    
    def supprDictReorg(self,flag):
        with open(self.fichier, 'r' , encoding='utf-8') as openfile:
            dict = json.load(openfile)
            del dict[flag]
            newDict = {}
            newKey = 0
            for cle in sorted(dict.keys(), key=lambda x: int(x)):
                newDict[str(newKey)] = dict[cle]
                newKey += 1
            writeFile = open(self.fichier, 'w', encoding='utf-8')
            json.dump(newDict,writeFile,indent=2)
            writeFile.close()