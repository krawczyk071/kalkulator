import pandas as pd
import numpy as np
import requests
import math
from mytypes import *


class Kalkulator:
    laczne_odsetki = 0
    ostatnia_zmiana = 0

    def __init__(
        self,
        kwota_kredytu: int,
        okres_splat: OkresSplaty = OkresSplaty.raty_miesieczne,
        ilosc_lat: int = 10,
        rodzaj_oprocentowania: RodzajOprocentowania = RodzajOprocentowania.zmienne,
        stopa_procentowa: float = 8,
        wskaznikBGK: float = 7.14,
        rodzaj_rat: RodzajRat = RodzajRat.rowne,
        r_kapitalizacji: RodzajKapitalizacji = RodzajKapitalizacji.ciagla,
        okres_kapitalizacji: OkresyKapitalizacji = OkresyKapitalizacji.miesieczna,
    ):
        self.kapital = kwota_kredytu
        self._set_ilosc_rat(okres_splat, ilosc_lat)
        self.okres_splat = okres_splat
        self.rodzaj_oprocentowania = rodzaj_oprocentowania
        self.stopa_procentowa = stopa_procentowa
        self.wskaznikBGK = wskaznikBGK
        self.rodzaj_rat = rodzaj_rat
        self.r_kapitalizacji = r_kapitalizacji
        self.okres_kapitalizacji = okres_kapitalizacji
        self.m = okres_kapitalizacji.value
        self.k = okres_splat.value
        self.r = stopa_procentowa / 100

        self.columns = [
            "Numer raty",
            "Kapitał na początku okresu",
            "Rata kapitałowa",
            "Rata odsetkowa",
            "Dopłata",
            "Rata łączna",
            "Kapitał na koniec okresu",
        ]
        self.tabela_splat = pd.DataFrame(columns=self.columns)

        # self._calc_rata_laczna()
        self.oblicz_kapitalizacje()
        self.oblicz_laczna_rate()

        self.rata_kapitalowa = round(self.kapital / self.ilosc_rat, 2)

        # self.generuj_harmonogram()
        self.inaczej()

    def _set_ilosc_rat(self, okres_splat, ilosc_lat):
        if ilosc_lat <= 35:
            self.ilosc_rat = ilosc_lat * okres_splat.value
        else:
            raise Exception("Kredyt może trwać maksymalnie 35 lat!")

    # def _calc_rata_laczna(self):
    #     if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
    #         self.kapitalizacja = math.exp((self.r / self.k))
    #         self.rata_laczna = round(
    #             (
    #                 self.kapital
    #                 * math.exp(self.r / self.k * self.ilosc_rat)
    #                 * (math.exp(self.r / self.k) - 1)
    #                 / (math.exp(self.r / self.k * self.ilosc_rat) - 1)
    #             ),
    #             2,
    #         )
    #     elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
    #         self.kapitalizacja = (1 + self.r / self.m) ** (self.m / self.k)
    #         self.rata_laczna = round(
    #             (
    #                 self.kapital
    #                 * self.r
    #                 / (self.k * (1 - (self.k / (self.k + self.r)) ** self.ilosc_rat))
    #             ),
    #             2,
    #         )
    #     else:
    #         raise Exception("Nieznany rodzaj kapitalizacji")
    def oblicz_kapitalizacje(self):
        r = self.r
        k = self.k
        m = self.m
        if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
            self.kapitalizacja = math.exp((r / k))
        elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
            self.kapitalizacja = (1 + r / m) ** (m / k)
        else:
            raise Exception("Nieznany rodzaj kapitalizacji")

    def oblicz_laczna_rate(self):
        r = self.r
        n = self.ilosc_rat
        k = self.k
        self.rata_kapitalowa = round(self.kapital / n, 2)
        if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
            self.rata_laczna = round(
                (
                    self.kapital
                    * math.exp(r / k * n)
                    * (math.exp(r / k) - 1)
                    / (math.exp(r / k * n) - 1)
                ),
                2,
            )
        elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
            self.rata_laczna = round(
                (self.kapital * r / (k * (1 - (k / (k + r)) ** n))), 2
            )
        else:
            raise Exception("Nieznany rodzaj kapitalizacji")

    def inaczej(self):
        # m = self.m #okres_kapitalizacji(ciagla)
        k = self.k  # okres_splat(miesiecznie-12)
        r = self.r  # oprocentowanie
        n = self.ilosc_rat  # ilosc_rat
        kredyt = self.kapital

        pozostale_zadluzenie = kredyt
        suma = 0

        if self.rodzaj_rat == RodzajRat.malejace:
            czesc_kapitalowa = round(kredyt / n, 2)

            kapitalowe = [czesc_kapitalowa for i in range(n)]
            odsetkowe = []
            raty = []
            zadluzenia = [kredyt]

            for i in range(n):
                czesc_odsetkowa = round(pozostale_zadluzenie * r / k, 2)
                odsetkowe.append(czesc_odsetkowa)
                raty.append(czesc_kapitalowa + czesc_odsetkowa)

                pozostale_zadluzenie -= czesc_kapitalowa
                zadluzenia.append(pozostale_zadluzenie)
                suma += czesc_odsetkowa

        if self.rodzaj_rat == RodzajRat.rowne:
            kapitalowe = []
            odsetkowe = []
            zadluzenia = [kredyt]

            sumka = 0
            for i in range(1, n + 1):
                sumka += (1 + (r / k)) ** (-i)

            rata = round(kredyt / sumka, 2)
            # raty = [rata for i in range(n)]

            for i in range(n):
                czesc_odsetkowa = round(pozostale_zadluzenie * r / k, 2)
                odsetkowe.append(czesc_odsetkowa)
                kapitalowe.append(round(rata - czesc_odsetkowa, 2))

                pozostale_zadluzenie -= rata - czesc_odsetkowa
                zadluzenia.append(pozostale_zadluzenie)
                suma += czesc_odsetkowa

        # def generuj_harmonogram2(self):
        tabela_splat = self.tabela_splat
        # kapitalowe = []
        # odsetkowe = []
        # zadluzenia = [kredyt]

        for i in range(self.ilosc_rat - 1):
            numer_raty = i + 1

            # Wskaźnik średniej kwartalnej stopy procentowej BGK
            def do_doplaty(nr_raty, pozostaly_kapital):
                if (nr_raty > 10 * k) | (self.rodzaj_rat == RodzajRat.rowne):
                    return 0
                return round(
                    pozostaly_kapital * ((self.wskaznikBGK / 100) - 0.02) / k, 2
                )

            tabela_splat.loc[i] = [
                numer_raty,
                zadluzenia[i],
                kapitalowe[i],
                odsetkowe[i],
                do_doplaty(numer_raty, zadluzenia[i]),
                kapitalowe[i] + odsetkowe[i],
                zadluzenia[i] - kapitalowe[i],
            ]

        # zmiana typu kolumny
        tabela_splat["Numer raty"] = tabela_splat["Numer raty"].astype(int)

    def generuj_harmonogram(self, oblicz_nowa_laczna: bool = True):
        # if oblicz_nowa_laczna:
        #     self.oblicz_laczna_rate()

        # self.oblicz_kapitalizacje()
        tabela_splat = self.tabela_splat
        kapital = self.kapital
        rata_laczna = self.rata_laczna
        rata_kapitalowa = self.rata_kapitalowa

        for i in range(self.ilosc_rat - 1):
            numer_raty = i + 1
            # nie potrzbnie dolicza odsetki do pierwszej raty?
            k0 = round(kapital * self.kapitalizacja, 2)
            odsetki = round(k0 - kapital, 2)

            if self.rodzaj_rat == RodzajRat.rowne:
                rata_kapitalowa = rata_laczna - odsetki
            elif self.rodzaj_rat == RodzajRat.malejace:
                rata_laczna = rata_kapitalowa + odsetki
            k1 = k0 - rata_laczna
            # Wskaźnik średniej kwartalnej stopy procentowej BGK
            # wBGK=7.14
            doplata = (
                kapital * ((self.wskaznikBGK / 100) - 0.02) / self.okres_splat.value
            )
            if k1 < 0:
                continue
            tabela_splat.loc[i] = [
                numer_raty,
                k0,
                rata_kapitalowa,
                odsetki,
                doplata,
                rata_laczna,
                k1,
            ]
            kapital = k1
        # OSTATNIA
        # Ostatnia rata może mieć inną kwotę kapitałową i łączną niż poprzednie raty
        # (kapitału może pozostać mniej lub więcej niż kwota równej raty łącznej
        k0 = round(kapital * self.kapitalizacja, 2)
        odsetki = round(k0 - kapital, 2)
        tabela_splat.loc[self.ilosc_rat - 1] = [
            self.ilosc_rat,
            k0,
            kapital,
            odsetki,
            0,
            k0,
            0,
        ]

        # zmiana typu kolumny
        tabela_splat["Numer raty"] = tabela_splat["Numer raty"].astype(int)

        # return tabela_splat

    def harmonogram_to_DF(self):
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            return self.tabela_splat
