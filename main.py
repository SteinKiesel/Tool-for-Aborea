import tkinter as tk
from tkinter import messagebox
import numpy as np
import os


class Hauptfenster:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='Charakter erstellen', width=25, command=self.charakterErstellung)
        self.button2 = tk.Button(self.frame, text='Charakter laden', width=25, command=self.charakterLaden)
        self.button3 = tk.Button(self.frame, text='Schließen', width=25, command=self.master.destroy)
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.frame.pack()

    def charakterErstellung(self):
        self.newWindow_chErstellung = tk.Toplevel(self.master)
        self.newWindow_chErstellung.title('Charaktererstellung')
        self.app_chErstellung = Charaktererstellung(self.newWindow_chErstellung)

    def charakterLaden(self):
        self.newWindow_chLaden = tk.Toplevel(self.master)
        self.newWindow_chLaden.title('Übersicht aller Charaktere')
        self.app_chLaden = CharakterLadenMenue(self.newWindow_chLaden)


class CharakterLadenMenue:
    def __init__(self, master):
        self.master=master
        self.master.config()
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        self.charakterListe = []

        self.CharaktereFrame = tk.LabelFrame(self.frame, text='Liste der verfügbaren Charakteren', bd=5, relief='ridge')
        self.CharaktereFrame.grid(row=0, column=0, padx=20, pady=20)

        # Canvas hinzufügen ins Frame
        self.canvas = tk.Canvas(self.CharaktereFrame)
        self.canvas.grid(row=0, column=0)

        # Vertikale Scroll-Leiste aufs Canvas bezogen
        vsbar = tk.Scrollbar(self.CharaktereFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)

        # Frame auf Canvas erschaffen für die Oberfläche
        self.CharaktereF_c = tk.Frame(self.canvas)

        # Einzelnen Charaktere hinzufügen
        self.CharaktereGesamt, self.AnzahlCharaktere = self.laden()
        # aufbauen der Charaktere
        self.aufbauCharakterauswahl(self.CharaktereF_c, self.CharaktereGesamt, self.AnzahlCharaktere)

        # Fenster erschaffen, der alle Objekte hält
        self.canvas.create_window((0,0), window=self.CharaktereF_c, anchor=tk.NW)

        # keine Ahnung was hier passiert
        self.CharaktereF_c.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        self.canvas.configure(scrollregion=bbox, width=550, height=200)

        # Beendenbutton
        self.Button_Beenden = tk.Button(self.frame, text='Beenden', command=self.master.destroy)
        self.Button_Beenden.grid(row=1, column=0)

    def laden(self):
        # initialisieren der gebrauchten Variablen
        listCharaktereGesamt=[] #wird zu einer Matrix der Dimension 3, 1 Dim->Charaktere, 2 Dim -> Eigenschaften, 3 Dim ->Untereigenschaften
        anzahlCharaktere = 0
        # charaktere reinladen
        path =os.getcwd()
        charaktere = next(os.walk(path+'\\charaktere'))[2]
        # charaktere auslesen und in Format bringen
        j=0
        for charakter in charaktere:
            with open(path+'\\charaktere\\'+charakter,'r') as f:
                charakterGesamt = f.read().splitlines()
                # leere text Datein löschen
                if charakterGesamt==[]:
                    f.close()
                    os.remove(path+'\\charaktere\\'+charakter)
                    continue
                f.close()
            # die Liste in geeignetes Format bringen
            i=0
            for zeile in charakterGesamt:
                zeile = zeile.split(', ')
                charakterGesamt[i] = zeile
                i+=1
            listCharaktereGesamt.append(charakterGesamt)
            j+=1
        anzahlCharaktere = j
        # Ausgabe der Gesamtliste der Charaktere, sowie der gesamtanzahl
        return listCharaktereGesamt, anzahlCharaktere

    def aufbauCharakterauswahl(self,master, charaktereGesamt, anzahlCharaktere):
        # in der Schleife wird jeder Charakter projeziert in das GUI
        aktuelleZeile = 0
        for zaehler in range(0,anzahlCharaktere):
            # Aufbau der Elemente
            self.Label_Spielername = tk.Label(master, text=charaktereGesamt[aktuelleZeile][0][0])
            self.Label_Charaktername = tk.Label(master, text=charaktereGesamt[aktuelleZeile][1][0])
            self.Label_Volk = tk.Label(master, text=charaktereGesamt[aktuelleZeile][2][0])
            self.Label_Klasse = tk.Label(master, text=charaktereGesamt[aktuelleZeile][3][0])
            self.Label_Stufe = tk.Label(master, text=charaktereGesamt[aktuelleZeile][4][0])
            self.Button_Laden = tk.Button(master, text='Laden', command=lambda zeile=aktuelleZeile: self.charakterladen(zeile))

            self.Label_Spielername.grid(row=aktuelleZeile,column=0)
            self.Label_Charaktername.grid(row=aktuelleZeile,column=1)
            self.Label_Volk.grid(row=aktuelleZeile,column=2)
            self.Label_Klasse.grid(row=aktuelleZeile,column=3)
            self.Label_Stufe.grid(row=aktuelleZeile,column=4)
            self.Button_Laden.grid(row=aktuelleZeile,column=5)

            self.charakterListe.append([
                self.Label_Spielername,
                self.Label_Charaktername,
                self.Label_Volk,
                self.Label_Klasse,
                self.Button_Laden,
                ])
            aktuelleZeile +=1

    def charakterladen(self, zeile):
        self.newWindow_chLaden = tk.Toplevel(self.frame)
        self.newWindow_chLaden.title(self.CharaktereGesamt[zeile][1][0])
        self.app_chLaden = CharakterLaden(self.newWindow_chLaden, self.CharaktereGesamt[zeile])


