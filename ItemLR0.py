"""
Implementación de Analizador SLR(1)
Analizador sintáctico ascendente (Bottom-Up) usando items LR(0) y tabla SLR(1)
"""

class ItemLR0:
    """Representa un item LR(0): A -> α·β"""
    
    def __init__(self, no_terminal, produccion, posicion_punto):
        self.no_terminal = no_terminal
        self.produccion = produccion
        self.posicion_punto = posicion_punto
    
    def __eq__(self, otro):
        return (self.no_terminal == otro.no_terminal and
                self.produccion == otro.produccion and
                self.posicion_punto == otro.posicion_punto)
    
    def __hash__(self):
        return hash((self.no_terminal, tuple(self.produccion), self.posicion_punto))
    
    def __repr__(self):
        prod_str = list(self.produccion)
        prod_str.insert(self.posicion_punto, '·')
        return f"{self.no_terminal} -> {''.join(prod_str)}"
    
    def simbolo_siguiente(self):
        """Retornar el símbolo después del punto, o None si el punto está al final"""
        if self.posicion_punto < len(self.produccion):
            return self.produccion[self.posicion_punto]
        return None
    
    def avanzar(self):
        """Retornar un nuevo item con el punto movido una posición adelante"""
        if self.posicion_punto < len(self.produccion):
            return ItemLR0(self.no_terminal, self.produccion, self.posicion_punto + 1)
        return None


class EstadoLR0:
    """Representa un estado en el autómata LR(0)"""
    
    def __init__(self, id_estado):
        self.id_estado = id_estado
        self.items = set()
        self.transiciones = {}  # simbolo -> id_estado_siguiente
    
    def agregar_item(self, item):
        self.items.add(item)
    
    def __eq__(self, otro):
        return self.items == otro.items
    
    def __hash__(self):
        return hash(frozenset(self.items))
    
    def __repr__(self):
        items_str = '\n  '.join(str(item) for item in self.items)
        return f"Estado {self.id_estado}:\n  {items_str}"