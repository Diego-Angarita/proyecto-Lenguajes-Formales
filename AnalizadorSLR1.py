"""
Implementación del Analizador Sintáctico SLR(1)

Este módulo implementa un analizador sintáctico ascendente (Bottom-Up) del
tipo SLR(1). El proceso se divide en dos fases principales:
1. Construcción del autómata de items LR(0).
2. Creación de las tablas de análisis ACCION e IR_A.

El analizador utiliza los conjuntos SIGUIENTE para resolver conflictos de
reducción, lo que lo hace más potente que un analizador LR(0) simple.
"""

from ItemLR0 import ItemLR0, EstadoLR0

class AnalizadorSLR1:
    """
    Implementa un analizador SLR(1) completo.

    Esta clase se encarga de aumentar la gramática, construir el autómata LR(0),
    generar las tablas de análisis y, finalmente, analizar cadenas de entrada.

    Atributos:
        gramatica: La gramática original.
        primero_siguiente: Objeto con los conjuntos PRIMERO y SIGUIENTE.
        estados (list): La lista de estados (EstadoLR0) del autómata.
        accion (dict): La tabla de acciones del analizador.
        ir_a (dict): La tabla de transiciones para no terminales.
        es_slr1 (bool): True si la gramática es SLR(1), False si no.
        inicio_aumentado (str): El nuevo símbolo inicial para la gramática aumentada.
    """
    def __init__(self, gramatica, primero_siguiente):
        """Inicializa el analizador con la gramática y los conjuntos PRIMERO/SIGUIENTE."""
        self.gramatica = gramatica
        self.primero_siguiente = primero_siguiente
        self.estados = []
        self.accion = {}
        self.ir_a = {}
        self.es_slr1 = False
        
        # Se aumenta la gramática con una nueva producción S' -> S
        # para tener un único punto de aceptación.
        self.inicio_aumentado = self.gramatica.simbolo_inicial + "'"

    def clausura(self, items):
        """
        Calcula la clausura de un conjunto de items LR(0).

        La clausura expande un conjunto de items para incluir todas las producciones
        que podrían ser necesarias. Si un item tiene la forma [A -> α·Bβ], se
        añaden todos los items [B -> ·γ] a la clausura.

        Args:
            items (set): Un conjunto de `ItemLR0`.

        Returns:
            set: El conjunto de items cerrado.
        """
        conjunto_clausura = set(items)
        agregado = True
        while agregado:
            agregado = False
            nuevos_items = set()
            for item in conjunto_clausura:
                simbolo_sig = item.simbolo_siguiente()
                if simbolo_sig and simbolo_sig in self.gramatica.no_terminales:
                    for produccion in self.gramatica.obtener_producciones(simbolo_sig):
                        nuevo_item = ItemLR0(simbolo_sig, produccion, 0)
                        if nuevo_item not in conjunto_clausura and nuevo_item not in nuevos_items:
                            nuevos_items.add(nuevo_item)
                            agregado = True
            conjunto_clausura.update(nuevos_items)
        return conjunto_clausura

    def calcular_ir_a(self, items, simbolo):
        """
        Calcula la función de transición IR_A (goto) para un conjunto de items y un símbolo.

        Esta función determina el nuevo estado al que se transita desde un estado
        actual (representado por `items`) al consumir un `simbolo`.

        Args:
            items (set): El conjunto de items del estado actual.
            simbolo (str): El símbolo de transición.

        Returns:
            set: La clausura del nuevo conjunto de items.
        """
        conjunto_ir_a = set()
        for item in items:
            if item.simbolo_siguiente() == simbolo:
                avanzado = item.avanzar()
                if avanzado:
                    conjunto_ir_a.add(avanzado)
        return self.clausura(conjunto_ir_a)

    def construir_automata(self):
        """Construye el autómata de estados LR(0) (la colección canónica)."""
        # El estado inicial se crea a partir de la clausura de la producción aumentada.
        item_inicial = ItemLR0(self.inicio_aumentado, [self.gramatica.simbolo_inicial], 0)
        items_iniciales = self.clausura({item_inicial})
        
        estado_inicial = EstadoLR0(0)
        estado_inicial.items = items_iniciales
        
        self.estados = [estado_inicial]
        dict_estados = {frozenset(items_iniciales): 0}
        
        cola = [estado_inicial]
        while cola:
            estado_actual = cola.pop(0)
            
            simbolos = {item.simbolo_siguiente() for item in estado_actual.items if item.simbolo_siguiente()}
            
            for simbolo in simbolos:
                items_ir_a = self.calcular_ir_a(estado_actual.items, simbolo)
                if not items_ir_a:
                    continue
                
                ir_a_congelado = frozenset(items_ir_a)
                if ir_a_congelado in dict_estados:
                    id_estado_siguiente = dict_estados[ir_a_congelado]
                else:
                    id_estado_siguiente = len(self.estados)
                    nuevo_estado = EstadoLR0(id_estado_siguiente)
                    nuevo_estado.items = items_ir_a
                    
                    self.estados.append(nuevo_estado)
                    dict_estados[ir_a_congelado] = id_estado_siguiente
                    cola.append(nuevo_estado)
                
                estado_actual.transiciones[simbolo] = id_estado_siguiente

    def construir_tabla_analisis(self):
        """
        Construye las tablas de análisis SLR(1) (ACCION e IR_A).

        Reglas:
        1. Si [A -> α·aβ] está en Ii y IR_A(Ii, a) = Ij, entonces ACCION[i, a] = "desplazar j".
        2. Si [A -> α·] está en Ii, entonces ACCION[i, b] = "reducir A -> α" para todo b en SIGUIENTE(A).
        3. Si [S' -> S·] está en Ii, entonces ACCION[i, $] = "aceptar".
        4. Si IR_A(Ii, A) = Ij, entonces IR_A[i, A] = j.

        Returns:
            bool: True si no hay conflictos, False si se encuentra alguno.
        """
        self.construir_automata()
        conflictos = []

        for estado in self.estados:
            for item in estado.items:
                simbolo_sig = item.simbolo_siguiente()

                # Regla 1: Acción de desplazamiento
                if simbolo_sig and simbolo_sig in self.gramatica.terminales:
                    clave = (estado.id_estado, simbolo_sig)
                    estado_siguiente = estado.transiciones.get(simbolo_sig)
                    if clave in self.accion and self.accion[clave] != ('desplazar', estado_siguiente):
                        conflictos.append(f"Conflicto Desplazar-Reducir en estado {estado.id_estado} con símbolo {simbolo_sig}")
                    else:
                        self.accion[clave] = ('desplazar', estado_siguiente)

                # Reglas 2 y 3: Acciones de reducción y aceptación
                elif not simbolo_sig:
                    if item.no_terminal == self.inicio_aumentado:
                        # Regla 3: Aceptación
                        self.accion[(estado.id_estado, '$')] = 'aceptar'
                    else:
                        # Regla 2: Reducción
                        for terminal in self.primero_siguiente.siguiente[item.no_terminal]:
                            clave = (estado.id_estado, terminal)
                            produccion_a_reducir = (item.no_terminal, tuple(item.produccion))
                            if clave in self.accion:
                                conflictos.append(f"Conflicto Reducir-Reducir en estado {estado.id_estado} con símbolo {terminal}")
                            else:
                                self.accion[clave] = ('reducir', item.no_terminal, item.produccion)
            
            # Regla 4: Tabla IR_A para no terminales
            for simbolo, id_estado_siguiente in estado.transiciones.items():
                if simbolo in self.gramatica.no_terminales:
                    self.ir_a[(estado.id_estado, simbolo)] = id_estado_siguiente

        self.es_slr1 = not conflictos
        if conflictos:
            print("Conflictos encontrados:", conflictos)
        return self.es_slr1

    def analizar(self, cadena_entrada):
        """
        Analiza una cadena de entrada utilizando las tablas SLR(1).

        El analizador utiliza una pila de estados y las tablas ACCION e IR_A
        para decidir si desplazar, reducir o aceptar.

        Args:
            cadena_entrada (str): La cadena a analizar.

        Returns:
            bool: True si la cadena es aceptada, False si no.
        """
        if not self.es_slr1:
            return False
        
        cadena_entrada += '$'
        pila = [0]
        indice_entrada = 0
        
        while True:
            estado = pila[-1]
            simbolo_actual = cadena_entrada[indice_entrada]
            clave = (estado, simbolo_actual)

            if clave not in self.accion:
                return False  # Error: acción no definida.
            
            accion = self.accion[clave]
            
            if accion == 'aceptar':
                return True
            
            elif accion[0] == 'desplazar':
                pila.append(accion[1])
                indice_entrada += 1
            
            elif accion[0] == 'reducir':
                no_terminal, produccion = accion[1], accion[2]
                
                if produccion != ['e']:
                    for _ in produccion:
                        pila.pop()
                
                estado_actual = pila[-1]
                clave_ir_a = (estado_actual, no_terminal)
                
                if clave_ir_a not in self.ir_a:
                    return False # Error: transición IR_A no definida.
                
                pila.append(self.ir_a[clave_ir_a])
            
            else:
                return False # Acción desconocida.

    def imprimir_estados(self):
        """Imprime los estados y transiciones del autómata LR(0) para depuración."""
        print("\n=== Autómata LR(0) ===")
        for estado in self.estados:
            print(estado)
            if estado.transiciones:
                print("  Transiciones:")
                for simbolo, estado_siguiente in estado.transiciones.items():
                    print(f"    {simbolo} -> Estado {estado_siguiente}")
            print()