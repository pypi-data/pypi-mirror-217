class TrieSolmu:

    """Trie-luokan tietorakenteen yksittäinen solmu."""

    def __init__(self, lapset, päätesolmu, arvo, arvojakauma=None):
        self.lapset = lapset
        self.päätesolmu = päätesolmu
        self.arvo = arvo
        self.arvojakauma = arvojakauma

    def __repr__(self):
        return f"TrieSolmu({self.lapset.__repr__()}, {self.päätesolmu.__repr__()}, {self.arvo.__repr__()}, {self.arvojakauma})"

class Trie:

    """Trie-tietorakenne, poikkeavuutena käänteinen järjestys (tukee prefiksikyselyjen sijaan suffiksikyselyjä)."""
    
    def __init__(self, juuri=None, koko=1):
        if juuri != None:
            self.juuri = juuri
        else:
            self.juuri = TrieSolmu({}, False, "")
        self.koko = koko
    
    def lisää(self, alkio, arvo, on_jakauma=False):
        käänteinen = alkio[::-1]
        nykyinen = self.juuri
        for i in range(len(alkio)):
            merkki = käänteinen[i]
            if merkki in nykyinen.lapset.keys():
                nykyinen = nykyinen.lapset[merkki]
            else:
                nykyinen.lapset[merkki] = TrieSolmu({}, False, käänteinen[:i+1])
                nykyinen = nykyinen.lapset[merkki]
                self.koko += 1
        if on_jakauma:
            nykyinen.arvojakauma = arvo
        else:
            if nykyinen.arvojakauma == None:
                nykyinen.arvojakauma = {}
            if not arvo in nykyinen.arvojakauma.keys():
                nykyinen.arvojakauma[arvo] = 0
            nykyinen.arvojakauma[arvo] += 1
        nykyinen.päätesolmu = True

    def laske_arvojakaumat(self):
        self.laske_arvojakaumat_kohdassa(self.juuri)
    
    def laske_arvojakaumat_kohdassa(self, solmu):
        if solmu.arvojakauma == None:
            solmu.arvojakauma = {}
        for lapsi in solmu.lapset.values():
            self.laske_arvojakaumat_kohdassa(lapsi)
        for lapsi in solmu.lapset.values():
            for avain in lapsi.arvojakauma.keys():
                if not avain in solmu.arvojakauma:
                    solmu.arvojakauma[avain] = 0
                solmu.arvojakauma[avain] += lapsi.arvojakauma[avain]
        
    def pisimmän_yhteisen_suffiksin_solmu(self, alkio):

        """Palauttaa parin, jonka ensimmäinen alkio on paras triestä löytyvä päätesolmu ja toinen on paras solmu yleisesti.
           Esimerkiksi jos trie kuvaa joukon {taskurapu, rapu} ja sieltä haetaan alkiolla laskurapu, palauttaa metodi parin
           (a, b), jossa a on merkkijonoa rapu vastaava solmu ja b on merkkijonoa askurapu vastaava solmu."""

        käänteinen = alkio[::-1]
        nykyinen = self.juuri
        paras = None
        for merkki in käänteinen:
            if merkki in nykyinen.lapset.keys():
                nykyinen = nykyinen.lapset[merkki]
            else:
                break
            if nykyinen.päätesolmu:
                paras = nykyinen
        return (paras, nykyinen)
    
    def etsi_pisimmällä_yhteisellä_suffiksilla(self, alkio, kokonainen=True):
        
        paras, nykyinen = self.pisimmän_yhteisen_suffiksin_solmu(alkio)
        
        if kokonainen:
            
            # Jos ei löydy kokonaista sanaa, palautetaan None
            
            if paras == None:
                return None
            else:
                return paras.arvo[::-1]
        else:
            
            # Seurataaan jotakin haaraa loppuun saakka
        
            while not nykyinen.päätesolmu:
                nykyinen = nykyinen.lapset[list(nykyinen.lapset.keys())[0]]
            return nykyinen.arvo[::-1]
    
    def arvojakauma_pisimmälle_yhteiselle_suffiksille(self, arvo):
        _, nykyinen = self.pisimmän_yhteisen_suffiksin_solmu(arvo)
        return nykyinen.arvojakauma

    def __repr__(self):
        return f"Trie({self.juuri}, {self.koko})"
