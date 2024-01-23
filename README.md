<p align="center">
  <img src="/doc/PlzenskyPoharPravdyLogo.png" alt="PPP logo"/>
</p>


# Plzeňský Pohár Pravdy

Uskupení několika datových zdrojů které se načítají do interaktivní webové aplikace, bylo zpracováno týmem plajta na HackujStat ver. 5.
Aplikace nabízí hned několik funkcionalit:
- Funkční nuke tester který dokáže z příslušných otevřených dat vygenerovat bližší kontext co by se stalo kdyby byla na území jakéhokoliv města (které si vybere uživatel) odpálena jaderná bomba
- Generování zajímavých faktů v oblasti polohy uživatele

## Oprávnění webové aplikace
- Aplikace potřebuje ke správnému fungování přístup k poloze, aby mohla vyhledat pozici člověka na mapě

## Užitečné odkazy

### Zpracované data

Použili jsem velmi zajímavou a rozsáhlou škálu dat.

- [sčítání lidu 2021](https://www.czso.cz/csu/czso/vysledky-scitani-2021-otevrena-data)
- [pohyb obyvatel 2022](https://www.czso.cz/documents/62353418/213522460/130141-23data2022.csv)
- [počet školských zařízení](https://www.czso.cz/documents/62353418/198619764/230057-23data101923.csv)
- [počet turu a prasat](https://www.czso.cz/documents/62353418/171347265/270248-22data020923.csv)
- [kanalizace](https://www.czso.cz/documents/62353418/200583836/sldb2021_obydomy_druh_odpad.csv)
- [věk podle pohlaví](https://www.czso.cz/documents/62353418/182807150/sldb2021_prumvek_pohlavi.csv)
- [domácnosti s kuchyní a kuchyňským koutem](https://www.czso.cz/documents/62353418/192056095/sldb2021_byty_kuchyne.csv)
- [obyvatelé podle věku a pohlaví](https://www.czso.cz/documents/62353418/183907242/sldb2021_vek5_pohlavi.csv)

- [mapa lesů 2018](https://geoportal.gov.cz/atom/hrl/TCD_2018_010m_CR.tif)
- [mapa vodních toků 2018](https://geoportal.gov.cz/atom/hrl/WAW_2018_010m_CR.tif)
- [mapa luk 2018](https://geoportal.gov.cz/atom/hrl/GRA_2018_010m_CR.tif)
- [mapa nepropustného povrchu 2018](https://geoportal.gov.cz/atom/hrl/IBU_2018_010m_CR.tif)

### Aplikace
**Aplikace se nachází na adrese [plajta.vesek.eu](https://plajta.vesek.eu)**

## TODO:
- [ ] najet na production server
- [ ] spravit geolokaci
- [ ] dodělat nuke simulaci
