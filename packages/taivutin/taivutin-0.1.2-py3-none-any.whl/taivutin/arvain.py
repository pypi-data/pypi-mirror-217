from .trie import Trie

class Arvain():

    """Arvain, joka pyrkii päättelemään nominien taivutustietoa."""

    def __init__(self, syöte_sanat, syöte_nimet={}):

        """
        Rakentaa uuden Arvain-olion hakurakenteesta sanoja ja valinnaisesti hakurakenteesta nimiä. Sanat taas hakurakenteita, joilla on seuraava rakenne:
        
        ```python
        syöte_sanat["risti"] = {
          "tn": "5", # Taivutusnumero merkkijonona, valinnainen; kaikki yli taivutusluokan 51 hylätään (ei nomineja)
          "av": "-", # Astevaihteluluokka tai viiva, valinnainen
        }
        ```
        
        Nimet taas ovat ovat hakurakenteita, joilla on seuraava rakenne:

        ```python
        syöte_nimet["Päivyt"] = {
          "tn": "43", # Taivutusnumero merkkijonona, pakollinen; kaikki yli taivutusluokan 51 hylätään (ei nomineja)
          "av": "-", # Astevaihteluluokka tai viiva, pakollinen
          "sointu": "ETU" # Vokaalisointuluokka merkkijonona, joko "ETU" tai "TAKA", pakollinen
        }
        ```
        """

        self.sanat = {}
        self.nimet = syöte_nimet
        self.trie = Trie()
        self.astetrie = Trie()
        
        # Sanaston syönti
        
        for sana in syöte_sanat.keys():
            if sana.endswith("-"):
                continue
            if "tn" in syöte_sanat[sana].keys() and syöte_sanat[sana]["tn"].isnumeric() and int(syöte_sanat[sana]["tn"]) > 51:
                continue
            self.sanat[sana] = syöte_sanat[sana]
            if "tn" in syöte_sanat[sana].keys():
                self.trie.lisää(sana, syöte_sanat[sana]["tn"])
            if "av" in syöte_sanat[sana].keys():
                self.astetrie.lisää(sana, syöte_sanat[sana]["av"])

        # Hieman tökerö kikka, joka merkitsee muutaman yleisen päätteen

        self.sanat["inen"] = {"tn":"38"}
        self.sanat["isuus"] = {"tn":"40"}
        self.trie.lisää("inen", "38")
        self.trie.lisää("isuus", "40")

        # Tehdään triejen esilaskenta valmiiksi

        self.trie.laske_arvojakaumat()
        self.astetrie.laske_arvojakaumat()

    def normalisoi_konsonanttiloppuiset(self, sana, taivutus):

        """
        Taivutusluokalla 5 (risti / golf) on kaksi eri käytöstä. Käytös riippuu siitä, loppuuko sana vokaaliin vai konsonanttiin. `normalisoi_konsonanttiloppuiset` muuntaa taivutuksen 5 taivutukseksi 5b, jos sana on konsonanttiloppuinen, eikä vaikuta liikaa monikolta.
        """

        # Selkeä 5b-tapaus

        if taivutus == "5" and sana[-1] in "qwrpsdfghjklzxcvbnm":
           return "5b"

        # Epätoivoinen yritys havaita monikolliset sanat

        elif taivutus == "5" and sana[-1] == "t" and sana[-2] in "qwrtpsdfghjklzxcvbnm":
           return "5b"

        # Ei tarvitse tehdä mitään

        return taivutus
   
    def arvaa(self, sana, **kwargs):

        """
        Arvaa sanan taivutusluokan. Hyväksyy joukon käytöstä hieman muokkaavia nimettyjä parametreja.
        * `tilastollisesti` (totuusarvo, oletusarvoisesti tosi): Jos tosi, katsotaan kaikki sellaiset sanat, joilla on yhtä pitkä yhteinen suffiksi haettavan kanssa kuin sanalla, jolla on pisin yhteinen suffiksi haettavan kanssa. Näillä sanoilla esiintyvistä taivutusmuodoista valitaan todennäköisin. Esimerkiksi jos haettava sana on teeri (26) ja löydetään sanat ukkoteeri (26), sihteeri (6) ja valtiosihteeri (6), niin tilastollinen haku valitsee yleisimmän taivutusluokan (26, esiintyy kahdesti). Jos `tilastollisesti` on epätosi, valitaan ennustamattomasti (vaikkei välttämättä umpimähkään) jokin sanoista, esimerkiksi sihteeri (6) ja palautetaan sen taivutusluokka. Jos löydetään lupaava osuma (eli sanakirjassa olisi teeri (6) tai jos haettaessa sanaa ilmapallo (1) löydetään sen suffiksi pallo (1)), valitaan sen mukainen taivutusluokka riippumatta siitä, minkä arvon `tilastollisesti` saa.
        * `nimi` (totuusarvo, oletusarvoisesti tosi): Jos tosi, tarkistetaan ensin nimihakurakenne suoran osuman varalta. Jos epätosi, ei tarkasteta nimihakurakennetta. Tämä on hyödyllistä esimerkiksi luontonimien tapauksessa, jossa voidaan haluta erisnimimäinen (Meri - Merin) tai yleissanamainen (Meri - Meren) taivutus.
        """

        kwargs = {"tilastollisesti": True, "nimi": True} | kwargs

        # Jos ei erikseen kielletty nimeä, katsotaan nimiosumat

        if kwargs["nimi"]:
            loppuosa = sana.split("-")[-1].split(" ")[-1]
            if loppuosa in self.nimet.keys():
                return self.normalisoi_konsonanttiloppuiset(loppuosa, self.nimet[loppuosa]["tn"])

        taivutus = None
        if sana in self.sanat.keys() and "tn" in self.sanat[sana].keys():
            taivutus = self.sanat[sana]["tn"]
        else:
            ehdokas = self.trie.etsi_pisimmällä_yhteisellä_suffiksilla(sana)
            if ehdokas == None and not kwargs["tilastollisesti"]:
                ehdokas = self.trie.etsi_pisimmällä_yhteisellä_suffiksilla(sana, False)
            if ehdokas != None:
                taivutus = self.sanat[ehdokas]["tn"]
            else:
                jakauma = self.trie.arvojakauma_pisimmälle_yhteiselle_suffiksille(sana)
                paras = 0
                paras_luokka = None
                for key in jakauma.keys():
                    if jakauma[key] > paras:
                        paras_luokka = key
                        paras = jakauma[key]
                        
                taivutus = paras_luokka
    
        return self.normalisoi_konsonanttiloppuiset(sana, taivutus)
    
    def sointuluokka_yksinkertaiselle(self, sana):

        """
        Päättelee vokaalisointuluokan sanalle sillä oletuksella, ettei se ole yhdyssana. Tieto on tarpeen, jos sijapäätteeseen tulee a tai ä: talossa / esimerkissä.
        Tämän se tekee etsimällä sanan viimeisen etu- (äöy) ja takavokaalin (aouå). Jos sanasta löytyy takavokaali viimeisimmän etuvokaalin jälkeen (tai löytyy ylipäänsä, sikäli kuin etuvokaaleja ei ole), on sana takavokaalinen (talossa).
        Muussa tapauksessa sana on etuvokaalinen (esimerkissä).
        """

        viimeinen_etu = -1
        viimeinen_taka = -1
        pienellä = sana.lower()
        for i in range(len(sana)):
            if pienellä[i] in "äöy":
                viimeinen_etu = i
            elif pienellä[i] in "aouå":
                viimeinen_taka = i
        if viimeinen_taka > viimeinen_etu:
            return "TAKA"
        else:
            return "ETU"
    
    def arvaa_sointuluokka(self, sana, **kwargs):

        """
        Päättelee vokaalisointuluokan sanalle yleisessä tapauksessa. Hyväksyy joukon metodin käytöstä muokkaavia nimettyjä parametreja.
        * `hiljaa` (totuusarvo, oletusarvoisesti tosi): jos epätosi, tulostaa virheenkorjausviestejä siitä, miten tehtyyn arvaukseen päädyttiin.
        * `nimi` (totuusarvo, oletusarvoisesti tosi): tarkistaa aluksi nimisanakirjan suoran tai yhdyssanaosuman varalta. Esimerkiksi moni englantilaisperäinen y-kirjaimeen päättyvä nimi ääntyy i-äänteeseen päättyvänä ja seuraakin takavokaalista vokaalisointua.

        Nimisanakirjan tarkistamisen (tai tarkistamatta jättämisen) jälkeen etsitään mahdollista suffiksisanaa: jos haetaan sanaa maantie (etuvokaalisointu), on hyödyllistä havaita sen olevan yhdyssana, joka loppuu sanaan tie (etuvokaalisointu). Jos kyseessä ei olisi yhdyssana, sen alkuosassa oleva pitkä a-äänne tekisi siitä takavokaalisen, siis maantie - maantieta eikä maantietä. Viimeiseksi päätellylle komponentille (joka saattaa olla koko sana, mikäli kyseessä ei ole yhdyssana) arvataan sitten sointuluokka metodilla `sointuluokka_yksinkertaiselle`.
        """

        kwargs = {"hiljaa": True, "nimi": True} | kwargs

        # Jos ei erikseen kielletty nimeä, katsotaan nimiosumat

        if kwargs["nimi"]:
            loppuosa = sana.split("-")[-1].split(" ")[-1]
            if loppuosa in self.nimet.keys():
                return self.nimet[loppuosa]["sointu"]

        ehdokas = self.trie.etsi_pisimmällä_yhteisellä_suffiksilla(sana[1:], True)
        if ehdokas != None:
            if not kwargs["hiljaa"]:
                print(f"Sanan suffiksisana '{ehdokas}' löytyy sanakirjasta")
            return self.sointuluokka_yksinkertaiselle(ehdokas)
        else:
            if not kwargs["hiljaa"]:
                print(f"Sanaan liittyvää tietoa ei löydy sanakirjasta")
            return self.sointuluokka_yksinkertaiselle(sana)
    
    def arvaa_astevaihteluluokka(self, sana, **kwargs):

        kwargs = {"tilastollisesti": True, "hiljaa": True} | kwargs

        # Jos ei erikseen kielletty nimeä, katsotaan nimiosumat

        if not "nimi" in kwargs.keys() or kwargs["nimi"]:
            loppuosa = sana.split("-")[-1].split(" ")[-1]
            if loppuosa in self.nimet.keys():
                return self.nimet[loppuosa]["av"]

        taivutus = None
        if sana in self.sanat.keys() and "av" in self.sanat[sana].keys():
            if not kwargs["hiljaa"]:
                print(f"{sana}: sukkana")
            taivutus = self.sanat[sana]["av"]
        else:
            ehdokas = self.astetrie.etsi_pisimmällä_yhteisellä_suffiksilla(sana)
            if ehdokas == None and not kwargs["tilastollisesti"]:
                if not kwargs["hiljaa"]:
                    print(f"{sana}: yritetään suffiksisanalla")
                ehdokas = self.astetrie.etsi_pisimmällä_yhteisellä_suffiksilla(sana, False)
            if ehdokas != None:
                if not kwargs["hiljaa"]:
                    print(f"{sana}: yritetään ei-tilastollisella suffiksilla")
                taivutus = self.sanat[ehdokas]["av"]
            else:
                if not kwargs["hiljaa"]:
                    print(f"{sana}: yritetään tilastollisella suffiksilla")
                jakauma = self.astetrie.arvojakauma_pisimmälle_yhteiselle_suffiksille(sana)
                paras = 0
                paras_luokka = None
                for key in jakauma.keys():
                    if jakauma[key] > paras:
                        paras_luokka = key
                        paras = jakauma[key]
                        
                taivutus = paras_luokka
        return taivutus
    
    def arvaa_viimeinen_komponentti(self, sana):
        ehdokas = self.astetrie.etsi_pisimmällä_yhteisellä_suffiksilla(sana[1:], True)
        if ehdokas == None:
            return sana
        else:
            return ehdokas
