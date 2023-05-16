class ZahlenDruckerMitVariablen:
    def DruckeZahlenVonNullAufsteigendOderAbsteigend(self, zahlBis):
        if zahlBis >= 0:
            k = 1
        else:
            k = -1

        for zahl in range(0, zahlBis + k, k):
            print(zahl)

drucker = ZahlenDruckerMitVariablen()
drucker.DruckeZahlenVonNullAufsteigendOderAbsteigend(10)
drucker.DruckeZahlenVonNullAufsteigendOderAbsteigend(-10)
drucker.DruckeZahlenVonNullAufsteigendOderAbsteigend(1)
drucker.DruckeZahlenVonNullAufsteigendOderAbsteigend(0)
