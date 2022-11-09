from tkinter import*
import webbrowser
from ModuleInternet import TestInternet
import requests
import geocoder
from time import*

#Constante
Color = "#3c0f14"
TextColor = "white"
#Var api 
keyMeteo="ecffd157b2cc9eacbd0d35a45c3dc047"
urlMeteo="https://api.openweathermap.org/data/2.5/weather?"
urlGeoLoc = "http://api.ipstack.com/check"
keyGeoLoc = "b8f00cfb49bfdaf40a317f98314ddc63"
textTemperature = "Temperature: "
textHumiditer = "Taux d'humidité : "
urlNew = "https://newsapi.org/v2/top-headlines?sources=google-news-fr"
keyNew = "3b43e18afcf945888748071d177b8513"
nombrePage = "4"
#Fonction
def Ecriture(file,text):#Fonction d'écriture sur un fichier texte
    doc = open(file,"w")
    doc.truncate()
    doc.write(text)
    doc.close()
    return text,file
def Lecture(file):#Fonction de lecture d'un fichier texte et stokage dans une varriable
    fichier = open(file,"r")
    contenu= fichier.readlines()[0]
    fichier.close()
    return contenu
def FoncModif(file):
    Contenu = Lecture(file)
    ScreenModif = Toplevel()
    ScreenModif.maxsize(300,150)
    ScreenModif.minsize(300,150)
    ScreenModif.wait_visibility(ScreenModif)
    ScreenModif.wm_attributes('-alpha',0.9)
    ScreenModif.config(bg=Color)
    LabelContenu = Label(ScreenModif,text=Contenu,font=("arial","20"),bg=Color,fg=TextColor).pack()
    entry = Entry(ScreenModif)
    def Modif():
        Var = str(entry.get())
        Ecriture(file,Var)
        ScreenModif.destroy()
    modif = Button(ScreenModif,text="Modifier",bg=Color,fg=TextColor,command=Modif).pack(side="right",anchor="s")
    entry.pack(side="left",anchor="s")
def Parametre():
    screenPara = Toplevel()
    def Ville():
        FoncModif("config/ville.txt")
    screenPara.title("Arrera Info")
    screenPara.minsize(200,100)
    screenPara.maxsize(200,100)
    screenPara.config(bg=Color)
    boutonVille = Button(screenPara,text="Localisation domicile",bg=Color,fg=TextColor,font=("arial","15"),command=Ville).pack(side="left") 
def Geoloc():
    myPublic_IP = requests.get("http://wtfismyip.com/text").text.strip()
    ip = geocoder.ip(myPublic_IP)
    loc = ip.latlng
    lat = str(loc[0])
    long = str(loc[1])
    return lat , long
def MeteoLoc():
    lat , long  = Geoloc()
    ReponseTemp = requests.get(urlMeteo+"appid="+keyMeteo+"&lat="+lat+"&lon="+long+"&lang=fr"+"&units=metric").json()
    if ReponseTemp['cod'] == 404 :
        ville = input("Entrer votre ville : ")
        ReponseTemp = requests.get(urlMeteo+"appid="+keyMeteo+"&q="+ville+"&lang=fr"+"&units=metric").json()
        return "none" ,"none","none"
    else :
       temperature = str(ReponseTemp['main']['temp']) 
       humiditer = str(ReponseTemp['main']['humidity'])
       code = ReponseTemp['weather'][0]['icon'] 
       icon = "weather/"+code+".png"
       return temperature ,humiditer,icon
def MeteoDomicile():
    ville = Lecture("config/ville.txt")
    ReponseTemp = requests.get(urlMeteo+"appid="+keyMeteo+"&q="+ville+"&lang=fr"+"&units=metric").json()
    if ReponseTemp['cod'] == 404 :
        ville = input("Entrer votre ville : ")
        ReponseTemp = requests.get(urlMeteo+"appid="+keyMeteo+"&q="+ville+"&lang=fr"+"&units=metric").json()
        return "none" ,"none","none"
    else :
       temperature = str(ReponseTemp['main']['temp']) 
       humiditer = str(ReponseTemp['main']['humidity'])
       code = ReponseTemp['weather'][0]['icon'] 
       icon = "weather/"+code+".png"
       return temperature ,humiditer,icon
def Netoyage(dictionnnaire):
    url= dictionnnaire["url"]
    titre = dictionnnaire["title"]
    return url,titre
