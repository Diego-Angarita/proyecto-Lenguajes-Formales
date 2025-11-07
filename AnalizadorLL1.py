"""
Implementación del Analizador Sintáctico LL(1)

Este módulo contiene la implementación de un analizador sintáctico predictivo
descendente (Top-Down) del tipo LL(1). Este tipo de analizador utiliza una
tabla de análisis para decidir qué producción aplicar basándose en el símbolo
actual de la entrada y el no terminal en el tope de la pila.
"""

class AnalizadorLL1:
    """
    Implementa un analizador LL(1) para una gramática dada.

    El analizador construye una tabla de análisis y la utiliza para parsear
    cadenas de entrada. También determina si la gramática es LL(1), es decir,
    si está libre de conflictos que impidan el análisis predictivo.

    Atributos:
        gramatica: La gramática a analizar.
        first_follow: Objeto con los conjuntos FIRST y FOLLOW.
        tabla_analisis (dict): La tabla de análisis LL(1).
        es_ll1 (bool): True si la gramatica es LL(1), False si no.
    """
    def __init__(self, gramatica, first_follow):
        """Inicializa el analizador con la gramática y los conjuntos FIRST/FOLLOW."""
        self.gramatica = gramatica
        self.first_follow = first_follow
        self.tabla_analisis = {}
        self.es_ll1 = False

    def construir_tabla_analisis(self):
        """
        Construye la tabla de análisis LL(1).

        El algoritmo se basa en dos reglas para llenar la tabla M[A, a]:
        1. Para cada producción A -> α, si un terminal 'a' está in FIRST(α),
           se añade A -> α a M[A, a].
        2. Si 'e' (epsilon) está en FIRST(α), para cada terminal 'b' en
           FOLLOW(A), se añade A -> α a M[A, b].

        Si alguna celda de la tabla contiene más de una producción, la gramática
        no es LL(1).

        Returns:
            bool: True si la tabla se construyó sin conflictos, False si no.
        """
        self.tabla_analisis = {}
        conflictos = []

        for nt in self.gramatica.no_terminales:
            for produccion in self.gramatica.obtener_producciones(nt):
                first_prod = self.first_follow._first_de_cadena(produccion)

                # Aplica la Regla 1
                for terminal in first_prod:
                    if terminal != 'e':
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            conflictos.append(clave)
                        else:
                            self.tabla_analisis[clave] = produccion
                
                # Aplica la Regla 2
                if 'e' in first_prod:
                    for terminal in self.first_follow.follow[nt]:
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            conflictos.append(clave)
                        else:
                            self.tabla_analisis[clave] = produccion
        
        self.es_ll1 = not conflictos
        return self.es_ll1

    def analizar(self, cadena_entrada):
        """
        Analiza una cadena de entrada utilizando el analizador LL(1).

        El proceso simula una derivación descendente utilizando una pila:
        - Se compara el tope de la pila con el símbolo de entrada actual.
        - Si coinciden (y son terminales), ambos se consumen.
        - Si el tope es un no terminal, se consulta la tabla de análisis para
          reemplazarlo con la producción correspondiente.
        - Si no hay entrada en la tabla, la cadena es rechazada.

        Args:
            cadena_entrada (str): La cadena a analizar.

        Returns:
            bool: True si la cadena es aceptada, False en caso contrario.
        """
        if not self.es_ll1:
            return False

        cadena_entrada += '$'
        pila = ['$', self.gramatica.simbolo_inicial]
        indice_entrada = 0

        while pila:
            tope = pila[-1]
            entrada_actual = cadena_entrada[indice_entrada]

            if tope in self.gramatica.terminales or tope == '$':
                if tope == entrada_actual:
                    pila.pop()
                    indice_entrada += 1
                else:
                    return False  # Error: terminal no coincide.
            
            elif tope in self.gramatica.no_terminales:
                clave = (tope, entrada_actual)
                if clave in self.tabla_analisis:
                    pila.pop()
                    produccion = self.tabla_analisis[clave]
                    
                    # Apila la producción en orden inverso.
                    if produccion != ['e']:
                        for simbolo in reversed(produccion):
                            pila.append(simbolo)
                else:
                    return False  # Error: no hay producción en la tabla.
            else:
                return False  # Símbolo inesperado en la pila.
        
        # La cadena es aceptada si la pila está vacía y se ha consumido toda la entrada.
        return indice_entrada == len(cadena_entrada)

    def imprimir_tabla(self):
        """Imprime la tabla de análisis LL(1) en un formato legible."""
        print("\n=== Tabla de Análisis LL(1) ===")
        terminales = sorted(list(self.gramatica.terminales))
        
        header = f"{'NT':<10}" + "".join(f"{t:<15}" for t in terminales)
        print(header)
        print("-" * len(header))

        for nt in sorted(self.gramatica.no_terminales):
            fila = f"{nt:<10}"
            for t in terminales:
                clave = (nt, t)
                if clave in self.tabla_analisis:
                    prod = "".join(self.tabla_analisis[clave])
                    fila += f"{nt}->{prod:<12}"
                else:
                    fila += f"{'---':<15}"
            print(fila)