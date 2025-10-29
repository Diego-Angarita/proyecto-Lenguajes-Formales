"""
Analizador SLR(1) - Implementación Principal
"""

from ItemLR0 import ItemLR0, EstadoLR0

class AnalizadorSLR1:
    def __init__(self, gramatica, primero_siguiente):
        self.gramatica = gramatica
        self.primero_siguiente = primero_siguiente
        self.estados = []
        self.accion = {}  # (estado, terminal) -> ('desplazar', estado) | ('reducir', produccion) | 'aceptar'
        self.ir_a = {}    # (estado, no_terminal) -> estado
        self.es_slr1 = False
        
        # Aumentar gramática: S' -> S
        self.inicio_aumentado = "S'"
    
    def clausura(self, items):
        """
        Calcular clausura de un conjunto de items
        Si [A -> a·Bb] está en clausura, agregar todos [B -> ·γ] para B -> γ
        """
        conjunto_clausura = set(items)
        agregado = True
        
        while agregado:
            agregado = False
            nuevos_items = set()
            
            for item in conjunto_clausura:
                simbolo_sig = item.simbolo_siguiente()
                
                # Si el siguiente símbolo es un no terminal
                if simbolo_sig and simbolo_sig in self.gramatica.no_terminales:
                    # Agregar todas las producciones de ese no terminal
                    for produccion in self.gramatica.obtener_producciones(simbolo_sig):
                        nuevo_item = ItemLR0(simbolo_sig, produccion, 0)
                        if nuevo_item not in conjunto_clausura:
                            nuevos_items.add(nuevo_item)
                            agregado = True
            
            conjunto_clausura.update(nuevos_items)
        
        return conjunto_clausura
    
    def calcular_ir_a(self, items, simbolo):
        """
        Calcular IR_A(I, X): conjunto de items [A -> aX·b] tal que [A -> a·Xb] está en I
        """
        conjunto_ir_a = set()
        
        for item in items:
            if item.simbolo_siguiente() == simbolo:
                avanzado = item.avanzar()
                if avanzado:
                    conjunto_ir_a.add(avanzado)
        
        return self.clausura(conjunto_ir_a)
    
    def construir_automata(self):
        """Construir autómata LR(0) (colección de conjuntos de items LR(0))"""
        
        # Crear estado inicial con producción aumentada S' -> ·S
        item_inicial = ItemLR0(self.inicio_aumentado, [self.gramatica.simbolo_inicial], 0)
        items_iniciales = self.clausura({item_inicial})
        
        estado_inicial = EstadoLR0(0)
        for item in items_iniciales:
            estado_inicial.agregar_item(item)
        
        self.estados = [estado_inicial]
        dict_estados = {frozenset(items_iniciales): 0}  # Mapear conjuntos de items a IDs de estado
        
        # Cola de estados a procesar
        cola = [estado_inicial]
        
        while cola:
            estado_actual = cola.pop(0)
            
            # Encontrar todos los símbolos que pueden seguir al punto
            simbolos = set()
            for item in estado_actual.items:
                simbolo_sig = item.simbolo_siguiente()
                if simbolo_sig:
                    simbolos.add(simbolo_sig)
            
            # Para cada símbolo, calcular IR_A y crear nuevo estado si es necesario
            for simbolo in simbolos:
                items_ir_a = self.calcular_ir_a(estado_actual.items, simbolo)
                
                if len(items_ir_a) == 0:
                    continue
                
                ir_a_congelado = frozenset(items_ir_a)
                
                if ir_a_congelado in dict_estados:
                    # Estado ya existe
                    id_estado_siguiente = dict_estados[ir_a_congelado]
                else:
                    # Crear nuevo estado
                    id_estado_siguiente = len(self.estados)
                    nuevo_estado = EstadoLR0(id_estado_siguiente)
                    for item in items_ir_a:
                        nuevo_estado.agregar_item(item)
                    
                    self.estados.append(nuevo_estado)
                    dict_estados[ir_a_congelado] = id_estado_siguiente
                    cola.append(nuevo_estado)
                
                # Agregar transición
                estado_actual.transiciones[simbolo] = id_estado_siguiente
    
    def construir_tabla_analisis(self):
        """Construir tabla de análisis SLR(1) (tablas ACCION e IR_A)"""
        
        self.construir_automata()
        conflictos = []
        
        for estado in self.estados:
            for item in estado.items:
                # Caso 1: Items de desplazamiento [A -> α·aβ] donde a es terminal
                simbolo_sig = item.simbolo_siguiente()
                if simbolo_sig and simbolo_sig in self.gramatica.terminales:
                    clave = (estado.id_estado, simbolo_sig)
                    estado_siguiente = estado.transiciones.get(simbolo_sig)
                    
                    if clave in self.accion:
                        conflictos.append(f"Conflicto Desplazar-Reducir en estado {estado.id_estado}")
                        self.es_slr1 = False
                    else:
                        self.accion[clave] = ('desplazar', estado_siguiente)
                
                # Caso 2: Items de reducción [A -> α·]
                elif simbolo_sig is None:
                    # Verificar si es el item de aceptación
                    if item.no_terminal == self.inicio_aumentado:
                        clave = (estado.id_estado, '$')
                        self.accion[clave] = 'aceptar'
                    else:
                        # Agregar acción de reducción para todos los terminales en SIGUIENTE(A)
                        for terminal in self.primero_siguiente.siguiente[item.no_terminal]:
                            clave = (estado.id_estado, terminal)
                            
                            if clave in self.accion:
                                conflictos.append(f"Conflicto Reducir-Reducir en estado {estado.id_estado}")
                                self.es_slr1 = False
                            else:
                                self.accion[clave] = ('reducir', item.no_terminal, item.produccion)
                
                # Caso 3: IR_A para no terminales
                if simbolo_sig and simbolo_sig in self.gramatica.no_terminales:
                    clave = (estado.id_estado, simbolo_sig)
                    estado_siguiente = estado.transiciones.get(simbolo_sig)
                    self.ir_a[clave] = estado_siguiente
        
        if len(conflictos) == 0:
            self.es_slr1 = True
        
        return self.es_slr1
    
    def analizar(self, cadena_entrada):
        """Analizar cadena de entrada usando analizador SLR(1)"""
        
        if not self.es_slr1:
            return False
        
        cadena_entrada += '$'
        pila = [0]  # Pila de IDs de estado
        indice_entrada = 0
        
        while True:
            estado = pila[-1]
            entrada_actual = cadena_entrada[indice_entrada]
            
            clave = (estado, entrada_actual)
            
            if clave not in self.accion:
                return False
            
            accion = self.accion[clave]
            
            if accion == 'aceptar':
                return True
            
            elif accion[0] == 'desplazar':
                pila.append(accion[1])
                indice_entrada += 1
            
            elif accion[0] == 'reducir':
                no_terminal = accion[1]
                produccion = accion[2]
                
                # Desapilar |produccion| estados (saltar epsilon)
                if produccion != ['e']:
                    for _ in range(len(produccion)):
                        pila.pop()
                
                # Obtener estado actual después de desapilar
                estado_actual = pila[-1]
                
                # Usar tabla IR_A
                clave_ir_a = (estado_actual, no_terminal)
                if clave_ir_a not in self.ir_a:
                    return False
                
                pila.append(self.ir_a[clave_ir_a])
            
            else:
                return False
    
    def imprimir_estados(self):
        """Imprimir todos los estados para depuración"""
        print("\nAutómata LR(0)")
        for estado in self.estados:
            print(estado)
            if estado.transiciones:
                print("  Transiciones:")
                for simbolo, estado_siguiente in estado.transiciones.items():
                    print(f"    {simbolo} -> Estado {estado_siguiente}")
            print()