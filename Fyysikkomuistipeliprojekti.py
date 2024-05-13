# TIE-02100 Johdatus ohjelmointiin, kevät 2020

# Tehtävä 13.10, Skaalautuva graafinen kayttoliittyma -projekti Tkinterilla

# Fyysikkomuistipeli:

# Tavallinen korttimuistipeli, oletuksena kaksi pelaajaa. Pelaajamäärää voi
# muokata muuttamalla alussa määriteltyä vakiota PLAYERNUM. Pelissä on 18
# korttiparia eli 36 korttia, teemana historian suurimmat fyysikot. Aina parin
# löytyessä pelaaja saa jatkaa vuoroaan. Pelin voittaa se, jolla on korttien
# loputtua eniten pareja. Käytännössä kortit ovat listaan tallennettuja
# buttoneja, joihin on yhdistetty kääntötoiminto. Tavoitteena on saavuttaa
# skaalautuvalle projektille asetetut vaatimukset.


from tkinter import *
import random
import math

CARDPICS = {"Maxwell": "Maxwell.gif", "Einstein": "Einstein.gif",
            "Curie": "Curie.gif", "Tesla": "Tesla.gif",
            "Hawking": "Hawking.gif", "Feynman": "Feynman.gif",
            "Galilei": "Galilei.gif", "Newton": "Newton.gif",
            "Schrodinger": "Schrodinger.gif", "Planck": "Planck.gif",
            "Faraday": "Faraday.gif", "Heisenberg": "Heisenberg.gif",
            "Fermi": "Fermi.gif", "Rontgen": "Rontgen.gif",
            "Compton": "Compton.gif", "Ampere": "Ampere.gif",
            "Arkhimedes": "Arkhimedes.gif", "Bohr": "Bohr.gif", }

BACKGROUND_CARD = "Background.gif"
BLANK_CARD = "Blank.gif"

PLAYERNUM = 2
CARDNUM = 36


