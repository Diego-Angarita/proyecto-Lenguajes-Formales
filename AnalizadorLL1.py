"""
AnalizadorLL1_Mejorado.py
==========================
Versión mejorada del AnalizadorLL1 que construye un árbol sintáctico
MEJORA: Usa estructura de datos de ÁRBOL
"""

from ArbolSintactico import NodoArbol, ArbolSintactico

class AnalizadorLL1:
    def __init__(self, gramatica, primero_siguiente):
        self.gramatica = gramatica
        self.primero_siguiente = primero_siguiente
        self.tabla_analisis = {}
        self.es_ll1 = False
        
    def construir_tabla_analisis(self):
        """Construir tabla de análisis LL(1) - igual que antes"""
        self.tabla_analisis = {}
        conflictos = []
        
        for nt in self.gramatica.no_terminales:
            for produccion in self.gramatica.obtener_producciones(nt):
                primero_prod = self.primero_siguiente._primero_de_cadena(produccion)
                
                for terminal in primero_prod:
                    if terminal != 'e':
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            conflictos.append(clave)
                            self.es_ll1 = False
                        else:
                            self.tabla_analisis[clave] = produccion
                
                if 'e' in primero_prod:
                    for terminal in self.primero_siguiente.siguiente[nt]:
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            conflictos.append(clave)
                            self.es_ll1 = False
                        else:
                            self.tabla_analisis[clave] = produccion
        
        if len(conflictos) == 0:
            self.es_ll1 = True
        
        return self.es_ll1
    
    def analizar_con_arbol(self, cadena_entrada):
        """
        NUEVA FUNCIONALIDAD: Analizar y construir árbol sintáctico
        Retorna (aceptado, arbol_sintactico)
        """
        if not self.es_ll1:
            return False, None
        
        cadena_entrada += '$'
        
        # Crear raíz del árbol
        raiz = NodoArbol(self.gramatica.simbolo_inicial, 'no_terminal')
        arbol = ArbolSintactico(raiz)
        
        # Pila ahora contiene tuplas (simbolo, nodo_arbol)
        pila = [('$', None), (self.gramatica.simbolo_inicial, raiz)]
        indice_entrada = 0
        
        while len(pila) > 0:
            simbolo_pila, nodo_actual = pila[-1]
            entrada_actual = cadena_entrada[indice_entrada] if indice_entrada < len(cadena_entrada) else '$'
            
            # Caso 1: Tope es un terminal
            if simbolo_pila in self.gramatica.terminales or simbolo_pila == '$':
                if simbolo_pila == entrada_actual:
                    pila.pop()
                    indice_entrada += 1
                else:
                    return False, None
            
            # Caso 2: Tope es un no terminal
            elif simbolo_pila in self.gramatica.no_terminales:
                clave = (simbolo_pila, entrada_actual)
                
                if clave in self.tabla_analisis:
                    pila.pop()
                    produccion = self.tabla_analisis[clave]
                    
                    # Crear nodos hijos en el árbol
                    if produccion != ['e']:
                        # Crear nodos para cada símbolo de la producción
                        nodos_hijos = []
                        for simbolo in produccion:
                            if simbolo in self.gramatica.terminales:
                                hijo = NodoArbol(simbolo, 'terminal')
                            else:
                                hijo = NodoArbol(simbolo, 'no_terminal')
                            nodos_hijos.append(hijo)
                            nodo_actual.agregar_hijo(hijo)
                        
                        # Apilar en orden inverso con sus nodos
                        for i in range(len(produccion) - 1, -1, -1):
                            pila.append((produccion[i], nodos_hijos[i]))
                    else:
                        # Producción epsilon - agregar nodo epsilon
                        hijo_epsilon = NodoArbol('e', 'terminal')
                        nodo_actual.agregar_hijo(hijo_epsilon)
                else:
                    return False, None
            else:
                return False, None
        
        return indice_entrada == len(cadena_entrada), arbol
    
    def analizar(self, cadena_entrada):
        aceptado, _ = self.analizar_con_arbol(cadena_entrada)
        return aceptado
    
    def imprimir_tabla(self):
        """Imprimir tabla de análisis para depuración"""
        print("\n=== Tabla de Análisis LL(1) ===")
        terminales = sorted(self.gramatica.terminales)
        
        print(f"{'NT':<5}", end='')
        for t in terminales:
            print(f"{t:<15}", end='')
        print()
        
        for nt in sorted(self.gramatica.no_terminales):
            print(f"{nt:<5}", end='')
            for t in terminales:
                clave = (nt, t)
                if clave in self.tabla_analisis:
                    prod = ''.join(self.tabla_analisis[clave])
                    print(f"{nt}->{prod:<12}", end='')
                else:
                    print(f"{'---':<15}", end='')
            print()