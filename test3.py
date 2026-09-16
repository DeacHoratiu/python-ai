class Vehicul():
    def __init__(self,tip,serie,viteza_maxima,marca,unitati,capacitate_cilindrica,culoare):
        self.tip= tip
        self.serie = serie
        self.viteza_maxima = viteza_maxima
        self.unitati = unitati
        self.marca = marca
        self.capacitate_cilindrica = capacitate_cilindrica
        self.culoare = culoare

    def __str__(self):
        return f"{self.tip} {self.marca}, serie {self.serie}, culoare {self.culoare}"


autobuz = Vehicul("autobuz", "CX1A", 110, "Mercedes", 13, 4998, "Alb")
masina = Vehicul("masina", "AB12", 180, "Dacia", 5, 1598, "Rosu")
motocicleta = Vehicul("motocicleta", "MOTO1", 220, "Yamaha", 1, 998, "Negru")

print(autobuz)
print(masina)
print(motocicleta)