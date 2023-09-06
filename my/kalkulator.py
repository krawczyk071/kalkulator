import pandas as pd
import numpy as np
import requests
import math
from mytypes import *


class Kalkulator:
    # laczne_odsetki = 0
    # ostatnia_zmiana = 0

    def __init__(
        self,
        kwota_kredytu: int,
        okres_splat: OkresSplaty = OkresSplaty.raty_miesieczne,
        ilosc_lat: int = 10,
        rodzaj_oprocentowania: RodzajOprocentowania = RodzajOprocentowania.zmienne,
        stopa_procentowa: float = 8,
        stopa_procentowa2: float = None,
        stopa_procentowa3: float = None,
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
        self.r2 = stopa_procentowa2 / 100 if stopa_procentowa2 else self.r
        self.r3 = stopa_procentowa3 / 100 if stopa_procentowa3 else self.r2

        self.columns = [
            "Numer raty",
            "Kapitał na początku okresu",
            "Rata kapitałowa",
            "Rata odsetkowa",
            "Dopłata",
            "Rata łączna",
            "Kapitał na koniec okresu",
            "Odsetki_po",
            "po_laczna",
        ]
        self.tabela_splat = pd.DataFrame(columns=self.columns)

        # self._calc_rata_laczna()
        # self.oblicz_kapitalizacje()
        # self.oblicz_laczna_rate()

        self.rata_kapitalowa = round(self.kapital / self.ilosc_rat, 2)

        self.generuj_harmonogram()

    def _set_ilosc_rat(self, okres_splat, ilosc_lat):
        if ilosc_lat <= 35:
            self.ilosc_rat = ilosc_lat * okres_splat.value
        else:
            raise Exception("Kredyt może trwać maksymalnie 35 lat!")

    # def oblicz_kapitalizacje(self):
    #     r = self.r
    #     k = self.k
    #     m = self.m
    #     if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
    #         self.kapitalizacja = math.exp((r / k))
    #     elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
    #         self.kapitalizacja = (1 + r / m) ** (m / k)
    #     else:
    #         raise Exception("Nieznany rodzaj kapitalizacji")

    def generuj_harmonogram(self):
        # m = self.m #okres_kapitalizacji(ciagla)
        tabela_splat = self.tabela_splat

        def do_doplaty(nr_raty, pozostaly_kapital):
            if (nr_raty > 120) | (self.rodzaj_rat != RodzajRat.bezpieczny):
                return 0
            return round(pozostaly_kapital * ((self.wskaznikBGK / 100) - 0.02) / 12, 2)

        if self.rodzaj_rat == RodzajRat.malejace:
            kapitalowe, odsetkowe, zadluzenia = self._harm_malejace()
        if self.rodzaj_rat == RodzajRat.rowne:
            kapitalowe, odsetkowe, zadluzenia = self._harm_rowne()

        if self.rodzaj_rat == RodzajRat.bezpieczny:
            kapitalowe, odsetkowe, zadluzenia = self._harm_malejace()
            # bo doplaty przez 10lat a pozniej rowne
            kapitalowe_po, odsetkowe_po, zadluzenia_po = self._harm_rowne(
                pozostalo=zadluzenia[120]
            )

        for i in range(self.ilosc_rat - 1):
            numer_raty = i + 1
            if (self.rodzaj_rat == RodzajRat.bezpieczny) & (numer_raty > 120):
                step = 120
                tabela_splat.loc[i] = [
                    numer_raty,
                    zadluzenia_po[i - step],
                    kapitalowe_po[i - step],
                    odsetkowe_po[i - step],
                    0,
                    kapitalowe_po[i - step] + odsetkowe_po[i - step],
                    zadluzenia_po[i - step] - kapitalowe_po[i - step],
                    odsetkowe_po[i - step] - 0,
                    kapitalowe_po[i - step] + odsetkowe_po[i - step] - 0,
                ]
            else:
                doplata = do_doplaty(numer_raty, zadluzenia[i])
                tabela_splat.loc[i] = [
                    numer_raty,
                    zadluzenia[i],
                    kapitalowe[i],
                    odsetkowe[i],
                    doplata,
                    kapitalowe[i] + odsetkowe[i],
                    zadluzenia[i] - kapitalowe[i],
                    odsetkowe[i] - doplata,
                    kapitalowe[i] + odsetkowe[i] - doplata,
                ]

        # zmiana typu kolumny
        tabela_splat["Numer raty"] = tabela_splat["Numer raty"].astype(int)

    def _harm_rowne(self, pozostalo=None):
        k = self.k  # okres_splat(miesiecznie-12)
        r = self.r3  # oprocentowanie
        if self.rodzaj_rat == RodzajRat.bezpieczny:
            n = self.ilosc_rat - (self.okres_splat.value * 10)
            kredyt = pozostalo
        else:
            n = self.ilosc_rat  # ilosc_rat
            kredyt = self.kapital
        pozostale_zadluzenie = kredyt
        # suma = 0

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
            # suma += czesc_odsetkowa
        return kapitalowe, odsetkowe, zadluzenia

    def _harm_malejace(self):
        k = self.k  # okres_splat(miesiecznie-12)
        r = self.r  # oprocentowanie w pierwszym 5leciu
        r2 = self.r2  # oprocentowanie w 2 5 leciu
        n = self.ilosc_rat  # ilosc_rat
        kredyt = self.kapital
        pozostale_zadluzenie = kredyt
        czesc_kapitalowa = round(kredyt / n, 2)

        kapitalowe = [czesc_kapitalowa for i in range(n)]
        odsetkowe = []
        zadluzenia = [kredyt]

        def calc_rata_odsetkowa(r):
            nonlocal pozostale_zadluzenie
            czesc_odsetkowa = round(pozostale_zadluzenie * r / k, 2)
            odsetkowe.append(czesc_odsetkowa)

            pozostale_zadluzenie -= czesc_kapitalowa
            zadluzenia.append(pozostale_zadluzenie)

        for i in range(n):
            if i < k * 5:
                calc_rata_odsetkowa(r)
            else:
                calc_rata_odsetkowa(r2)

        return kapitalowe, odsetkowe, zadluzenia

    def harmonogram_to_DF(self):
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            return self.tabela_splat

    def raty_to_list(self) -> list:
        return self.tabela_splat["po_laczna"].apply(round).to_list()

    def totals_to_dict(self, short=False) -> dict:
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            new = [
                "total_kapital",
                "bezdoplaty_total_odsetki",
                "total_doplata",
                "bezdoplaty_total_raty",
                "total_odsetki",
                "total_raty",
            ]
            old = [
                "Rata kapitałowa",
                "Rata odsetkowa",
                "Dopłata",
                "Rata łączna",
                "Odsetki_po",
                "po_laczna",
            ]

            cols_renamer = dict(zip(old, new))
            df_new = self.tabela_splat[old].rename(columns=cols_renamer)

            tot_dict = df_new.sum().apply(round).to_dict()
            if short == False:
                return tot_dict
            else:
                return {
                    k: v
                    for k, v in tot_dict.items()
                    if k in ["total_doplata", "total_odsetki", "total_raty"]
                }


Kalkulator(
    kwota_kredytu=450000,
    ilosc_lat=20,
    stopa_procentowa=7.14,
    stopa_procentowa3=9,
    rodzaj_rat=RodzajRat.bezpieczny,
    wskaznikBGK=7.14,
)