def Actu():
    CompleteURLNew = urlNew+"&pageSize="+nombrePage+"&apiKey="+keyNew
    article = requests.get(CompleteURLNew).json()["articles"]
    url1,titreFull1 = Netoyage(article[0])
    url2,titreFull2 = Netoyage(article[1])
    url3,titreFull3 = Netoyage(article[2])
    url4,titreFull4 = Netoyage(article[3])
    titre1Part1 = titreFull1[:len(titreFull1)//2]
    titre1Part2 = titreFull1[len(titreFull1)//2:]
    titre2Part1 = titreFull2[:len(titreFull2)//2]
    titre2Part2 = titreFull2[len(titreFull2)//2:]
    titre3Part1 = titreFull3[:len(titreFull3)//2]
    titre3Part2 = titreFull3[len(titreFull3)//2:]
    titre4Part1 = titreFull4[:len(titreFull4)//2]
    titre4Part2 = titreFull4[len(titreFull4)//2:]
    return url1,titre1Part1,titre1Part2,url2,titre2Part1,titre2Part2,url3,titre3Part1,titre3Part2,url4,titre4Part1,titre4Part2
#Fenetre tkinter
screen = Tk()
screen.title("Arrera Info")
screen.minsize(600,750)
screen.maxsize(600,750)
screen.config(bg=Color)
screen.iconphoto(False,PhotoImage(file="image/icon.png"))
#Var image
iconParametre = PhotoImage(file="image/iconParametre.png")
iconActulisation = PhotoImage(file="image/iconActualisation.png")
#Definition des cadre
cadreMeteoLoc = Frame(screen,bg=Color,width=250,height=240)
cadreMeteoDomicile = Frame(screen,bg=Color,width=250,height=240)
cadreCentral = Frame(screen,bg=Color,width=550,height=355)
#MeteoLoc
labelInfoLoc = Label(cadreMeteoLoc,text="A votre localisation",bg=Color,fg=TextColor,font=("arial","15"))
labelTemperatureLoc = Label(cadreMeteoLoc,text=textTemperature,bg=Color,fg=TextColor,font=("arial","15"))
labelTempLoc = Label(cadreMeteoLoc)
labelHumiditerLoc = Label(cadreMeteoLoc,text=textHumiditer,bg=Color,fg=TextColor,font=("arial","15"))
#Meteo Domicile
labelInfoDomicile = Label(cadreMeteoDomicile,text="Chez vous",bg=Color,fg=TextColor,font=("arial","15"))
labelTemperatureDomicile = Label(cadreMeteoDomicile,text=textTemperature,bg=Color,fg=TextColor,font=("arial","15"))
labelTempDomicile = Label(cadreMeteoDomicile)
labelHumiditerDomicile = Label(cadreMeteoDomicile,text=textHumiditer,bg=Color,fg=TextColor,font=("arial","15"))
#Cadre central
boutonActu1 = Button(cadreCentral,bg=Color,fg=TextColor,font=("arial","10"))
boutonActu2 = Button(cadreCentral,bg=Color,fg=TextColor,font=("arial","10"))
boutonActu3 = Button(cadreCentral,bg=Color,fg=TextColor,font=("arial","10"))
boutonActu4 = Button(cadreCentral,bg=Color,fg=TextColor,font=("arial","10"))
#fonction widge
def Widget():
    etatInternet = TestInternet()
    if etatInternet == True:
        labelInternet.place_forget()
        cadreMeteoLoc.pack(side="left",anchor="n")
        cadreMeteoDomicile.pack(side="right",anchor="n")
        cadreCentral.place(relx=.5, rely=.5, anchor="n")
        temperatureLoc , humiditerLoc , descriptionLoc = MeteoLoc()
        temperatureDomicile ,humiditerDomicile , descriptionDomicile = MeteoDomicile()
        url1,titre1Part1,titre1Part2,url2,titre2Part1,titre2Part2,url3,titre3Part1,titre3Part2,url4,titre4Part1,titre4Part2 = Actu()
        iconDomicile = PhotoImage(file=descriptionDomicile)
        iconLoc = PhotoImage(file=descriptionLoc)
        labelTempDomicile.image_names = iconDomicile
        labelTempLoc.image_names = iconLoc
        labelTempLoc.config(image = iconLoc ,bg=Color )
        labelTempDomicile.config(image=iconDomicile,bg=Color)
        labelTemperatureLoc.config(text=textTemperature+temperatureLoc+" °C")
        labelHumiditerLoc.config(text=textHumiditer+humiditerLoc+" %")
        labelHumiditerDomicile.config(text=textHumiditer+humiditerDomicile+" %")
        labelTemperatureDomicile.config(text=textTemperature+temperatureDomicile+" °C")
        def Actu1():
            webbrowser.open(url1)
        def Actu2():
            webbrowser.open(url2)
        def Actu3():
            webbrowser.open(url3)
        def Actu4():
            webbrowser.open(url4)
        boutonActu1.config(text=titre1Part1+"\n"+titre1Part2,command=Actu1)
        boutonActu2.config(text=titre2Part1+"\n"+titre2Part2,command=Actu2)
        boutonActu3.config(text=titre3Part1+"\n"+titre3Part2,command=Actu3)
        boutonActu4.config(text=titre4Part1+"\n"+titre4Part2,command=Actu4)
    else :
        cadreMeteoLoc.pack_forget()
        cadreMeteoDomicile.pack_forget()
        cadreCentral.place_forget()
        labelInternet.place(relx=.5, rely=.5, anchor="center")

#Fenetre
labelInternet = Label(screen,text="Internet n'est pas\nDisponible",bg=Color,fg=TextColor,font=("arial","25"))
boutonActualisation = Button(screen,image=iconActulisation,bg=Color,command=Widget)
boutonPara = Button(screen,image=iconParametre,bg=Color,command=Parametre)
#affichage
boutonPara.place(x="0",y="690")
boutonActualisation.place(x="545",y="690")
cadreMeteoLoc.pack(side="left",anchor="n")
cadreMeteoDomicile.pack(side="right",anchor="n")
cadreCentral.place(relx=.5, rely=.5, anchor="n")

#Cadre meteo Loc
labelInfoLoc.place(x="0",y="0")
labelTemperatureLoc.place(x="0",y="35")
labelTempLoc.place(relx=.5, rely=.5, anchor="center") 
labelHumiditerLoc.place(x="0",y="210")
#Cadre meteo Domicile
labelInfoDomicile.place(x="0",y="0")
labelTemperatureDomicile.place(x="0",y="35")
labelTempDomicile.place(relx=.5, rely=.5, anchor="center") 
labelHumiditerDomicile.place(x="0",y="210")
#Cadre central
boutonActu1.place(x="3",y="5")
boutonActu2.place(x="3",y="65")
boutonActu3.place(x="3",y="125")
boutonActu4.place(x="3",y="185")
Widget()
screen.mainloop()