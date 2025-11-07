"""
Cálculo de Conjuntos PRIMERO y SIGUIENTE

Este módulo implementa los algoritmos para calcular los conjuntos PRIMERO y
SIGUIENTE de una gramática libre de contexto. Estos conjuntos son un pilar
fundamental en la construcción de analizadores sintácticos predictivos (como LL(1))
y ascendentes (como SLR(1)).

- PRIMERO(X): Conjunto de terminales con los que puede comenzar una cadena derivada de X.
- SIGUIENTE(A): Conjunto de terminales que pueden aparecer inmediatamente después de A.
"""

class First_Follow:
    """
    Calcula y almacena los conjuntos PRIMERO y SIGUIENTE para una gramática dada.

    Esta clase toma una gramática como entrada y aplica algoritmos iterativos
    para derivar los conjuntos. Los resultados se almacenan internamente y pueden
    ser utilizados por los analizadores sintácticos.

    Atributos:
        gramatica: La gramática libre de contexto a analizar.
        primero (dict): Diccionario que mapea cada no terminal a su conjunto PRIMERO.
        siguiente (dict): Diccionario que mapea cada no terminal a su conjunto SIGUIENTE.
    """
    def __init__(self, gramatica):
        """Inicializa la calculadora con una gramática."""
        self.gramatica = gramatica
        self.primero = {}
        self.siguiente = {}

    def calcular_primero(self):
        """
        Calcula los conjuntos PRIMERO para todos los no terminales de la gramática.

        El algoritmo es iterativo: se repite sobre las producciones hasta que los
        conjuntos PRIMERO de todos los no terminales dejen de cambiar. Esto asegura
        que se hayan propagado todos los símbolos posibles.

        Returns:
            dict: El diccionario de conjuntos PRIMERO.
        """
        # Inicializa un conjunto vacío para cada no terminal.
        for nt in self.gramatica.no_terminales:
            self.primero[nt] = set()

        # Itera hasta que no se puedan agregar más símbolos a ningún conjunto PRIMERO.
        cambio = True
        while cambio:
            cambio = False
            for nt in self.gramatica.no_terminales:
                for produccion in self.gramatica.obtener_producciones(nt):
                    tamaño_anterior = len(self.primero[nt])
                    
                    # Calcula el conjunto PRIMERO de la producción actual.
                    primero_prod = self._primero_de_cadena(produccion)
                    self.primero[nt].update(primero_prod)

                    # Si el conjunto ha crecido, se necesita otra iteración.
                    if len(self.primero[nt]) > tamaño_anterior:
                        cambio = True
        
        return self.primero

    def _primero_de_cadena(self, cadena):
        """
        Calcula el conjunto PRIMERO para una secuencia de símbolos (una producción).

        Reglas aplicadas:
        1. Si el primer símbolo es un terminal, es el único miembro del conjunto PRIMERO.
        2. Si es un no terminal, su conjunto PRIMERO se añade al resultado.
        3. Si un no terminal puede derivar en epsilon ('e'), se considera el
           siguiente símbolo en la cadena.

        Args:
            cadena (list[str]): La secuencia de símbolos.

        Returns:
            set: El conjunto PRIMERO de la cadena.
        """
        if not cadena or cadena == ['e']:
            return {'e'}

        resultado = set()
        for simbolo in cadena:
            if simbolo in self.gramatica.terminales:
                resultado.add(simbolo)
                return resultado  # Termina al encontrar el primer terminal.
            
            elif simbolo in self.gramatica.no_terminales:
                primero_simbolo = self.primero.get(simbolo, set())
                resultado.update(primero_simbolo - {'e'})
                
                # Si el no terminal no deriva en epsilon, no se puede seguir.
                if 'e' not in primero_simbolo:
                    return resultado
        
        # Si todos los símbolos de la cadena pueden derivar en epsilon, se añade epsilon.
        resultado.add('e')
        return resultado

    def calcular_siguiente(self):
        """
        Calcula los conjuntos SIGUIENTE para todos los no terminales.

        Este algoritmo también es iterativo y se basa en tres reglas principales:
        1. SIGUIENTE(SímboloInicial) siempre contiene '.
        2. Para una producción A -> αBβ, PRIMERO(β) (excepto 'e') está en SIGUIENTE(B).
        3. Si β puede derivar en 'e', entonces SIGUIENTE(A) está en SIGUIENTE(B).

        Returns:
            dict: El diccionario de conjuntos SIGUIENTE.
        """
        # Inicializa los conjuntos y aplica la Regla 1.
        for nt in self.gramatica.no_terminales:
            self.siguiente[nt] = set()
        self.siguiente[self.gramatica.simbolo_inicial].add('$')

        # Itera hasta la convergencia de los conjuntos.
        cambio = True
        while cambio:
            cambio = False
            for nt in self.gramatica.no_terminales:
                for produccion in self.gramatica.obtener_producciones(nt):
                    for i, simbolo in enumerate(produccion):
                        if simbolo in self.gramatica.no_terminales:
                            tamaño_anterior = len(self.siguiente[simbolo])
                            
                            # Beta es la secuencia de símbolos después del no terminal actual.
                            beta = produccion[i+1:]
                            
                            # Aplica la Regla 2.
                            primero_beta = self._primero_de_cadena(beta)
                            self.siguiente[simbolo].update(primero_beta - {'e'})
                            
                            # Aplica la Regla 3.
                            if 'e' in primero_beta or not beta:
                                self.siguiente[simbolo].update(self.siguiente[nt])
                            
                            if len(self.siguiente[simbolo]) > tamaño_anterior:
                                cambio = True
        
        return self.siguiente

    def imprimir_conjuntos(self):
        """Imprime los conjuntos PRIMERO y SIGUIENTE de forma legible."""
        print("\n=== Conjuntos PRIMERO ===")
        for nt in sorted(self.primero.keys()):
            print(f"PRIMERO({nt}) = {{{', '.join(sorted(self.primero[nt]))}}}")
        
        print("\n=== Conjuntos SIGUIENTE ===")
        for nt in sorted(self.siguiente.keys()):
            print(f"SIGUIENTE({nt}) = {{{', '.join(sorted(self.siguiente[nt]))}}}")