class CharakterLaden:
    def __init__(self, master, CharakterGesamt):
        # Hilfsvaribalen
        self.Fertigkeitsliste_Objekte =[]
        self.Fertigkeitsliste_row = 1
        self.Fertigkeitsliste_rowhilfe=[]
        self.liste_AuswahlFertigkeiten=[]
        self.liste_Checkboxen = []
        self.fertigkeiten = self.auslesen_Fertigkeiten()

        # Die Charaktereigenschaften aufspalten in allgemein, attribut und fertigkeiten
        allgemeine_Daten, attribut_Daten, fertigkeiten_Daten = self.Daten_laden(CharakterGesamt)

        # aktuelle Klassenberechnung herausfinden
        self.berechnung_Leben, self.berechnung_Mana, self.kosten_Fertigkeiten = self.klassenBerechnung_filter(str(CharakterGesamt[3])[2:-2])

        # Canvas hinzufügen ins Frame
        self.canvas = tk.Canvas(master)
        self.canvas.grid(row=0, column=0)

        # Vertikale Scroll-Leiste aufs Canvas bezogen
        vsbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        vsbar.grid(row=0, column=2, sticky=tk.NS)

        # Frame auf Canvas erschaffen für die Oberfläche
        self.c_master = tk.Frame(self.canvas)

        # Objekte hinzufügen
        #Allgemeine Übersicht erstellen
        self.erstellen_Allgemein(self.c_master, allgemeine_Daten, fertigkeiten_Daten)
        #ATT Übersicht erstellen
        self.erstellen_Attribut(self.c_master,attribut_Daten)
        # Fertigkeitsübersicht erstellen
        self.erstellen_Fertigkeiten(self.c_master, fertigkeiten_Daten)
        # Speicher Button
        self.Button_speichern = tk.Button(self.c_master, text='Speichern', command=self.speichern, font=14, width=20)
        self.Button_speichern.grid(row=2, column=0)
        # Schließen
        self.Button_schließen = tk.Button(self.c_master, text='Schließen', command=master.destroy, font=14, width=20)
        self.Button_schließen.grid(row=2, column=1)

        # Fenster erschaffen, der alle Objekte hält
        self.canvas.create_window((0, 0), window=self.c_master, anchor=tk.NW)

        # keine Ahnung was hier passiert
        self.c_master.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        self.canvas.configure(scrollregion=bbox, width=800, height=600)

    def Daten_laden(self,CharakterGesamt):
        allgemeine_Daten=CharakterGesamt[:8]
        attribut_Daten =CharakterGesamt[8:13]
        fertigkeiten_Daten = []
        fertigkeiten_Daten[:2] = CharakterGesamt[4:6]
        fertigkeiten_Daten[2:] = CharakterGesamt[13:]
        return allgemeine_Daten, attribut_Daten, fertigkeiten_Daten

    def auslesen_Fertigkeiten(self):
        f = open('fertigkeiten.txt','r')
        inhalt=f.readlines()
        f.close()
        i=0
        for zeile in inhalt:
            zeile = zeile.strip('\n')
            inhalt[i]=zeile
            i+=1
        return inhalt

    def klassenBerechnung_filter(self, klasse):
        klassen = open('klassen.txt', 'r')
        inhalt = klassen.readlines()
        klassen.close()
        i = 0
        for zeile in inhalt:
            zeile = zeile.strip('\n')
            zeile = zeile.split(' ')
            if klasse == zeile[0]:
                berechnung_Leben = zeile[1]
                berechnung_Mana = zeile[2]
                kosten_fertigkeiten = zeile[3:]
                return berechnung_Leben, berechnung_Mana, kosten_fertigkeiten
            i += 1

    def erstellen_Allgemein(self, master, Daten, fertigkeiten_Daten):
        self.APuebrig = str(Daten[5])[5:-2]
        self.APuebrig = int(self.APuebrig)

        self.LabelFrame_AllgemeinEingabe = tk.LabelFrame(master, text='Attribute', width=500, bd=5, relief='ridge' )
        self.LabelFrame_AllgemeinEingabe.grid(row=0, column=0, sticky='W')

        self.Label_spNameL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Spieler: ', font=20)
        self.Label_spName = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[0])[15:-2], font=20)
        self.Label_chNameL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Charakter: ', font=20)
        self.Label_chName = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[1])[17:-2], font=20)
        self.Label_volkL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Volk: ', font=20)
        self.Label_volk = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[2])[2:-2], font=20)
        self.Label_klasseL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Klasse: ', font=20)
        self.Label_klasse = tk.Label(self.LabelFrame_AllgemeinEingabe, text=Daten[3], font=20)
        self.Label_stufeL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Stufe: ', font=20)
        self.Label_stufe = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[4])[8:-2], font=20)
        self.Label_lebenL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Leben: ', font=20)
        self.Label_leben = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[6])[9:-2], font=20)
        self.Label_manaL = tk.Label(self.LabelFrame_AllgemeinEingabe, text='Mana: ', font=20)
        self.Label_mana = tk.Label(self.LabelFrame_AllgemeinEingabe, text=str(Daten[7])[8:-2], font=20)
        self.Button_aufleveln = tk.Button(self.LabelFrame_AllgemeinEingabe, text='Level UP', command=self.aufleveln_Charakter)
        self.Button_Resett_Stufe = tk.Button(self.LabelFrame_AllgemeinEingabe, text='Resett', command=lambda: self.allgemeineEingabe_RESETT(master, Daten, fertigkeiten_Daten))

        self.Label_spNameL.grid(row= 0, column=0, sticky='W')
        self.Label_spName.grid(row= 0, column=1, sticky='W')
        self.Label_chNameL.grid(row=1, column=0, sticky='W')
        self.Label_chName.grid(row=1, column=1, sticky='W')
        self.Label_volkL.grid(row=2, column=0, sticky='W')
        self.Label_volk.grid(row=2, column=1, sticky='W')
        self.Label_klasseL.grid(row=3, column=0, sticky='W')
        self.Label_klasse.grid(row=3, column=1, sticky='W')
        self.Label_stufeL.grid(row=4, column=0, sticky='W')
        self.Label_stufe.grid(row=4, column=1, sticky='W')
        self.Label_lebenL.grid(row=5, column=0, sticky='W')
        self.Label_leben.grid(row=5, column=1, sticky='W')
        self.Label_manaL.grid(row=6, column=0, sticky='W')
        self.Label_mana.grid(row=6, column=1, sticky='W')
        self.Button_aufleveln.grid(row=7,column=0, sticky='W')
        self.Button_Resett_Stufe.grid(row=7, column=1, sticky='E')

    def aufleveln_Charakter(self):
        # aufleveln
        level = int(self.Label_stufe.cget('text'))
        level+=1
        self.Label_stufe.config(text=level)
        # AP steigern
        self.APuebrig+=8
        # Leben steigern
        leben = int(self.Label_leben.cget('text'))
        steigerung = int(self.berechnung_Leben[:-1])
        leben=leben + (steigerung + int(self.Label_Boni_ko.cget('text')))
        # Ausgabe
        self.Label_leben.config(text=leben)
        self.Label_Apuebrig.config(text='AP: ' + str(self.APuebrig))
        for checkbox in self.liste_Checkboxen:
            checkbox = 0
        for fertigkeit in self.Fertigkeitsliste_Objekte:
            fertigkeit[5].deselect()
            fertigkeit[4].config(state='active')

    def allgemeineEingabe_RESETT(self, master, Daten, fertigkeiten_Daten):
        self.LabelFrame_AllgemeinEingabe.destroy()
        self.LabelFrame_FertigkeitEingabe.destroy()
        self.erstellen_Allgemein(master, Daten, fertigkeiten_Daten)

        self.erstellen_Fertigkeiten(master, fertigkeiten_Daten)

    def erstellen_Attribut(self, master, Daten):
        self.LabelFrame_AttEingabe = tk.LabelFrame(master, text='Allgemeine Daten', width=500, bd=5, relief='ridge')
        self.LabelFrame_AttEingabe.grid(row=0, column=1, sticky='W')

        self.Label_ueber_ATTR = tk.Label(self.LabelFrame_AttEingabe, text='Attribut   ', font=18)
        self.Label_ueber_wert = tk.Label(self.LabelFrame_AttEingabe, text=' Gesamtwert   ', font=18)
        self.Label_ueber_BONI = tk.Label(self.LabelFrame_AttEingabe, text=' Att-Bonus   ', font=18)

        self.Label_ueber_ATTR.grid(row=0,column=0,sticky='W', pady=5)
        self.Label_ueber_wert.grid(row=0,column=1,sticky='W', pady=5)
        self.Label_ueber_BONI.grid(row=0,column=3,sticky='W', pady=5)

        self.Label_staerke = tk.Label(self.LabelFrame_AttEingabe, text='ST:', font=18)
        self.Label_geschick = tk.Label(self.LabelFrame_AttEingabe, text='GE:', font=18)
        self.Label_konsti = tk.Label(self.LabelFrame_AttEingabe, text='KO:', font=18)
        self.Label_intelli = tk.Label(self.LabelFrame_AttEingabe, text='IN:', font=18)
        self.Label_chari = tk.Label(self.LabelFrame_AttEingabe, text='CH:', font=18)
        self.Button_resett_ATT = tk.Button(self.LabelFrame_AttEingabe, text='Resett', command=lambda :self.ATT_RESETT(master, Daten))

        self.Label_staerke.grid(row=1,column=0)
        self.Label_geschick.grid(row=2,column=0)
        self.Label_konsti.grid(row=3,column=0)
        self.Label_intelli.grid(row=4,column=0)
        self.Label_chari.grid(row=5,column=0)
        self.Button_resett_ATT.grid(row=7,column=3,sticky='E')

        self.Label_Wert_st = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[0][0]), font=18)
        self.Label_Wert_ge = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[1][0]), font=18)
        self.Label_Wert_ko = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[2][0]), font=18)
        self.Label_Wert_in = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[3][0]), font=18)
        self.Label_Wert_ch = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[4][0]), font=18)

        self.Label_Wert_st.grid(row=1,column=1)
        self.Label_Wert_ge.grid(row=2, column=1)
        self.Label_Wert_ko.grid(row=3, column=1)
        self.Label_Wert_in.grid(row=4, column=1)
        self.Label_Wert_ch.grid(row=5, column=1)

        self.Label_Boni_st = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[0][1]), font=18)
        self.Label_Boni_ge = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[1][1]), font=18)
        self.Label_Boni_ko = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[2][1]), font=18)
        self.Label_Boni_in = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[3][1]), font=18)
        self.Label_Boni_ch = tk.Label(self.LabelFrame_AttEingabe, text=int(Daten[4][1]), font=18)

        self.Label_Boni_st.grid(row=1,column=3)
        self.Label_Boni_ge.grid(row=2,column=3)
        self.Label_Boni_ko.grid(row=3,column=3)
        self.Label_Boni_in.grid(row=4,column=3)
        self.Label_Boni_ch.grid(row=5,column=3)

        # Buttons dehalb hierhingeschoben, da die Label_Boni vor den Buttons generiert werden müssen, wegen der Commandanweisung
        self.Button_aufleveln_st = tk.Button(self.LabelFrame_AttEingabe, text='Aufleveln', command=lambda: self.auflevlen_Attribut(self.Label_Wert_st, self.Label_Boni_st, self.Button_aufleveln_st))
        self.Button_aufleveln_ge = tk.Button(self.LabelFrame_AttEingabe, text='Aufleveln', command=lambda: self.auflevlen_Attribut(self.Label_Wert_ge, self.Label_Boni_ge, self.Button_aufleveln_ge))
        self.Button_aufleveln_ko = tk.Button(self.LabelFrame_AttEingabe, text='Aufleveln', command=lambda: self.auflevlen_Attribut(self.Label_Wert_ko, self.Label_Boni_ko, self.Button_aufleveln_ko))
        self.Button_aufleveln_in = tk.Button(self.LabelFrame_AttEingabe, text='Aufleveln', command=lambda: self.auflevlen_Attribut(self.Label_Wert_in, self.Label_Boni_in, self.Button_aufleveln_in))
        self.Button_aufleveln_ch = tk.Button(self.LabelFrame_AttEingabe, text='Aufleveln', command=lambda: self.auflevlen_Attribut(self.Label_Wert_ch, self.Label_Boni_ch, self.Button_aufleveln_ch))

        self.Button_aufleveln_st.grid(row=1,column=2,sticky='W')
        self.Button_aufleveln_ge.grid(row=2,column=2,sticky='W')
        self.Button_aufleveln_ko.grid(row=3,column=2,sticky='W')
        self.Button_aufleveln_in.grid(row=4,column=2,sticky='W')
        self.Button_aufleveln_ch.grid(row=5,column=2,sticky='W')

    def auflevlen_Attribut(self, Label_Att_Wert, Label_Att_Boni, Button):
        # Hilfslisten um den aktuellen Bonus zu bestimmen
        Array_Werte =   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        Array_Boni  =   [-3, -2, -2, -1, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8]
        # Attributswert bestimmen, um 1 steigern
        Wert = int(Label_Att_Wert.cget('text'))
        Wert += 1
        # Attributswert=20, maximale Größe erreicht
        if Wert==20:
            Button['state']='disabled'
        # Attributsbonus bestimmen
        index= Array_Werte.index(Wert)
        Boni = Array_Boni[index]
        # Attributswert und -bonus zurückgeben
        Label_Att_Boni.config(text=Boni)
        Label_Att_Wert.config(text=Wert)

    def ATT_RESETT(self, master, Daten):
        self.LabelFrame_AttEingabe.destroy()
        self.erstellen_Attribut(master, Daten)

    def erstellen_Fertigkeiten(self,master,Daten):
        self.LabelFrame_FertigkeitEingabe = tk.LabelFrame(master, text='Fertigkeiten', width=600, bd=5, relief='ridge')
        self.LabelFrame_FertigkeitEingabe.grid(row=1, column=0, columnspan=2, sticky='W')
        # Initialisieren der benötigten Variablen
        self.Fertigkeitsliste_Objekte=[]
        self.liste_AuswahlFertigkeiten=[]
        self.liste_Checkboxen=[]
        self.Fertigkeitsliste_row=1
        self.Fertigkeitsliste_rowhilfe=[]

        self.Label_Apuebrig=tk.Label(self.LabelFrame_FertigkeitEingabe, text=str(Daten[1])[2:-2])
        self.Button_hibzufuegenFertigkeit = tk.Button(self.LabelFrame_FertigkeitEingabe, text='Fertigkeit hinzufügen', command=lambda: self.hinzufuegen_Fertigkeit(self.LabelFrame_FertigkeitEingabe))

        self.Label_Apuebrig.grid(row=0, column=0, sticky='E')
        self.Button_hibzufuegenFertigkeit.grid(row=0, column=1)
        self.laden_Fertigkeiten(self.LabelFrame_FertigkeitEingabe,Daten)


    def laden_Fertigkeiten(self, master, Daten):
        # nur die Fertigkeiten laden
        fertigkeiten = Daten[2:]
        # aktuelle Objektzeile finden
        zeile = self.Fertigkeitsliste_row
        # für jede Fertigkeit die geladen wird, eine Objektzeile erstellen
        for fertigkeit in fertigkeiten:
            index=self.fertigkeiten.index(fertigkeit[0])
            self.liste_AuswahlFertigkeiten.append(tk.StringVar(master,self.fertigkeiten[index]))
            self.liste_Checkboxen.append(tk.IntVar(master, value=0))
            # Objekte erstellen
            self.OptionMenu_Fertigkeit = tk.OptionMenu(master, self.liste_AuswahlFertigkeiten[zeile-1], *self.fertigkeiten, command=self.aktualisieren_Fertigkeit)
            self.Entry_Notiz = tk.Entry(master, text=fertigkeit[1], state='disabled')
            self.Label_Stufe = tk.Label(master, text=fertigkeit[2])
            self.Label_Kosten = tk.Label(master, text=fertigkeit[3])
            self.Button_lvlUP_Fertigkeit = tk.Button(master,text='Aufleveln', command=lambda z=zeile: self.aufleveln_Fertigkeit(z))
            self.Checkbox_Fertigkeit_lvlt = tk.Checkbutton(master, text='Einmal gelevelt?', var=self.liste_Checkboxen[zeile-1], state='disabled')
            self.Button_Fertigkeit_loeschen = tk.Button(master, text='Fertigkeit löschen', state='disabled', command=lambda z=zeile: self.loeschen_Fertigkeit(z))
            # Objekte platzieren
            self.OptionMenu_Fertigkeit.grid(row=zeile,column=0, sticky='E')
            self.Entry_Notiz.grid(row=zeile,column=1)
            self.Label_Stufe.grid(row=zeile,column=2)
            self.Label_Kosten.grid(row=zeile,column=3)
            self.Button_lvlUP_Fertigkeit.grid(row=zeile,column=4)
            self.Checkbox_Fertigkeit_lvlt.grid(row=zeile,column=5)
            self.Button_Fertigkeit_loeschen.grid(row=zeile,column=6)

            # die geladenen Fertigkeiten checken, wie oft gelevelt
            if fertigkeit[4]=='2':
                self.Button_lvlUP_Fertigkeit['state']='disabled'
                self.liste_Checkboxen[zeile-1].set(1)
            elif fertigkeit[4]=='1'and len(fertigkeit[3])>2:
                self.Button_lvlUP_Fertigkeit['state']='active'
                self.liste_Checkboxen[zeile-1].set(1)
            elif fertigkeit[4]=='1'and len(fertigkeit[3])<2:
                self.Button_lvlUP_Fertigkeit['state']='disabled'
                self.liste_Checkboxen[zeile-1].set(1)
            elif fertigkeit[4] == '0':
                self.Button_lvlUP_Fertigkeit['state']='active'
                self.liste_Checkboxen[zeile-1].set(0)
            self.OptionMenu_Fertigkeit.config(state='disabled')

            # Objekte einer Liste hinzufügen
            hilfliste = [
                self.OptionMenu_Fertigkeit,
                self.Entry_Notiz,
                self.Label_Stufe,
                self.Label_Kosten,
                self.Button_lvlUP_Fertigkeit,
                self.Checkbox_Fertigkeit_lvlt,
                self.Button_Fertigkeit_loeschen
            ]
            self.Fertigkeitsliste_Objekte.append(hilfliste)
            self.Fertigkeitsliste_rowhilfe.append(zeile)
            zeile+=1

        self.Fertigkeitsliste_row = zeile

    def hinzufuegen_Fertigkeit(self, master):
        zeile = self.Fertigkeitsliste_row
        self.liste_AuswahlFertigkeiten.append(tk.StringVar(master, self.fertigkeiten[0]))
        self.liste_Checkboxen.append(tk.IntVar(master, value=0))
        hilfsvariable=len(self.liste_Checkboxen)
        # Objekte erstellen
        self.OptionMenu_Fertigkeit = tk.OptionMenu(master, self.liste_AuswahlFertigkeiten[hilfsvariable - 1], *self.fertigkeiten,  command=self.aktualisieren_Fertigkeit)
        self.Entry_Notiz = tk.Entry(master, text='')
        self.Label_Stufe = tk.Label(master, text='0')
        self.Label_Kosten = tk.Label(master, text='-')
        self.Button_lvlUP_Fertigkeit = tk.Button(master, text='Aufleveln', command=lambda z=zeile: self.aufleveln_Fertigkeit(z), state='disabled')
        self.Checkbox_Fertigkeit_lvlt = tk.Checkbutton(master, text='Einmal gelevelt?', var=self.liste_Checkboxen[hilfsvariable - 1], state='disabled')
        self.Button_Fertigkeit_loeschen = tk.Button(master, text='Fertigkeit löschen', command=lambda z=zeile: self.loeschen_Fertigkeit(z))
        # Objekte platzieren
        self.OptionMenu_Fertigkeit.grid(row=zeile, column=0, sticky='E')
        self.Entry_Notiz.grid(row=zeile, column=1)
        self.Label_Stufe.grid(row=zeile, column=2)
        self.Label_Kosten.grid(row=zeile, column=3)
        self.Button_lvlUP_Fertigkeit.grid(row=zeile, column=4)
        self.Checkbox_Fertigkeit_lvlt.grid(row=zeile, column=5)
        self.Button_Fertigkeit_loeschen.grid(row=zeile, column=6)

        # Objekte einer Liste hinzufügen
        hilfliste = [
                self.OptionMenu_Fertigkeit,
                self.Entry_Notiz,
                self.Label_Stufe,
                self.Label_Kosten,
                self.Button_lvlUP_Fertigkeit,
                self.Checkbox_Fertigkeit_lvlt,
                self.Button_Fertigkeit_loeschen
            ]
        self.Fertigkeitsliste_Objekte.append(hilfliste)
        self.Fertigkeitsliste_rowhilfe.append(zeile)
        zeile+=1
        self.Fertigkeitsliste_row = zeile

        # Canvas aktualisieren, Magie
        # Fenster erschaffen, der alle Objekte hält
        self.canvas.create_window((0, 0), window=self.c_master, anchor=tk.NW)

        # keine Ahnung was hier passiert
        self.c_master.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        self.canvas.configure(scrollregion=bbox, width=800, height=600)

    def aktualisieren_Fertigkeit(self, auswahl):
        fertigkeit = auswahl
        # kosten der Fertigkeit bestimmen
        index = self.fertigkeiten.index(fertigkeit)
        kosten = self.kosten_Fertigkeiten[index]

        if fertigkeit in ['Waffen', 'Wissen', 'Spruchliste', 'Kunst']:
            zulaessig = True
        else:
            zulaessig =False
        # Optionmenu auswahl sperren und freigeben fürs leveln
        i = 0
        for Values in self.liste_AuswahlFertigkeiten:
            if fertigkeit == Values.get():
                if self.Fertigkeitsliste_Objekte[i][0]['state'] == 'disabled' and zulaessig==False:
                    tk.messagebox.showerror('Fertgikeit-Fehler', 'Fertgikeit wurde bereits ausgewählt. Andernfalls wenden Sie sich an den Programmierer.')
                    break
                if self.Fertigkeitsliste_Objekte[i][0]['state'] == 'active' or self.Fertigkeitsliste_Objekte[i][0]['state'] == 'normal':
                    self.Fertigkeitsliste_Objekte[i][3].config(text=kosten)
                    self.Fertigkeitsliste_Objekte[i][0].config(state='disabled')
                    self.Fertigkeitsliste_Objekte[i][4].config(state='active')
                    break
            i += 1

    def loeschen_Fertigkeit(self, zeile):
        # leiste = Index, um 2 kleiner da Array bei 0 startet
        index = self.Fertigkeitsliste_rowhilfe.index(zeile)
        for Objekt in self.Fertigkeitsliste_Objekte[index]:
            Objekt.destroy()
        del self.Fertigkeitsliste_Objekte[index]
        del self.Fertigkeitsliste_rowhilfe[index]
        del self.liste_Checkboxen[index]
        del self.liste_AuswahlFertigkeiten[index]

    def aufleveln_Fertigkeit(self, zeile):
        # aktuelle Fertigkeit/Index herrausfinden
        index = self.Fertigkeitsliste_rowhilfe.index(zeile)
        # aktuelles Level, -kosten herausfinden
        level = float(self.Fertigkeitsliste_Objekte[index][2].cget('text'))
        levelkosten = self.Fertigkeitsliste_Objekte[index][3].cget('text')
        levelkosten1 = int(levelkosten[0])
        levelkosten2 = int(levelkosten[-1])
        # Fertgikeit schon einmal gelevelt diese Stufe?
        checkbutton = self.liste_Checkboxen[index].get()
        # Fertigkeit nicht mehr löschbar, zur Vermeidung von Fehlern/löschen von bereits ausgegebenen AP
        self.Fertigkeitsliste_Objekte[index][6].config(state='disabled')

        Apuebrig = self.APuebrig
        # Checken der Bedingungen
        # Fertigkeit 2 mal levelbar
        if (checkbutton < 1 and levelkosten1 <= Apuebrig and len(levelkosten) > 2):
            # überprüfen des aktuellen Levels
            if level < 6:
                aufleveln = 1
            elif level >= 6 and level < 11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten1
            # Ausgabe AP und Level
            self.Label_Apuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste_Objekte[index][2].config(text=str(level))
            # Fertigkeit einmal gelevelt
            self.Fertigkeitsliste_Objekte[index][5].select()

        elif checkbutton > 0 and levelkosten2 <=Apuebrig and len(levelkosten) > 2:
            # überprüfen des aktuellen Levels
            if level < 6:
                aufleveln = 1
            elif level >= 6 and level < 11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten2
            # Ausgabe AP und Level
            self.Label_Apuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste_Objekte[index][2].config(text=str(level))
            # Fertigkeit maximal gelevelt
            self.Fertigkeitsliste_Objekte[index][4].config(state='disabled')
        # abfangen Fehler zur 'überlevelung'
        elif checkbutton < 1 and levelkosten1 > Apuebrig and len(levelkosten) > 2:
            self.Fertigkeitsliste_Objekte[index][4].config(state='disabled')
        elif checkbutton > 0 and levelkosten2 > Apuebrig and len(levelkosten) > 2:
            self.Fertigkeitsliste_Objekte[index][4].config(state='disabled')
        # Fertigkeit 1 mal levelbar
        elif levelkosten1 == levelkosten2 and levelkosten1 <= Apuebrig:
            # überprüfen des aktuellen Levels
            if level < 6:
                aufleveln = 1
            elif level >= 6 and level < 11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten1
            # Ausgabe AP und Level
            self.Label_Apuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste_Objekte[index][2].config(text=str(level))
            # Fertigkeit maximal gelevelt
            self.Fertigkeitsliste_Objekte[index][5].select()
            self.Fertigkeitsliste_Objekte[index][4].config(state='disabled')
        # Abfangen von überlevelung
        elif levelkosten1 == levelkosten2 and levelkosten1 > Apuebrig:
            self.Fertigkeitsliste_Objekte[index][4].config(state='disabled')

        #Mana Berechnung
        if self.liste_AuswahlFertigkeiten[index].get()=='Magie entwickeln':
            stufe = float(self.Fertigkeitsliste_Objekte[index][2].cget('text'))
            stufe=int(stufe)
            if self.berechnung_Mana[-1]=='i':
                bonus=int(self.Label_Boni_in.cget('text'))
            elif self.berechnung_Mana[-1]=='c':
                bonus = int(self.Label_Boni_ch.cget('text'))
            wert = int(self.berechnung_Mana[:-1])
            Mana = stufe*(wert+bonus)
            self.Label_mana.config(text=str(Mana))

    def speichern(self):
        Charakter_Matrix = []
        # !Charakter allgemeine Daten abspeicher
        Charakter_Matrix.append('Spielername: '+ self.Label_spName.cget('text'))
        Charakter_Matrix.append('Charaktername: '+ self.Label_chName.cget('text'))
        Charakter_Matrix.append(self.Label_volk.cget('text'))
        Charakter_Matrix.append(self.Label_klasse.cget('text'))
        Charakter_Matrix.append('Stufe: '+ str(self.Label_stufe.cget('text')))
        Charakter_Matrix.append(self.Label_Apuebrig.cget('text'))
        Charakter_Matrix.append('Leben: '+ str(self.Label_leben.cget('text')))
        Charakter_Matrix.append('Mana: '+ str(self.Label_mana.cget('text')))
        # Charakter Attributsdaten abspeichern
        Charakter_Matrix.append(str(self.Label_Wert_st.cget('text')) + ', ' + str(self.Label_Boni_st.cget('text')))
        Charakter_Matrix.append(str(self.Label_Wert_ge.cget('text')) + ', ' + str(self.Label_Boni_ge.cget('text')))
        Charakter_Matrix.append(str(self.Label_Wert_ko.cget('text')) + ', ' + str(self.Label_Boni_ko.cget('text')))
        Charakter_Matrix.append(str(self.Label_Wert_in.cget('text')) + ', ' + str(self.Label_Boni_in.cget('text')))
        Charakter_Matrix.append(str(self.Label_Wert_ch.cget('text')) + ', ' + str(self.Label_Boni_ch.cget('text')))
        # leere Fertigkeiten löschen
        # Charakter Fertigkeiten abspeichern
        zaehler = 0
        for Fertgikeit in self.Fertigkeitsliste_Objekte:
            name_fertigkeit = self.liste_AuswahlFertigkeiten[zaehler].get()
            notiz_fertigkeit = Fertgikeit[1].cget('text')
            stufe_fertigkeit = str(Fertgikeit[2].cget('text'))
            # wenn Fertigkeitsstufe = 0, dann überspringe
            if float(stufe_fertigkeit) == 0:
                continue
            kosten_fertigkeit = str(Fertgikeit[3].cget('text'))

            if self.liste_Checkboxen[zaehler].get() == 1:
                gelevelt = '1'
                if Fertgikeit[4]['state'] == 'disabled':
                    gelevelt = '2'
            else:
                gelevelt = '0'

            fertigkeit_liste = name_fertigkeit + ', ' + notiz_fertigkeit + ', ' + stufe_fertigkeit + ', ' + kosten_fertigkeit + ', ' + gelevelt
            Charakter_Matrix.append(fertigkeit_liste)
            zaehler +=1

        # Charakter abspeichern/txt überschreiben
        pfad = os.getcwd()
        txt = open((pfad + '\\charaktere\\' + self.Label_chName.cget('text'))+'.txt', 'w')
        for zeile in Charakter_Matrix:
            txt.write(str(zeile)+'\n')
        txt.close()

