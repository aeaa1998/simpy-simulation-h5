
class Utils:
    def intInput(self, text) -> int:
        bool = True
        while (bool):
            value = input(text + "\n")
            try:
                value = int(value)
                return value
            except:
                print("Ingrese un valor valido")


    def intInputMin(self, text, min: int) -> int:
        bool = True
        while (bool):
            value = input(text + "\n")
            try:
                value = int(value)
                if value > min:
                    return value
                print("Ingrese un valor mayor a " + str(min))

            except:
                print("Ingrese un valor valido")


    def isPrime(self, integer) ->bool:
        half = int(integer / 2)
        for i in range(2, half):
            if integer % i == 0:
                return False
        return True

    def primeInput(self, text, min, max) ->int:
        number = 0
        boolPrime = False
        boolPositive = False
        ranges = False
        while not boolPrime or not boolPositive or not ranges:
            print("Ingrese un numero primo En el rango de " + str(min) + " - " + str(max))

            number = self.intInput(text)
            boolPrime = self.isPrime(number)
            ranges = number < min or number > max
            boolPositive = number > 0
            ranges = number >= min and number <= max
            if not boolPrime:
                print("Ingrese un numero primo.")
            elif not boolPositive:
                print("Ingrese un numero positivo.")
            elif not ranges:
                print("Ingrese un numero en el rango adecuado")
        return number


    def inverseMod(slef, number, modN) -> int:
        for x in range(1, modN):
            if (number * x) % modN == 1:
                return x
        return 0

    def mcd(self, numberOne, numberTwo) -> int:
        maxNumber = max(numberOne, numberTwo)
        minNumber = min(numberOne, numberTwo)

        return self.bezaut(maxNumber, minNumber)

    def bezaut(self, max, min) -> int:
            if min == 0:
                return max
            else:
                return self.bezaut(min, max % min)


    def coprimes(self, ph) -> list:
        list = []
        # Agrega los coprimos
        if ph <= 0:
            return []
        for x in range(2, ph):
            if self.mcd(ph, x) == 1:
                list.append(x)
        #Elimina los inversos
        for x in list:
            if x%ph ==1:
                list.remove(x)
        return list

    def chooseIntList(self, list) -> int:
        while True:
            counter = 0
            print("Escoja una de las siguientes opciones.")
            for item in list:
                counter += 1
                print(str(counter) + ") " + str(item))
            c = input()
            val = 0
            try:
                val = int(c)
                if val in list:
                    return val
                print("Escoja una opcion valida.\n")
            except:
                print("Ingrese un numero.")

    def chooseKey(self, list) -> int:
        while True:
            keyList = []
            print("Escoja el numero una de las siguientes opciones.")
            for key, item in enumerate(list):
                print(str(key+1) + ") " + str(item))
                keyList.append(key)
            c = input()
            val = 0
            try:
                val = int(c)
                if val-1 in keyList:
                    return val
                print("Escoja una opcion valida.\n")
            except:
                print("Ingrese un numero.")



