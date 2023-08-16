from Kalkulator_klasa import Kalkulator
from parametry import *

kalkulator2 = Kalkulator(
    kwota_kredytu=380000,
    ilosc_rat=250,
    okres_splat=OkresSplaty.raty_miesieczne,
    rodzaj_rat=RodzajRat.kapitalowe,
    rodzaj_oprocentowania=RodzajOprocentowania.zmienne,
    r_kapitalizacji=RodzajKapitalizacji.okresowa,
    okres_kapitalizacji=OkresyKapitalizacji.miesieczna,  # okresy nieużywanie w przypadku kapitalizacji ciągłej
)
kalkulator2.generuj_harmonogram()
kalkulator2.pokaz_harmonogram()