class Memorygame:

    def __init__(self):

        self.__mainwindow = Tk()
        self.__mainwindow.title("Fyysikkomuistipeli")

        self.__turn = 0
        self.__open_cards = 0
        self.__collected_pairs = [0] * PLAYERNUM

        self.__first_cardname = None
        self.__second_cardname = None

        self.__first_buttonnumber = None
        self.__second_buttonnumber = None

        self.__closing_cards = False
        self.__collecting_cards = False

        # Jos kortti on auki, on sen kohdalla True
        self.__open_cards_list = [False] * CARDNUM
        # Jos button ei ole käytössä, on sen kohdalla True
        self.__disabled_buttons_list = [False] * CARDNUM

        self.__cardpic_dict = {}
        for picturename in CARDPICS:
            picturefile = CARDPICS[picturename]
            cardpicture = PhotoImage(file=picturefile)
            self.__cardpic_dict[picturename] = cardpicture

        self.__card_name_list = []
        for picturename in CARDPICS:
            # Lisataan listaan joka kuvannimi kahdesti pareja varten
            for i in range(2):
                self.__card_name_list.append(picturename)

        # Nimet sekoitetaan
        random.shuffle(self.__card_name_list)

        # Korttien taustat
        self.__background_card = PhotoImage(file=BACKGROUND_CARD)
        # Buttonin kuvan paikalle asetetaan parin loytymisen jalkeen valkoinen
        # taustakuva Blank
        self.__blank_card = PhotoImage(file=BLANK_CARD)

        for i in range(PLAYERNUM):
            Label(self.__mainwindow, text="Pelaajalla " + str(i + 1) +
                  " pareja:").grid(row=i, column=0, columnspan=2)

        self.__pointslabel_list = []
        for i in range(PLAYERNUM):
            pointslabel = Label(text=0)
            pointslabel.grid(row=i, column=2, sticky=W)
            self.__pointslabel_list.append(pointslabel)

        self.__cardbuttons = []
        for i in range(CARDNUM):
            cardbutton = Button(image=self.__background_card, command=lambda
                                x=i: self.flip(x))
            self.__cardbuttons.append(cardbutton)

        # Korteista muodostetaan 6x6 neliö
        k = 0
        for i in range(6):
            for j in range(6):
                self.__cardbuttons[k].grid(column=j, row=i + PLAYERNUM)
                k += 1

        self.__physicistname_label = Label(text="Fyysikon nimi:")
        self.__turn_info_label = Label(text="Pelaajan 1 vuoro")
        self.__infolabel = Label(
            text="Pelaaja 1, aloita peli kääntämällä kortti")
        self.__endbutton = Button(text="Lopeta", background="red",
                                  foreground="black", command=self.stop)
        self.__newbutton = Button(text="Uusi peli", background="green",
                                  foreground="black", command=self.initialize)

        self.__physicistname_label.grid(row=1, column=3, columnspan=2,
                                        sticky=W)
        self.__turn_info_label.grid(row=0, column=3)
        self.__infolabel.grid(row=int(math.sqrt(CARDNUM)) + PLAYERNUM,
                              column=0,
                              columnspan=4)
        self.__endbutton.grid(row=int(math.sqrt(CARDNUM)) + PLAYERNUM,
                              column=5)
        self.__newbutton.grid(row=int(math.sqrt(CARDNUM)) + PLAYERNUM,
                              column=4)

    def flip(self, buttonnumber):
        """ Kortin kääntotoiminto. Ohjaa tilanteen mukaan seuraavaan metodiin
        riippuen siitä, onko tarkoitus avata, kerätä vai sulkea kortti.
        :param buttonnumber: painetun nappulan järjestysnumero
        :return: -
        """
        if self.__closing_cards:
            self.flip_card_back(buttonnumber)

        elif self.__collecting_cards:
            self.collect_card(buttonnumber)

        else:
            self.open_card(buttonnumber)

    def open_card(self, buttonnumber):
        """ Kortin avaamismetodi. Vaihtaa nappulan kuvan backgroundista,
        tarkistaa onko tullut pari, kertoo fyysikon nimen labelissa
        :param buttonnumber: painetun nappulan järjestysnumero
        :return: -
        """
        # Varmistetaan, että avattava kortti on eri kuin ensimmäinen nostettu
        if self.__open_cards_list[buttonnumber]:
            self.__infolabel.configure(text="Käännä eri kortti")
        else:
            # Lisataan tieto kyseisen kortin aukaisusta listaan
            self.__open_cards_list[buttonnumber] = True
            self.__open_cards += 1
            # Nimilistasta etsitaan buttonin indeksia vastaava kuvan nimi
            cardname = self.__card_name_list[buttonnumber]
            # Kuvan nimea kaytetaan dictin keyna varsinaisen kuvan saamiseksi
            cardpic = self.__cardpic_dict[cardname]
            self.__cardbuttons[buttonnumber].configure(image=cardpic)
            self.__physicistname_label.configure(
                text="Fyysikon nimi: " + cardname)

            # Jos kortteja on auki 1, käsketään avaamaan toinen
            if self.__open_cards == 1:
                self.__first_buttonnumber = buttonnumber
                self.__first_cardname = cardname
                self.__infolabel.configure(text="Avaa toinen kortti")

            # Jos taas 2, tehdään paritarkastelu
            elif self.__open_cards == 2:
                self.__second_buttonnumber = buttonnumber
                self.__second_cardname = cardname

                if self.__first_cardname == self.__second_cardname:
                    self.pair()
                else:
                    self.__infolabel.configure(
                        text="Ei paria, käännä kortit takaisin väärinpäin")
                    self.__closing_cards = True

    def collect_card(self, buttonnumber):
        """ Kortin keräämismetodi. Jos attribuutti __collecting_cards on
        tosi, ohjataan nappulan painamisen jalkeen tänne. Metodi tekee
        varmistukset, etta kyseessa on oikea nappula, ja "poistaa" kortin
        kentalta, eli lukitsee nappulan ja asettaa nappulan kuvaksi tyhjän
        valkoisen kuvan. Peli päättyy, jos kaikki kortit on kerätty.
        :param buttonnumber: painetun nappulan järjestysnumero
        :return:-
        """
        # Varmistetaan, että valittu kortti on todella tarkoitus kerata pois
        # pelialueelta
        if not self.__open_cards_list[buttonnumber]:
            self.__infolabel.configure(
                text="Kerää ensin saamasi kortit talteen")
        else:
            self.__open_cards_list[buttonnumber] = False
            button = self.__cardbuttons[buttonnumber]
            # Lukitaan nappula
            button.configure(image=self.__blank_card, state=DISABLED)

            self.__open_cards -= 1
            if self.__open_cards == 1:
                self.__infolabel.configure(text="Kerää toinen kortti")
            else:
                self.__collecting_cards = False
                # Tutkitaan, pitääkö pelin loppua
                if self.check_for_game_end():
                    self.winning()
                else:
                    self.__infolabel.configure(text="Pelaaja " + str(
                        self.__turn + 1) + " saa uuden vuoron")

    def flip_card_back(self, buttonnumber):
        """ Kortin sulkemismetodi. Buttonin painamisen jälkeen ohjataan tänne,
        jos attribuutti __closing_cards on tosi. Tarkistaa, että painettu
        nappula on oikea ja "kääntää" kortin takaisin väärinpäin eli vaihtaa
        kuvan taustakuvaan.
        :param buttonnumber: painetun nappulan järjestysnumero
        :return:
        """
        # Varmistetaan, että kortti on todella tarkoitus kääntää väärinpain
        if not self.__open_cards_list[buttonnumber]:
            self.__infolabel.configure(
                text="Käännä ensin avaamasi kortit takaisin väärinpäin")
        else:
            button = self.__cardbuttons[buttonnumber]
            button.configure(image=self.__background_card)
            self.__open_cards_list[buttonnumber] = False
            self.__open_cards -= 1

            if self.__open_cards == 1:
                self.__infolabel.configure(text="Käännä toinen kortti")
            else:
                self.__closing_cards = False
                self.end_turn()

    def check_for_game_end(self):
        """ Metodi tutkii, onko kaikki kortit kerätty eli pitääkö peli päättää
        :return: True, jos pelin pitää loppua, muuten False
        """
        if sum(self.__collected_pairs) == CARDNUM / 2:
            return True
        else:
            return False

    def winning(self):
        """ Pelin päättävä metodi, sisältää voittotarkastelun
        :return: -
        """
        max_pairs_list = []
        max_pairs = max(self.__collected_pairs)
        # Kerätään suurimmat pisteet saaneiden pelaajien indeksit listaan
        for k in range(PLAYERNUM):
            if self.__collected_pairs[k] == max_pairs:
                max_pairs_list.append(str(k + 1))
        # Jos monella pelaajalla on yhtä paljon pareja, on peli tasapeli
        if len(max_pairs_list) > 1:
            self.__infolabel.configure(
                text="Tasapeli! Pelaajat " + " ja ".join(
                    max_pairs_list) + " jakavat voiton!")
        # Muuten eniten pareja löytänyt voittaa
        else:
            most_points = max(self.__collected_pairs)
            winner = self.__collected_pairs.index(most_points)
            self.__infolabel.configure(
                text="Pelaaja " + str(winner + 1) + " voittaa!")

    def end_turn(self):
        """ Vuoron päättävä metodi. Päivittää kirjanpitoattribuutin __turn ja
        infolabelit
        :return: -
        """
        self.__turn += 1
        if self.__turn == PLAYERNUM:
            self.__turn = 0

        self.__turn_info_label.configure(
            text="Pelaajan " + str(self.__turn + 1) + " vuoro")
        self.__infolabel.configure(
            text="Pelaaja " + str(self.__turn + 1) + ", kaanna kortti")

    def pair(self):
        """ Metodi kasvattaa parin saaneen pistesaldoa ja antaa tälle uuden
        vuoron. Päivittää infolabelit. Attribuutti __collecting_cards saa arvon
         True, jotta korttien kerääminen onnistuu
        :return: -
        """
        self.__collected_pairs[self.__turn] += 1
        self.__pointslabel_list[self.__turn].configure(
            text=str(self.__collected_pairs[self.__turn]))
        self.__infolabel.configure(text="Löysit parin! Kerää kortit itsellesi")
        self.__collecting_cards = True

    def initialize(self):
        """ Uuden peli alustava metodi. Asettaa kaikki attribuutien arvot
        oletus/lähtöarvoiksi, "sekoittaa kortit"
        :return: -
        """
        self.__turn = 0
        self.__open_cards = 0
        self.__collected_pairs = [0] * PLAYERNUM

        self.__first_cardname = None
        self.__second_cardname = None

        self.__first_buttonnumber = None
        self.__second_buttonnumber = None

        self.__closing_cards = False
        self.__collecting_cards = False

        self.__open_cards_list = [False] * CARDNUM
        self.__disabled_buttons_list = [False] * CARDNUM

        random.shuffle(self.__card_name_list)
        self.__physicistname_label.configure(text="Fyysikon nimi:")
        self.__turn_info_label.configure(text="Pelaajan 1 vuoro")
        self.__infolabel.configure(
            text="Pelaaja 1, aloita peli kääntämällä kortti")

        for pointslabel in self.__pointslabel_list:
            pointslabel.configure(text="0")

        for cardbutton in self.__cardbuttons:
            cardbutton.configure(image=self.__background_card, state=NORMAL)

    def stop(self):
        """ Pelin lopettava metodi
        :return: -
        """
        self.__mainwindow.destroy()

    def start(self):
        """ Pelin aloittava metodi
        :return: -
        """
        self.__mainwindow.mainloop()


def main():
    ui = Memorygame()
    ui.start()


main()
