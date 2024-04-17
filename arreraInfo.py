from tkinter import*
import webbrowser
from ModuleInternet import TestInternet
from librairy.travailJSON import*
import requests
import geocoder
from time import*
from PIL import Image, ImageTk


class PArreraInfo :
    def __init__(self) -> None:
        #Constante
        self.__color = "white"
        self.__textColor = "black"
        #Fichier de config
        self.__configFile = jsonWork("config/config.json")
        #Var api 
        self.__keyMeteo="ecffd157b2cc9eacbd0d35a45c3dc047"
        self.__urlMeteo="https://api.openweathermap.org/data/2.5/weather?"
        self.__urlGeoLoc = "http://api.ipstack.com/check"
        self.__keyGeoLoc = "b8f00cfb49bfdaf40a317f98314ddc63"
        self.__textTemperature = "Temperature: "
        self.__textHumiditer = "Taux d'humidité : "
        self.__urlNew = "https://newsapi.org/v2/top-headlines?sources=google-news-fr"
        self.__keyNew = "3b43e18afcf945888748071d177b8513"
        self.__nombrePage = "4"
        #Fenetre tkinter
        self.__screen = Tk()
        self.__screen.title("Arrera Info")
        self.__screen.minsize(600,750)
        self.__screen.maxsize(600,750)
        self.__screen.config(bg=self.__color)
        self.__screen.iconphoto(False,PhotoImage(file="image/icon.png"))
        #Menu
        menu = Menu(self.__screen)
        menu.add_command(label="A propos",command=self.__apropop)
        self.__screen.configure(menu=menu)
        #Bouton Parametre et actualisation
        self.__boutonActualisation = Button(self.__screen,bg=self.__color,command=self.__widget)
        iconActulisation = PhotoImage(file="image/iconActualisation.png",master=self.__boutonActualisation)
        self.__boutonActualisation.image_names=iconActulisation
        self.__boutonActualisation.configure(image=iconActulisation)
        self.__boutonPara = Button(self.__screen,bg=self.__color,command=self.setting)
        iconParametre = PhotoImage(file="image/iconParametre.png",master=self.__boutonPara)
        self.__boutonPara.image_names = iconParametre
        self.__boutonPara.configure(image=iconParametre)
        #Definition des cadre
        self.__cadreMeteoLoc = Frame(self.__screen,bg=self.__color,width=250,height=240)
        self.__cadreMeteoDomicile = Frame(self.__screen,bg=self.__color,width=250,height=240)
        self.__cadreCentral = Frame(self.__screen,bg=self.__color,width=550,height=315)
        self.__cadrePara = Frame(self.__screen,bg="blue",height=750,width=600)
        #MeteoLoc
        self.__labelInfoLoc = Label(self.__cadreMeteoLoc,text="A votre localisation",bg=self.__color,fg=self.__textColor,font=("arial","15"))
        self.__labelTemperatureLoc = Label(self.__cadreMeteoLoc,text=self.__textTemperature,bg=self.__color,fg=self.__textColor,font=("arial","15"))
        self.__labelTempLoc = Label(self.__cadreMeteoLoc)
        self.__labelHumiditerLoc = Label(self.__cadreMeteoLoc,text=self.__textHumiditer,bg=self.__color,fg=self.__textColor,font=("arial","15"))
        #Meteo Domicile
        self.__labelInfoDomicile = Label(self.__cadreMeteoDomicile,text="Chez vous",bg=self.__color,fg=self.__textColor,font=("arial","15"))
        self.__labelTemperatureDomicile = Label(self.__cadreMeteoDomicile,text=self.__textTemperature,bg=self.__color,fg=self.__textColor,font=("arial","15"))
        self.__labelTempDomicile = Label(self.__cadreMeteoDomicile)
        self.__labelHumiditerDomicile = Label(self.__cadreMeteoDomicile,text=self.__textHumiditer,bg=self.__color,fg=self.__textColor,font=("arial","15"))
        #Cadre central
        self.__boutonActu1 = Button(self.__cadreCentral,bg=self.__color,fg=self.__textColor,font=("arial","13"))
        self.__boutonActu2 = Button(self.__cadreCentral,bg=self.__color,fg=self.__textColor,font=("arial","13"))
        self.__boutonActu3 = Button(self.__cadreCentral,bg=self.__color,fg=self.__textColor,font=("arial","13"))
        self.__boutonActu4 = Button(self.__cadreCentral,bg=self.__color,fg=self.__textColor,font=("arial","13"))
        self.__labelInternet = Label(self.__screen,text="Internet n'est pas\nDisponible",bg=self.__color,fg=self.__textColor,font=("arial","25"))
        #Parametre
        self.__entryVille = Entry(self.__cadrePara,font=("arial","25"))
        self.__validerPara = Button(self.__cadrePara,text="Valider",font=("arial","15"),bg="green",fg="white",width=25,command=self.__validerSetting)
        self.__quitterPara = Button(self.__cadrePara,text="Retour",font=("arial","15"),bg="red",fg="white",width=25,command=self.disablePara)
        
    def show(self):
        #affichage
        self.__cadreMeteoLoc.pack(side="left",anchor="n")
        self.__cadreMeteoDomicile.pack(side="right",anchor="n")
        self.__cadreCentral.place(relx=.5, rely=.5, anchor="n")

        #Cadre meteo Loc
        self.__labelInfoLoc.place(x="0",y="0")
        self.__labelTemperatureLoc.place(x="0",y="35")
        self.__labelTempLoc.place(relx=.5, rely=.5, anchor="center") 
        self.__labelHumiditerLoc.place(x="0",y="210")
        #Cadre meteo Domicile
        self.__labelInfoDomicile.place(x="0",y="0")
        self.__labelTemperatureDomicile.place(x="0",y="35")
        self.__labelTempDomicile.place(relx=.5, rely=.5, anchor="center") 
        self.__labelHumiditerDomicile.place(x="0",y="210")
        #Cadre central
        self.__boutonActu1.place(x="3",y="5")
        self.__boutonActu2.place(x="3",y="65")
        self.__boutonActu3.place(x="3",y="125")
        self.__boutonActu4.place(x="3",y="185")
        self.__boutonActualisation.place(x="545",y="690")
        self.__boutonPara.place(x="0",y="690")
        self.__widget()
        self.__screen.mainloop()
    
    def disablePara(self):
        self.__cadrePara.pack_forget()
        self.show()

    def __widget(self):
        etatInternet = TestInternet()
        if etatInternet == True:
            self.__labelInternet.place_forget()
            self.__cadreMeteoLoc.pack(side="left",anchor="n")
            self.__cadreMeteoDomicile.pack(side="right",anchor="n")
            self.__cadreCentral.place(relx=.5, rely=.5, anchor="n")
            temperatureLoc , humiditerLoc , descriptionLoc = self.__meteoLoc()
            temperatureDomicile ,humiditerDomicile , descriptionDomicile = self.__meteoDomicile()
            url1,titre1Part1,titre1Part2,url2,titre2Part1,titre2Part2,url3,titre3Part1,titre3Part2,url4,titre4Part1,titre4Part2 = self.__actu()
            iconDomicile = PhotoImage(file=descriptionDomicile)
            iconLoc = PhotoImage(file=descriptionLoc)
            self.__labelTempDomicile.image_names = iconDomicile
            self.__labelTempLoc.image_names = iconLoc
            self.__labelTempLoc.config(image = iconLoc ,bg=self.__color )
            self.__labelTempDomicile.config(image=iconDomicile,bg=self.__color)
            self.__labelTemperatureLoc.config(text=self.__textTemperature+temperatureLoc+" °C")
            self.__labelHumiditerLoc.config(text=self.__textHumiditer+humiditerLoc+" %")
            self.__labelHumiditerDomicile.config(text=self.__textHumiditer+humiditerDomicile+" %")
            self.__labelTemperatureDomicile.config(text=self.__textTemperature+temperatureDomicile+" °C")
            self.__boutonActu1.config(text=titre1Part1+"\n"+titre1Part2,command=lambda :webbrowser.open(url1) )
            self.__boutonActu2.config(text=titre2Part1+"\n"+titre2Part2,command=lambda :webbrowser.open(url2))
            self.__boutonActu3.config(text=titre3Part1+"\n"+titre3Part2,command=lambda :webbrowser.open(url3))
            self.__boutonActu4.config(text=titre4Part1+"\n"+titre4Part2,command=lambda :webbrowser.open(url4))
        else :
            self.__cadreMeteoLoc.pack_forget()
            self.__cadreMeteoDomicile.pack_forget()
            self.__cadreCentral.place_forget()
            self.__labelInternet.place(relx=.5, rely=.5, anchor="center")
   
    def __geoloc(self):
        myPublic_IP = requests.get("http://wtfismyip.com/text").text.strip()
        ip = geocoder.ip(myPublic_IP)
        loc = ip.latlng
        lat = str(loc[0])
        long = str(loc[1])
        return lat , long
    
    def __meteoLoc(self):
        lat , long  = self.__geoloc()
        ReponseTemp = requests.get(self.__urlMeteo+"appid="+self.__keyMeteo+"&lat="+lat+"&lon="+long+"&lang=fr"+"&units=metric").json()
        if ReponseTemp['cod'] == 404 :
            return "none" ,"none","none"
        else :
            temperature = str(ReponseTemp['main']['temp']) 
            humiditer = str(ReponseTemp['main']['humidity'])
            code = ReponseTemp['weather'][0]['icon'] 
            icon = "weather/"+code+".png"
        return temperature ,humiditer,icon
    
    def __meteoDomicile(self):
        ville = self.__configFile.lectureJSON("ville")
        if (ville ==  ""):
            ville = "Paris"
        ReponseTemp = requests.get(self.__urlMeteo+"appid="+self.__keyMeteo+"&q="+ville+"&lang=fr"+"&units=metric").json()
        if ReponseTemp['cod'] == 404 :
            ville = input("Entrer votre ville : ")
            ReponseTemp = requests.get(self.__urlMeteo+"appid="+self.__keyMeteo+"&q="+ville+"&lang=fr"+"&units=metric").json()
            return "none" ,"none","none"
        else :
            temperature = str(ReponseTemp['main']['temp']) 
            humiditer = str(ReponseTemp['main']['humidity'])
            code = ReponseTemp['weather'][0]['icon'] 
            icon = "weather/"+code+".png"
        return temperature ,humiditer,icon
    
    def __netoyage(self,dictionnnaire):
        url= dictionnnaire["url"]
        titre = dictionnnaire["title"]
        return url,titre
    
    def __actu(self):
        CompleteURLNew = self.__urlNew+"&pageSize="+self.__nombrePage+"&apiKey="+self.__keyNew
        article = requests.get(CompleteURLNew).json()["articles"]
        url1,titreFull1 = self.__netoyage(article[0])
        url2,titreFull2 = self.__netoyage(article[1])
        url3,titreFull3 = self.__netoyage(article[2])
        url4,titreFull4 = self.__netoyage(article[3])
        titre1Part1 = titreFull1[:len(titreFull1)//2]
        titre1Part2 = titreFull1[len(titreFull1)//2:]
        titre2Part1 = titreFull2[:len(titreFull2)//2]
        titre2Part2 = titreFull2[len(titreFull2)//2:]
        titre3Part1 = titreFull3[:len(titreFull3)//2]
        titre3Part2 = titreFull3[len(titreFull3)//2:]
        titre4Part1 = titreFull4[:len(titreFull4)//2]
        titre4Part2 = titreFull4[len(titreFull4)//2:]
        return url1,titre1Part1,titre1Part2,url2,titre2Part1,titre2Part2,url3,titre3Part1,titre3Part2,url4,titre4Part1,titre4Part2

    def __apropop(self):
        #Variable
        nameApp = "Arrera Info"
        versionApp = "I2024-"
        imagePath = "image/icon.png"
        copyrightApp = "Copyright Arrera Software by Baptiste P 2023-2024"
        tailleIMG = (100,100)
        #Creation de la fenetre
        about = Toplevel()
        about.title("A propos :"+nameApp)
        about.maxsize(400,300)
        about.minsize(400,300)
        #Traitement Image
        imageOrigine = Image.open(imagePath)    
        imageRedim = imageOrigine.resize(tailleIMG)
        icon = ImageTk.PhotoImage(imageRedim)
        #Label
        labelIcon = Label(about,image=icon)
        labelName = Label(about,text="\n"+nameApp+"\n",font=("arial","12"))
        labelVersion = Label(about,text=versionApp+"\n",font=("arial","11"))
        labelCopyright = Label(about,text=copyrightApp,font=("arial","9"))
        #affichage
        labelIcon.pack()
        labelName.pack()
        labelVersion.pack()
        labelCopyright.pack()
        about.mainloop()
    
    def __lecture(self,file):#Fonction de lecture d'un fichier texte et stokage dans une varriable
        fichier = open(file,"r")
        contenu= fichier.readlines()[0]
        fichier.close()
        return contenu
    
    def setting(self):
        largeurFrame = self.__cadrePara.winfo_reqheight()
        labelTitre = Label(self.__cadrePara,text="Entrer votre domicile",font=("arial","15"),bg=self.__color,fg=self.__textColor)
        labelTitre.place(x=((largeurFrame-(labelTitre.winfo_reqwidth())//2)),y=25)
        self.__entryVille.place(x=(((largeurFrame-(self.__entryVille.winfo_reqwidth()))//2)-50),y=125)
        self.__validerPara.place(x=(((largeurFrame-(self.__validerPara.winfo_reqwidth()))//2)-50),y=225)
        self.__quitterPara.place(x=(((largeurFrame-(self.__quitterPara.winfo_reqwidth()))//2)-50),y=325)
        self.__cadreMeteoLoc.pack_forget()
        self.__cadreMeteoDomicile.pack_forget()
        self.__cadreCentral.pack_forget()
        self.__cadrePara.pack()
    
    def __validerSetting(self):
        ville = self.__entryVille.get()
        self.__entryVille.delete(0,END)
        self.__configFile.EcritureJSON("ville",ville)
        self.disablePara()       