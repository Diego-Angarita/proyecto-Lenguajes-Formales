"""
Cálculo de Conjuntos PRIMERO y SIGUIENTE para Análisis Sintáctico

Este módulo implementa los algoritmos fundamentales para calcular:
- Conjuntos PRIMERO: Terminales que pueden aparecer al inicio de derivaciones
- Conjuntos SIGUIENTE: Terminales que pueden aparecer después de un no terminal

Estos conjuntos son esenciales para:
- Construcción de tablas de análisis LL(1)
- Resolución de conflictos en analizadores SLR(1)
- Determinación de la aplicabilidad de reglas de producción

Basado en los algoritmos estándar de:
Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"
"""

class First_Follow:
    """
    Calculadora de Conjuntos PRIMERO y SIGUIENTE
    
    Implementa los algoritmos iterativos para calcular los conjuntos fundamentales
    necesarios en el análisis sintáctico predictivo y LR.
    
    Atributos:
        gramatica: Referencia a la gramática libre de contexto
        primero: Mapeo de no terminales a sus conjuntos PRIMERO
        siguiente: Mapeo de no terminales a sus conjuntos SIGUIENTE
    """
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.primero = {}    # Dict[str, Set[str]]: NoTerminal -> Conjunto PRIMERO
        self.siguiente = {}  # Dict[str, Set[str]]: NoTerminal -> Conjunto SIGUIENTE
        
    def calcular_primero(self):
        """
        Calcular conjuntos PRIMERO para todos los no terminales
        PRIMERO(X) = conjunto de terminales que pueden aparecer al inicio de cadenas derivadas desde X
        """
        # Inicializar conjuntos PRIMERO
        for nt in self.gramatica.no_terminales:
            self.primero[nt] = set()
        
        # Calcular iterativamente conjuntos PRIMERO hasta que no haya cambios
        cambio = True
        while cambio:
            cambio = False
            
            for nt in self.gramatica.no_terminales:
                for produccion in self.gramatica.obtener_producciones(nt):
                    tamaño_anterior = len(self.primero[nt])
                    
                    # Calcular PRIMERO de esta producción
                    primero_prod = self._primero_de_cadena(produccion)
                    self.primero[nt].update(primero_prod)
                    
                    if len(self.primero[nt]) > tamaño_anterior:
                        cambio = True
        
        return self.primero
    
    def _primero_de_cadena(self, cadena):
        """
        Calcular PRIMERO de una cadena (secuencia de símbolos)
        """
        if len(cadena) == 0:
            return {'e'}
        
        resultado = set()
        
        for i, simbolo in enumerate(cadena):
            if simbolo == 'e':
                # Cadena vacía
                resultado.add('e')
                break
            elif simbolo in self.gramatica.terminales:
                # Símbolo terminal
                resultado.add(simbolo)
                break
            elif simbolo in self.gramatica.no_terminales:
                # Símbolo no terminal
                primero_simbolo = self.primero.get(simbolo, set())
                resultado.update(primero_simbolo - {'e'})
                
                # Si epsilon está en PRIMERO(simbolo), continuar al siguiente símbolo
                if 'e' not in primero_simbolo:
                    break
                
                # Si estamos en el último símbolo y puede derivar epsilon
                if i == len(cadena) - 1:
                    resultado.add('e')
        
        return resultado
    
    def calcular_siguiente(self):
        """
        Calcular conjuntos SIGUIENTE para todos los no terminales
        SIGUIENTE(A) = conjunto de terminales que pueden aparecer inmediatamente después de A
        """
        # Inicializar conjuntos SIGUIENTE
        for nt in self.gramatica.no_terminales:
            self.siguiente[nt] = set()
        
        # Regla 1: Agregar $ a SIGUIENTE del símbolo inicial
        if self.gramatica.simbolo_inicial not in self.siguiente:
            self.siguiente[self.gramatica.simbolo_inicial] = set()
        self.siguiente[self.gramatica.simbolo_inicial].add('$')
        
        # Calcular iterativamente conjuntos SIGUIENTE hasta que no haya cambios
        cambio = True
        while cambio:
            cambio = False
            
            for nt in self.gramatica.no_terminales:
                for produccion in self.gramatica.obtener_producciones(nt):
                    # Para cada símbolo en la producción
                    for i, simbolo in enumerate(produccion):
                        if simbolo in self.gramatica.no_terminales:
                            tamaño_anterior = len(self.siguiente[simbolo])
                            
                            # Obtener resto de producción después de este símbolo
                            beta = produccion[i+1:]
                            
                            # Regla 2: Agregar PRIMERO(beta) - {epsilon} a SIGUIENTE(simbolo)
                            primero_beta = self._primero_de_cadena(beta)
                            self.siguiente[simbolo].update(primero_beta - {'e'})
                            
                            # Regla 3: Si epsilon en PRIMERO(beta), agregar SIGUIENTE(A) a SIGUIENTE(simbolo)
                            if 'e' in primero_beta or len(beta) == 0:
                                self.siguiente[simbolo].update(self.siguiente[nt])
                            
                            if len(self.siguiente[simbolo]) > tamaño_anterior:
                                cambio = True
        
        return self.siguiente
    
    def imprimir_conjuntos(self):
        """Imprimir conjuntos PRIMERO y SIGUIENTE para depuración"""
        print("\n=== Conjuntos PRIMERO ===")
        for nt in sorted(self.primero.keys()):
            print(f"PRIMERO({nt}) = {{{', '.join(sorted(self.primero[nt]))}}}")
        
        print("\n=== Conjuntos SIGUIENTE ===")
        for nt in sorted(self.siguiente.keys()):
            print(f"SIGUIENTE({nt}) = {{{', '.join(sorted(self.siguiente[nt]))}}}")