class Charaktererstellung:
    def __init__(self, master):
        # Auslesen datein
        self.fertigkeiten = self.auslesen('fertigkeiten.txt')
        self.voelkerGesamt = self.auslesen('voelker.txt')
        self.voelkerGesamt = self.listStringToArray(self.voelkerGesamt)
        self.klassenGesamt = self.auslesen('klassen.txt')

        # Erstllen der Variablen mit 1. nur Voekler, 2. nur Attributen der Völker
        self.voelker, self.vLeben, self.vAtt = self.voelkerULebenUAttAuslesen(self.voelkerGesamt)
        # Erstellen der Variablen mit 1. nur Klassen, 2. fertigkeitsKosten der Klassen
        self.klassen,self.kLebenuMana, self.fKosten = self.klassenUfKostenAuslasen(self.klassenGesamt)

        # Erstellen von Hilfsvariabeln um die Kosten der Attribute zu zählen
        self.kaufAtt = [0, 0, 0, 0, 0]

        # Hauptfenster erstellen
        self.master = master
        self.master.config()
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # UnterFenster erstellen
        self.allgemeineEingabe(self.frame)
        self.attributEingabe(self.frame)
        self.attBonusBestimmen()
        self.klassenUndLevelEingabe(self.frame)


        # Menü-Hauptfenster erstellen
        self.quitButton = tk.Button(self.frame, text='Schließen', width=25, command=self.master.destroy)
        self.Button_Bestaetigung = tk.Button(self.frame, text='Bestätigung', width=25, command=self.Bestaetigen)
        self.ScrollBar = tk.Scrollbar(self.frame, orient='vertical')

        self.quitButton.grid(row=4, column=0)
        self.Button_Bestaetigung.grid(row=3, column=0)
        self.ScrollBar.grid(row=0, rowspan=5,column=2, sticky='ns')
        self.ScrollBar.set(0,1000000)

    def allgemeineEingabe(self, mainFrame):
        self.aEingabe = tk.LabelFrame(mainFrame, text='Allgemeine Eingabe', bd=5, relief='ridge')
        self.aEingabe.grid(row=0, column=0, padx=20, pady=20)

        self.volk = tk.StringVar(self.aEingabe, self.voelker[0])
        self.klasse = tk.StringVar(self.aEingabe, self.klassen[0])

        self.Label_spName = tk.Label(self.aEingabe, text='Spielername:')
        self.Label_chName = tk.Label(self.aEingabe, text='Charakternamen:')
        self.Label_volk = tk.Label(self.aEingabe, text='Volk:')
        self.Label_klasse = tk.Label(self.aEingabe, text='Klasse:')
        self.Entry_spName = tk.Entry(self.aEingabe)
        self.Entry_chName = tk.Entry(self.aEingabe)
        self.OptionMenu_volk = tk.OptionMenu(self.aEingabe, self.volk, *self.voelker, command=self.aktualisierenVolkattB)
        self.OptionMenu_klasse = tk.OptionMenu(self.aEingabe, self.klasse, *self.klassen, command=self.aktualisierenKlasse)

        self.Label_spName.grid(row=0, column=0, sticky='w')
        self.Label_chName.grid(row=1, column=0, sticky='w')
        self.Label_volk.grid(row=2, column=0, sticky='w')
        self.Label_klasse.grid(row=3, column=0, sticky='w')
        self.Entry_spName.grid(row=0, column=1, sticky='w')
        self.Entry_chName.grid(row=1, column=1, sticky='w')
        self.OptionMenu_volk.grid(row=2, column=1, sticky='e')
        self.OptionMenu_klasse.grid(row=3, column=1, sticky='e')

    def attributEingabe(self, mainFrame):
        self.atEingabe = tk.LabelFrame(mainFrame, text='Eingabe der Attribute', bd=5, relief='ridge')
        self.atEingabe.grid(row=1, column=0, padx=20, pady=20)

        # Erstellen der einzelnen Blöcke
        # Bezeichnungsblock
        self.Label_Att = tk.Label(self.atEingabe, text='Attribut')
        self.Label_st = tk.Label(self.atEingabe, text='Stärke:')
        self.Label_ge = tk.Label(self.atEingabe, text='Geschicklichkeit:')
        self.Label_ko = tk.Label(self.atEingabe, text='Konstitution:')
        self.Label_in = tk.Label(self.atEingabe, text='Intelligenz:')
        self.Label_ch = tk.Label(self.atEingabe, text='Charisma:')

        self.Label_Att.grid(row=0, column=0, sticky='w')
        self.Label_st.grid(row=1, column=0, sticky='w')
        self.Label_ge.grid(row=2, column=0, sticky='w')
        self.Label_ko.grid(row=3, column=0, sticky='w')
        self.Label_in.grid(row=4, column=0, sticky='w')
        self.Label_ch.grid(row=5, column=0, sticky='w')

        # Block für die Boni der Völker
        self.Label_AttB = tk.Label(self.atEingabe, text='Bonus')
        self.Label_stB = tk.Label(self.atEingabe, text='0')
        self.Label_geB = tk.Label(self.atEingabe, text='0')
        self.Label_koB = tk.Label(self.atEingabe, text='0')
        self.Label_inB = tk.Label(self.atEingabe, text='0')
        self.Label_chB = tk.Label(self.atEingabe, text='0')

        self.Label_AttB.grid(row=0, column=1)
        self.Label_stB.grid(row=1, column=1)
        self.Label_geB.grid(row=2, column=1)
        self.Label_koB.grid(row=3, column=1)
        self.Label_inB.grid(row=4, column=1)
        self.Label_chB.grid(row=5, column=1)

        # Block für die Kaufauswahl
        self.listeP = [0, 1 , 2, 3, 4, 5, 6, 7, 8, 9 , 10]
        self.eSt = tk.StringVar(self.atEingabe, self.listeP[0])
        self.eGe = tk.StringVar(self.atEingabe, self.listeP[0])
        self.eKo = tk.StringVar(self.atEingabe, self.listeP[0])
        self.eIn = tk.StringVar(self.atEingabe, self.listeP[0])
        self.eCh = tk.StringVar(self.atEingabe, self.listeP[0])

        self.Label_kaufAtt = tk.Label(self.atEingabe, text='Kauf')
        self.OptionMenu_st = tk.OptionMenu(self.atEingabe, self.eSt, *self.listeP, command=self.aktualisierenATTkauf_st)
        self.OptionMenu_ge = tk.OptionMenu(self.atEingabe, self.eGe, *self.listeP, command=self.aktualisierenATTkauf_ge)
        self.OptionMenu_ko = tk.OptionMenu(self.atEingabe, self.eKo, *self.listeP, command=self.aktualisierenATTkauf_ko)
        self.OptionMenu_in = tk.OptionMenu(self.atEingabe, self.eIn, *self.listeP, command=self.aktualisierenATTkauf_in)
        self.OptionMenu_ch = tk.OptionMenu(self.atEingabe, self.eCh, *self.listeP, command=self.aktualisierenATTkauf_ch)

        self.Label_kaufAtt.grid(row=0, column=2)
        self.OptionMenu_st.grid(row=1, column=2)
        self.OptionMenu_ge.grid(row=2, column=2)
        self.OptionMenu_ko.grid(row=3, column=2)
        self.OptionMenu_in.grid(row=4, column=2)
        self.OptionMenu_ch.grid(row=5, column=2)

        # Block Gesamtergebnis Attribute
        self.Label_AttG = tk.Label(self.atEingabe, text='Gesamt')
        self.Label_Gst = tk.Label(self.atEingabe, text='0')
        self.Label_Gge = tk.Label(self.atEingabe, text='0')
        self.Label_Gko = tk.Label(self.atEingabe, text='0')
        self.Label_Gin = tk.Label(self.atEingabe, text='0')
        self.Label_Gch = tk.Label(self.atEingabe, text='0')

        self.Label_AttG.grid(row=0, column=3)
        self.Label_Gst.grid(row=1, column=3)
        self.Label_Gge.grid(row=2, column=3)
        self.Label_Gko.grid(row=3, column=3)
        self.Label_Gin.grid(row=4, column=3)
        self.Label_Gch.grid(row=5, column=3)

        # Block für den resultierenden Bonus
        self.Label_rBoni = tk.Label(self.atEingabe, text='resultierender\nBonus')
        self.Label_Rst = tk.Label(self.atEingabe, text='0')
        self.Label_Rge = tk.Label(self.atEingabe, text='0')
        self.Label_Rko = tk.Label(self.atEingabe, text='0')
        self.Label_Rin = tk.Label(self.atEingabe, text='0')
        self.Label_Rch = tk.Label(self.atEingabe, text='0')

        self.Label_rBoni.grid(row=0, column=4)
        self.Label_Rst.grid(row=1, column=4)
        self.Label_Rge.grid(row=2, column=4)
        self.Label_Rko.grid(row=3, column=4)
        self.Label_Rin.grid(row=4, column=4)
        self.Label_Rch.grid(row=5, column=4)

        # Letzter Block dient zur Überprüfung der ausgegebenen Punkte und ausgabe der verbleibenden
        self.Label_attPunkte = tk.Label(self.atEingabe, text='Kauf->Kosten\n(1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->8, 8->10, 9->112, 10->16)')
        self.Label_attPuebrig = tk.Label(self.atEingabe, text = 'Kaufpunkte übrig\n35')

        self.Label_attPunkte.grid(row=6, column=1, columnspan=3)
        self.Label_attPuebrig.grid(row=6, column=4)

    def klassenUndLevelEingabe(self, mainFrame):
        self.kUlEingabe = tk.LabelFrame(mainFrame, text='Fertigkeitenauswahl, sowie Level', bd=5, relief='ridge')
        self.kUlEingabe.grid(row=2, column=0, padx=20, pady=20)

        self.cb = []
        self.auswahlfertigkeit = []
        self.Fertigkeitsliste = []
        self.Fertigkeitsliste_row_hilfliste = []
        self.Fertigkeitsliste_row = 2
        self.CharStufe = 1
        self.Leben=0

        if self.volk.get() == 'Mensch':
            self.APuebrig = 10
        else:
            self.APuebrig = 8

        # Canvas hinzufügen ins Frame
        self.canvas = tk.Canvas(self.kUlEingabe)
        self.canvas.grid(row=0, column=0)

        # Vertikale Scroll-Leiste aufs Canvas bezogen
        vsbar = tk.Scrollbar(self.kUlEingabe, orient=tk.VERTICAL, command=self.canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)

        # Frame auf Canvas erschaffen für die Oberfläche
        self.c_kUlEingabe = tk.Frame(self.canvas)

        # Objekte hinzufügen
        self.Button_neueFertigkeit = tk.Button(self.c_kUlEingabe, text='Fertigkeit hinzufügen', command=self.Fertigkeit_hinzufuegen)
        self.Button_CharLeveln = tk.Button(self.c_kUlEingabe, text='Charakter leveln', command=self.CharLeveln)
        self.Label_CharStufe = tk.Label(self.c_kUlEingabe, text='Charakterstufe: ' + str(self.CharStufe))
        self.Label_APuebrig = tk.Label(self.c_kUlEingabe, text='AP: ' + str(self.APuebrig))
        self.Button_Resett = tk.Button(self.c_kUlEingabe, text='Zurücksetzen', command=self.resett)
        self.Label_Fertigkeit_Namen = tk.Label(self.c_kUlEingabe, text='Fertigkeit')
        self.Label_Fertigkeit_Notiz = tk.Label(self.c_kUlEingabe, text='Optionale Beschreibung')
        self.Label_Fertigkeit_Levelkosten = tk.Label(self.c_kUlEingabe, text='Kosten')
        self.Label_Fertigkeit_Level = tk.Label(self.c_kUlEingabe, text='Level')
        self.Label_Leben = tk.Label(self.c_kUlEingabe, text='Leben: ' + str(self.Leben))
        self.Label_Mana = tk.Label(self.c_kUlEingabe, text='Mana: 0')

        self.Button_neueFertigkeit.grid(row=0, column=0)
        self.Button_CharLeveln.grid(row=0,column=1)
        self.Label_CharStufe.grid(row=0, column=2)
        self.Label_APuebrig.grid(row=0,column=3)
        self.Label_Leben.grid(row=0, column=4)
        self.Label_Mana.grid(row=0, column=5)
        self.Button_Resett.grid(row=0, column=6)
        self.Label_Fertigkeit_Namen.grid(row=1, column=0)
        self.Label_Fertigkeit_Notiz.grid(row=1, column=1)
        self.Label_Fertigkeit_Levelkosten.grid(row=1, column=2)
        self.Label_Fertigkeit_Level.grid(row=1, column=3)

        # Fenster erschaffen, der alle Objekte hält
        self.canvas.create_window((0,0), window=self.c_kUlEingabe, anchor=tk.NW)

        # keine Ahnung was hier passiert
        self.c_kUlEingabe.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        self.canvas.configure(scrollregion=bbox, width=700, height=200)

        self.aktualisierenLeben()
        self.aktualisierenMana()

    def CharLeveln(self):
        self.CharStufe +=1
        self.Label_CharStufe.config(text='Charakterstufe: ' + str(self.CharStufe))
        self.APuebrig += 8
        self.Label_APuebrig.config(text='AP: ' + str(self.APuebrig))
        for element in self.cb:
            element = 0
        for fertigkeit in self.Fertigkeitsliste:
            fertigkeit[5].deselect()
            fertigkeit[4].config(state='active')
        self.aktualisierenLeben()

    def resett(self):
        self.kUlEingabe.destroy()
        self.klassenUndLevelEingabe(self.frame)

    def Fertigkeit_hinzufuegen(self):
        # Aktuelle Zeilenzahl der "Tabelle" rückverfolgen
        self.Fertigkeitsliste_row_hilfliste.append(self.Fertigkeitsliste_row)

        # Erstellung der Variablen
        self.auswahlfertigkeit.append(tk.StringVar(self.c_kUlEingabe, self.fertigkeiten[0]))
        self.cb.append(tk.IntVar(self.c_kUlEingabe, value=0))
        hilfVariable = len(self.cb)

        # Erstellung der Fertigkeits-Zeile
        self.OptionMenuFertigkeit = tk.OptionMenu(self.c_kUlEingabe, self.auswahlfertigkeit[hilfVariable-1], *self.fertigkeiten, command=self.fertigkeitAktualisieren)
        self.Entry_Fertigkeit_Notiz = tk.Entry(self.c_kUlEingabe)
        self.Label_FertigkeitslevelKosten = tk.Label(self.c_kUlEingabe, text=self.fKosten[0][0])
        self.Label_Fertigkeitslevel = tk.Label(self.c_kUlEingabe, text='0')
        self.Button_FertigkeitLeveln = tk.Button(self.c_kUlEingabe, text='Level up',state='disabled', command=lambda leiste=self.Fertigkeitsliste_row: self.fertigkeitLeveln(leiste))
        self.Checkbox_Maxlvl = tk.Checkbutton(self.c_kUlEingabe, text='1 mal\gelevelt',state='disabled', var=self.cb[hilfVariable-1])
        self.Button_Fertigkeitloeschen = tk.Button(self.c_kUlEingabe, text='Fertigkeit löschen', command=lambda leiste=self.Fertigkeitsliste_row: self.fertigkeitLoeschen(leiste))
        # Platzierung der Fertigkeitszeile
        self.OptionMenuFertigkeit.grid(row=self.Fertigkeitsliste_row, column=0, sticky='e')
        self.Entry_Fertigkeit_Notiz.grid(row=self.Fertigkeitsliste_row, column=1)
        self.Label_FertigkeitslevelKosten.grid(row=self.Fertigkeitsliste_row, column=2)
        self.Label_Fertigkeitslevel.grid(row=self.Fertigkeitsliste_row, column=3)
        self.Button_FertigkeitLeveln.grid(row=self.Fertigkeitsliste_row, column=4)
        self.Checkbox_Maxlvl.grid(row=self.Fertigkeitsliste_row, column=5)
        self.Button_Fertigkeitloeschen.grid(row=self.Fertigkeitsliste_row, column=6)

        # Alle Objekte der Zeile werden in ein Array zusammengefasst
        hilfs_liste = [
            self.OptionMenuFertigkeit,
            self.Entry_Fertigkeit_Notiz,
            self.Label_FertigkeitslevelKosten,
            self.Label_Fertigkeitslevel,
            self.Button_FertigkeitLeveln,
            self.Checkbox_Maxlvl,
            self.Button_Fertigkeitloeschen,
            ]
        # Objektzeile/Fertigkeit-Zeile wird der Fertigkeitsliste angefügt, Zeile +1, für nächste Fertigkeit
        self.Fertigkeitsliste.append(hilfs_liste)
        self.Fertigkeitsliste_row += 1

        # Fenster erschaffen, der alle Objekte hält
        self.canvas.create_window((0,0), window=self.c_kUlEingabe, anchor=tk.NW)

        # keine Ahnung was hier passiert
        self.c_kUlEingabe.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        self.canvas.configure(scrollregion=bbox, width=700, height=200)

    def fertigkeitAktualisieren(self, inhalt):
        index_klasse = self.klassen.index(self.klasse.get())
        # Überprüfung der Mehrauswählbarkeit
        if inhalt in ['Wissen', 'Spruchliste', 'Waffen', 'Kunst']:
            zulaessig=True
        else:
            zulaessig=False

        i=0
        for Values in self.auswahlfertigkeit:
            if inhalt==Values.get():
                if self.Fertigkeitsliste[i][0]['state'] == 'disabled' and zulaessig==False:
                    tk.messagebox.showerror('Fertgikeit-Fehler', 'Fertgikeit wurde bereits ausgewählt. Andernfalls wenden Sie sich an den Programmierer.')
                    break
                if self.Fertigkeitsliste[i][0]['state'] == 'active' or self.Fertigkeitsliste[i][0]['state']=='normal':
                    self.Fertigkeitsliste[i][2].config(text=self.fKosten[index_klasse][self.fertigkeiten.index(Values.get())])
                    self.Fertigkeitsliste[i][0].config(state='disabled')
                    self.Fertigkeitsliste[i][4].config(state='active')
                    break
            i +=1

    def fertigkeitLeveln(self, leiste):
        # aktuelle Fertigkeit/Index herrausfinden
        index = self.Fertigkeitsliste_row_hilfliste.index(leiste)
        # aktuelles Level, -kosten herausfinden
        level = float(self.Fertigkeitsliste[index][3].cget('text'))
        levelkosten = self.Fertigkeitsliste[index][2].cget('text')
        levelkosten1 = int(levelkosten[0])
        levelkosten2 = int(levelkosten[-1])
        # Fertgikeit schon einmal gelevelt diese Stufe?
        checkbutton = self.cb[index].get()
        # Fertigkeit nicht mehr löschbar, zur Vermeidung von Fehlern/löschen von bereits ausgegebenen AP
        self.Fertigkeitsliste[index][6].config(state='disabled')

        # Checken der Bedingungen
        # Fertigkeit 2 mal levelbar
        if (checkbutton <1 and levelkosten1<=self.APuebrig and len(levelkosten)>2):
            # überprüfen des aktuellen Levels
            if level <6:
                aufleveln = 1
            elif level>=6 and level<11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten1
            # Ausgabe AP und Level
            self.Label_APuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste[index][3].config(text=str(level))
            # Fertigkeit einmal gelevelt
            self.Fertigkeitsliste[index][5].select()

        elif checkbutton>0 and levelkosten2<=self.APuebrig and len(levelkosten)>2:
            # überprüfen des aktuellen Levels
            if level < 6:
                aufleveln = 1
            elif level >= 6 and level < 11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten2
            # Ausgabe AP und Level
            self.Label_APuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste[index][3].config(text=str(level))
            # Fertigkeit maximal gelevelt
            self.Fertigkeitsliste[index][4].config(state='disabled')
        # abfangen Fehler zur 'überlevelung'
        elif checkbutton < 1 and levelkosten1 > self.APuebrig and len(levelkosten) > 2:
            self.Fertigkeitsliste[index][4].config(state='disabled')
        elif checkbutton>0 and levelkosten2>self.APuebrig and len(levelkosten)>2:
            self.Fertigkeitsliste[index][4].config(state='disabled')
        # Fertigkeit 1 mal levelbar
        elif levelkosten1==levelkosten2 and levelkosten1<=self.APuebrig:
            # überprüfen des aktuellen Levels
            if level < 6:
                aufleveln = 1
            elif level >= 6 and level < 11:
                aufleveln = 0.5
            else:
                aufleveln = 0.25
            # Berechnung Level, übrigen AP
            level += aufleveln
            self.APuebrig -= levelkosten1
            # Ausgabe AP und Level
            self.Label_APuebrig.config(text='AP: ' + str(self.APuebrig))
            self.Fertigkeitsliste[index][3].config(text=str(level))
            # Fertigkeit maximal gelevelt
            self.Fertigkeitsliste[index][5].select()
            self.Fertigkeitsliste[index][4].config(state='disabled')
        # Abfangen von überlevelung
        elif levelkosten1==levelkosten2 and levelkosten1>self.APuebrig:
            self.Fertigkeitsliste[index][4].config(state='disabled')
        self.aktualisierenMana()

    def fertigkeitLoeschen(self, leiste):
        # leiste = Index, um 2 kleiner da Array bei 0 startet
        index = self.Fertigkeitsliste_row_hilfliste.index(leiste)
        for Objekt in self.Fertigkeitsliste[index]:
            Objekt.destroy()
        del self.Fertigkeitsliste[index]
        del self.Fertigkeitsliste_row_hilfliste[index]
        del self.cb[index]
        del self.auswahlfertigkeit[index]

    def aktualisierenLeben(self):
        ausgewaehlteKlasseI = self.klassen.index(self.klasse.get())
        ausgewaehltesVolk = self.voelker.index(self.volk.get())
        kontiBonus = int(self.Label_Rko.cget('text'))
        Stufe = int(self.CharStufe)

        volkLebenBonus = self.vLeben[ausgewaehltesVolk]
        volkLebenBonus = int(volkLebenBonus[1:])
        LebenBerechnung = self.kLebenuMana[ausgewaehlteKlasseI][0]
        LebenBerechnung = int(LebenBerechnung[:-1])

        self.Leben = ((LebenBerechnung+kontiBonus)*Stufe)+volkLebenBonus
        if self.Leben<0:
            self.Leben=0
        self.Label_Leben.config(text='Leben: ' + str(self.Leben))

    def aktualisierenMana(self):
        # Index herausfinden, um die aktuelle Klassenberechnung zu finden
        # Attribut und Bonus zur Manaberechnung
        stufeMEntwickeln = 0
        klasse_index=self.klassen.index(self.klasse.get())
        mAtt= self.kLebenuMana[klasse_index][1]
        mBonus = int(mAtt[:-1])
        mAtt = mAtt[-1]
        # Magie entwicklen - Stufe finden
        i=0
        for Objekt in self.auswahlfertigkeit:
            if Objekt.get()=='Magie entwickeln':
                stufeMEntwickeln = float(self.Fertigkeitsliste[i][3].cget('text'))
                break
            i += 1
        # Attribut Charisma oder Intelligenz, Att-Bonus herausfinden
        if mAtt == 'i':
            bonus = int(self.Label_Rin.cget('text'))
        else:
            bonus = int(self.Label_Rch.cget('text'))
        # Berechnung des Manas
        Mana = int(stufeMEntwickeln)*(bonus+mBonus)
        if Mana < 0:
            Mana = 0
        # Ausgabe
        self.Label_Mana.config(text=('Mana: ' + str(Mana)))

    def aktualisierenVolkattB(self, auswahl):
        volk_index = self.voelker.index(auswahl)
        volk_attB = self.vAtt[volk_index]
        self.resett()
        self.Label_stB.configure(text=volk_attB[0])
        self.Label_geB.configure(text=volk_attB[1])
        self.Label_koB.configure(text=volk_attB[2])
        self.Label_inB.configure(text=volk_attB[3])
        self.Label_chB.configure(text=volk_attB[4])

        self.st = int(volk_attB[0]) + int(self.eSt.get())
        self.ge = int(volk_attB[1]) + int(self.eGe.get())
        self.ko = int(volk_attB[2]) + int(self.eKo.get())
        self.inti = int(volk_attB[3]) + int(self.eIn.get())
        self.ch = int(volk_attB[4]) + int(self.eKo.get())

        self.Label_Gst.configure(text=str(self.st))
        self.Label_Gge.configure(text=str(self.ge))
        self.Label_Gko.configure(text=str(self.ko))
        self.Label_Gin.configure(text=str(self.inti))
        self.Label_Gch.configure(text=str(self.ch))

        self.attBonusBestimmen()

    def voelkerULebenUAttAuslesen(self, Dim2Array):
        i = 0
        volk = []
        vAtt = []
        vLeben = []
        for a in Dim2Array:
            volk.append(Dim2Array[i][0])
            vLeben.append(Dim2Array[i][1])
            vAtt.append(Dim2Array[i][2:])
            i += 1
        return volk, vLeben, vAtt

    def klassenUfKostenAuslasen(self, Array):
        i = 0
        klassen = []
        kLebenUmana=[]
        fKosten = []
        for zeile in Array:
            zeile = zeile.split()
            klassen.append(zeile[0])
            kLebenUmana.append(zeile[1:3])
            fKosten.append(zeile[3:])
        return klassen, kLebenUmana, fKosten

    def aktualisierenKlasse(self, inhalt):
        self.resett()

    # Kommands zum ändern der Attributspunkte und Zusammennrechnens der zu verbleibenden Punkte
    def aktualisierenATTkauf_st(self, Wert):
        kaufkosten = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        kaufpunkte = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        p_index = kaufpunkte.index(Wert)
        kaufkostenW = kaufkosten[p_index]
        self.kaufAtt[0] = kaufkostenW
        kaufAttsum = np.sum(self.kaufAtt)
        self.Label_attPuebrig.configure(text='Kaufpunkte übrig\n' + str(35 - kaufAttsum))

        vBonus = int(self.Label_stB.cget('text'))
        self.Label_Gst.configure(text=str(vBonus + Wert))
        self.attBonusBestimmen()

    def aktualisierenATTkauf_ge(self, Wert):
        kaufkosten = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        kaufpunkte = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        p_index = kaufpunkte.index(Wert)
        kaufkostenW = kaufkosten[p_index]
        self.kaufAtt[1] = kaufkostenW
        kaufAttsum = np.sum(self.kaufAtt)
        self.Label_attPuebrig.configure(text='Kaufpunkte übrig\n' + str(35 - kaufAttsum))

        vBonus = int(self.Label_geB.cget('text'))
        self.Label_Gge.configure(text=str(vBonus + Wert))
        self.attBonusBestimmen()

    def aktualisierenATTkauf_ko(self, Wert):
        kaufkosten = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        kaufpunkte = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        p_index = kaufpunkte.index(Wert)
        kaufkostenW = kaufkosten[p_index]
        self.kaufAtt[2] = kaufkostenW
        kaufAttsum = np.sum(self.kaufAtt)
        self.Label_attPuebrig.configure(text='Kaufpunkte übrig\n' + str(35 - kaufAttsum))

        vBonus = int(self.Label_koB.cget('text'))
        self.Label_Gko.configure(text=str(vBonus + Wert))
        self.attBonusBestimmen()
        self.aktualisierenLeben()

    def aktualisierenATTkauf_in(self, Wert):
        kaufkosten = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        kaufpunkte = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        p_index = kaufpunkte.index(Wert)
        kaufkostenW = kaufkosten[p_index]
        self.kaufAtt[3] = kaufkostenW
        kaufAttsum = np.sum(self.kaufAtt)
        self.Label_attPuebrig.configure(text='Kaufpunkte übrig\n' + str(35 - kaufAttsum))

        vBonus = int(self.Label_inB.cget('text'))
        self.Label_Gin.configure(text=str(vBonus + Wert))
        self.attBonusBestimmen()
        self.aktualisierenMana()

    def aktualisierenATTkauf_ch(self, Wert):
        kaufkosten = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        kaufpunkte = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        p_index = kaufpunkte.index(Wert)
        kaufkostenW = kaufkosten[p_index]
        self.kaufAtt[4] = kaufkostenW
        kaufAttsum = np.sum(self.kaufAtt)
        self.Label_attPuebrig.configure(text='Kaufpunkte übrig\n' + str(35 - kaufAttsum))

        vBonus = int(self.Label_chB.cget('text'))
        self.Label_Gch.configure(text=str(vBonus + Wert))
        self.attBonusBestimmen()
        self.aktualisierenMana()

    def auslesen(self, datei_namen):
        i = 0
        datei = open(datei_namen, "r")
        inhalt = datei.readlines()
        datei.close()
        for zeile in inhalt:
            zeile = zeile.strip('\n')
            inhalt[i] = zeile
            i += 1
        return inhalt

    def listStringToArray(self, lString):
        i = 0
        for zeile in lString:
            zeile = zeile.split()
            lString[i] = zeile
            i += 1
        return lString

    def attBonusBestimmen(self):
        punkte = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        Bonus = [-1000, -1000, -1000, -1000, -1000, -1000, -3, -2, -2, -1, 0, +1, +1, +2, +2, +3, +3, +4, +4, +5, +5, +6]
        Bonus_auswahl = [0, 0, 0, 0, 0]
        self.attGesamt = [0, 0, 0, 0, 0]

        self.attGesamt[0] = int(self.Label_Gst.cget('text'))
        self.attGesamt[1] = int(self.Label_Gge.cget('text'))
        self.attGesamt[2] = int(self.Label_Gko.cget('text'))
        self.attGesamt[3] = int(self.Label_Gin.cget('text'))
        self.attGesamt[4] = int(self.Label_Gch.cget('text'))

        i=0
        for Attribut in self.attGesamt:
            index = punkte.index(Attribut)
            Bonus_auswahl[i] = Bonus[index]
            i +=1

        self.Label_Rst.configure(text=Bonus_auswahl[0])
        self.Label_Rge.configure(text=Bonus_auswahl[1])
        self.Label_Rko.configure(text=Bonus_auswahl[2])
        self.Label_Rin.configure(text=Bonus_auswahl[3])
        self.Label_Rch.configure(text=Bonus_auswahl[4])

    def Bestaetigen(self):
        charakterMatrix=[]
        # Überprüfen leerer Fertigkeiten
        i=0
        j=[]
        for Zeile in self.Fertigkeitsliste:
            if Zeile[0]['state']=='normal':
                for Obj in Zeile:
                    Obj.destroy()
                j.append(i)
            i+=1
        for zeile in j[::-1]:
            del self.Fertigkeitsliste[zeile]
            del self.Fertigkeitsliste_row_hilfliste[zeile]
            del self.cb[zeile]
            del self.auswahlfertigkeit[zeile]

        # Überprüfung ob alles richtig ausgefüllt ist
        ausgefuellt=True
        #   Spielername und Charaaktername ausgefüllt?
        if self.Entry_spName.get() == '' and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Spielernamen eintragen!"
        if self.Entry_chName.get() == '' and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Charakternamen eintragen!"
        # Sind die Attributswerte richtig ausgefüllt?
        if int(self.Label_Gst.cget('text')) ==0 and ausgefuellt==True:
            ausgefuellt=False
            nachricht = "Stärke muss Gesamt mindestens = 1 sein!"
        if int(self.Label_Gge.cget('text')) == 0 and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Geschicklichkeit muss Gesamt mindestens = 1 sein!"
        if int(self.Label_Gko.cget('text')) == 0 and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Konstitution muss Gesamt mindestens = 1 sein!"
        if int(self.Label_Gin.cget('text')) == 0 and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Intelligenz muss Gesamt mindestens = 1 sein!"
        if int(self.Label_Gch.cget('text')) == 0 and ausgefuellt==True:
            ausgefuellt = False
            nachricht = "Charisma muss Gesamt mindestens = 1 sein!"
        # Sind zu viele Attributspunkte verbraucht?
        if (35-np.sum(self.kaufAtt))<0 and ausgefuellt == True:
            ausgefuellt = False
            nachricht = "Zu viele Attributspunkte ausgegeben!"
        # Sind zu wenig Attributspunkte verbraucht? Gib Frage aus, ob weiterverfahren werden soll
        if (35-np.sum(self.kaufAtt))>0 and ausgefuellt==True:
            messagebox_Frage = tk.messagebox.askquestion('Fortfahren?', 'Es sind noch Attributspunkte zum Ausgeben verfügbar. Wollen Sie trotzdem die Charaktererstellung beenden?', icon='warning')
            if messagebox_Frage =='no':
                return
        # Ausgabe der Error
        if ausgefuellt == False:
            tk.messagebox.showerror("Warnung", nachricht)
            return

        # Überprüfen ob der Charakter schon exestiert
        if not os.path.exists((os.getcwd()+'\\charaktere\\' + self.Entry_chName.get() + '.txt')):
            file_Charakter = open((os.getcwd()+'\\charaktere\\' + self.Entry_chName.get() + '.txt'),'w+')
        else:
            tk.messagebox.showerror('Charakterfehler', 'Dieser Charakter exestiert schon!')
            return
        # Allgemeinen Angaben anfügen
        charakterMatrix.append('Spielername: '+self.Entry_spName.get())
        charakterMatrix.append('Charaktername: '+self.Entry_chName.get())
        charakterMatrix.append(self.volk.get())
        charakterMatrix.append(self.klasse.get())
        # Stufe, Leben, Mana anfügen
        charakterMatrix.append(self.Label_CharStufe.cget('text'))
        charakterMatrix.append('AP: ' + str(self.APuebrig))
        charakterMatrix.append(self.Label_Leben.cget('text'))
        charakterMatrix.append(self.Label_Mana.cget('text'))
        # Attribute + Boni anfügen
        charakterMatrix.append((str(self.Label_Gst.cget('text'))+', '+ str(self.Label_Rst.cget('text'))))
        charakterMatrix.append((str(self.Label_Gge.cget('text'))+', '+ str(self.Label_Rge.cget('text'))))
        charakterMatrix.append((str(self.Label_Gko.cget('text'))+', '+ str(self.Label_Rko.cget('text'))))
        charakterMatrix.append((str(self.Label_Gin.cget('text'))+', '+ str(self.Label_Rin.cget('text'))))
        charakterMatrix.append((str(self.Label_Gch.cget('text'))+', '+ str(self.Label_Rch.cget('text'))))
        # Fertigkeiten anfügen
        # Format: Fertgikeit, Notiz, Kosten, Stufe, 0/1/2 gelevelt?
        i = 0
        for liFertigkeit in self.Fertigkeitsliste:
            Fertigkeit = self.auswahlfertigkeit[i].get()
            Notiz = liFertigkeit[1].cget('text')
            Stufe = liFertigkeit[3].cget('text')
            kosten = liFertigkeit[2].cget('text')
            # 0 = gar nicht gelevelt, 1 = 1 von 2 gelevelt, 2 vollgelevelt
            if self.cb[i].get() == 1:
                gelevelt = 1
                if liFertigkeit[4]['state'] == 'disabled':
                    gelevelt = 2
            else:
                gelevelt = 0
            listFertigkeit = str(Fertigkeit)+', '+ (Notiz)+', '+ (Stufe)+', '+ (kosten)+', '+ str(gelevelt)
            charakterMatrix.append(listFertigkeit)
            i+=1
        for j in charakterMatrix:
            file_Charakter.write(str(j) + '\n')
        file_Charakter.close()


def pfadeInitialisieren():
    pfad=os.getcwd()
    if not os.path.exists((pfad+'\\klassen.txt')):
        f = open('klassen.txt','w+')
        f.write("Krieger 10k 3i 1 2 4 1 2 4&8 2 1 2 4&8 1&3 1 2" + '\n')
        f.close()

    if not os.path.exists((pfad+'\\' + 'voelker.txt')):
        f = open('voelker.txt','w+')
        f.write("Mensch L0 0 0 0 0 0 "+'\n')
        f.close()

    if not os.path.exists((pfad+'\\' + 'fertigkeiten.txt')):
        f = open('fertigkeiten.txt','w+')
        f.write('Athletik'+'\n')
        f.close()

    if not os.path.exists(pfad+'\\charaktere'):
        os.makedirs(pfad+'\\charaktere')


def main():
    pfadeInitialisieren()
    root = tk.Tk()
    root.title('Charakterhilfe')
    app = Hauptfenster(root)
    root.mainloop()


if __name__ == '__main__':
    main()
