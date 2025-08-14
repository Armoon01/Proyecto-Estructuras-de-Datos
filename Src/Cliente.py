class Cliente:
    def __init__(self, id, nom, dir, tel, corr):
        self.ID = id
        self.nombre = nom
        self.direccion = dir
        self.telefono = tel
        self.Correo = corr
        self.Lista_ordenes = set()
        
    #def __repr__(self):
        #...
        
    def getId(self):
        return self.ID

    def setId(self, id):
        self.ID = id

    def getNom(self):
        return self.nombre

    def setNom(self, nom):
        self.nombre = nom

    def getDirec(self):
        return self.direccion

    def setDirec(self, direc):
        self.direccion = direc

    def getTele(self):
        return self.telefono

    def setTele(self, tel):
        self.telefono = tel

    def getCorr(self):
        return self.Correo

    def setCorr(self, corr):
        self.Correo = corr

    def getOrdenes(self):
        return self.Lista_ordenes

    #def setOrdenes(self, ordenes):
        #self.Lista_ordenes = ordenes