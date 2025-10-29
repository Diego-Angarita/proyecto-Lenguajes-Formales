"""
Implementación del Analizador LL(1)
Analizador sintáctico predictivo descendente (Top-Down)
"""

class AnalizadorLL1:
    def __init__(self, gramatica, primero_siguiente):
        self.gramatica = gramatica
        self.primero_siguiente = primero_siguiente
        self.tabla_analisis = {}
        self.es_ll1 = False
        
    def construir_tabla_analisis(self):
        """
        Construir tabla de análisis LL(1)
        Tabla[A, a] contiene producción A -> α si a está en PRIMERO(α)
        """
        self.tabla_analisis = {}
        conflictos = []
        
        for nt in self.gramatica.no_terminales:
            for produccion in self.gramatica.obtener_producciones(nt):
                # Calcular PRIMERO de la producción
                primero_prod = self.primero_siguiente._primero_de_cadena(produccion)
                
                # Para cada terminal en PRIMERO(produccion)
                for terminal in primero_prod:
                    if terminal != 'e':
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            # Conflicto detectado
                            conflictos.append(clave)
                            self.es_ll1 = False
                        else:
                            self.tabla_analisis[clave] = produccion
                
                # Si epsilon en PRIMERO(produccion), agregar entradas para SIGUIENTE(nt)
                if 'e' in primero_prod:
                    for terminal in self.primero_siguiente.siguiente[nt]:
                        clave = (nt, terminal)
                        if clave in self.tabla_analisis:
                            # Conflicto detectado
                            conflictos.append(clave)
                            self.es_ll1 = False
                        else:
                            self.tabla_analisis[clave] = produccion
        
        # Verificar si es LL(1) - sin conflictos
        if len(conflictos) == 0:
            self.es_ll1 = True
        
        return self.es_ll1
    
    def analizar(self, cadena_entrada):
        """
        Analizar una cadena de entrada usando analizador LL(1)
        Retorna True si la cadena es aceptada, False en caso contrario
        """
        if not self.es_ll1:
            return False
        
        # Agregar $ al final de la entrada
        cadena_entrada += '$'
        
        # Inicializar pila con $ y símbolo inicial
        pila = ['$', self.gramatica.simbolo_inicial]
        indice_entrada = 0
        
        while len(pila) > 0:
            tope = pila[-1]
            entrada_actual = cadena_entrada[indice_entrada] if indice_entrada < len(cadena_entrada) else '$'
            
            # Caso 1: Tope es un terminal
            if tope in self.gramatica.terminales or tope == '$':
                if tope == entrada_actual:
                    pila.pop()
                    indice_entrada += 1
                else:
                    return False  # No coinciden
            
            # Caso 2: Tope es un no terminal
            elif tope in self.gramatica.no_terminales:
                clave = (tope, entrada_actual)
                
                if clave in self.tabla_analisis:
                    pila.pop()
                    produccion = self.tabla_analisis[clave]
                    
                    # Apilar producción en orden inverso (saltar epsilon)
                    if produccion != ['e']:
                        for simbolo in reversed(produccion):
                            pila.append(simbolo)
                else:
                    return False  # No hay producción válida
            else:
                return False  # Símbolo inválido
        
        # Aceptar si se consumió toda la entrada
        return indice_entrada == len(cadena_entrada)
    
    def imprimir_tabla(self):
        """Imprimir tabla de análisis para depuración"""
        print("\n=== Tabla de Análisis LL(1) ===")
        terminales = sorted(self.gramatica.terminales)
        
        # Imprimir encabezado
        print(f"{'NT':<5}", end='')
        for t in terminales:
            print(f"{t:<15}", end='')
        print()
        
        # Imprimir filas
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