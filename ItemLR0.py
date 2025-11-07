"""
Definición de Items y Estados LR(0)

Este módulo contiene las estructuras de datos para los items y estados LR(0),
que son los componentes básicos para construir el autómata de un analizador SLR(1).

- ItemLR0: Una producción con un punto en una posición del lado derecho.
- EstadoLR0: Un conjunto de items LR(0) que representa un estado en el autómata.
"""

class ItemLR0:
    """
    Representa un item LR(0), que es una producción con un punto.

    Un item LR(0) como "A -> α·β" indica que hemos visto una cadena derivable
    de α y esperamos ver una cadena derivable de β.

    Atributos:
        no_terminal (str): El no terminal de la producción.
        produccion (list[str]): La lista de símbolos de la producción.
        posicion_punto (int): El índice que indica la posición del punto.
    """
    def __init__(self, no_terminal, produccion, posicion_punto):
        """Inicializa un item LR(0)."""
        self.no_terminal = no_terminal
        self.produccion = produccion
        self.posicion_punto = posicion_punto

    def __eq__(self, otro):
        """Compara dos items para ver si son idénticos."""
        return (isinstance(otro, ItemLR0) and
                self.no_terminal == otro.no_terminal and
                self.produccion == otro.produccion and
                self.posicion_punto == otro.posicion_punto)

    def __hash__(self):
        """Genera un hash para el item, permitiendo su uso en conjuntos."""
        return hash((self.no_terminal, tuple(self.produccion), self.posicion_punto))

    def __repr__(self):
        """Devuelve una representación legible del item, ej: "A -> α·β"."""
        prod_str = list(self.produccion)
        prod_str.insert(self.posicion_punto, '·')
        return f"{self.no_terminal} -> {''.join(prod_str)}"

    def simbolo_siguiente(self):
        """
        Devuelve el símbolo inmediatamente después del punto.

        Returns:
            str or None: El símbolo si existe, o None si el punto está al final.
        """
        if self.posicion_punto < len(self.produccion):
            return self.produccion[self.posicion_punto]
        return None

    def avanzar(self):
        """
        Crea un nuevo item con el punto desplazado una posición a la derecha.

        Esto representa el consumo de un símbolo durante el análisis.

        Returns:
            ItemLR0 or None: El nuevo item si es posible avanzar, o None.
        """
        if self.posicion_punto < len(self.produccion):
            return ItemLR0(self.no_terminal, self.produccion, self.posicion_punto + 1)
        return None


class EstadoLR0:
    """
    Representa un estado en el autómata LR(0), compuesto por un conjunto de items.

    Cada estado agrupa un conjunto de items LR(0) y define las transiciones
    hacia otros estados basadas en los símbolos de la gramática.

    Atributos:
        id_estado (int): Un identificador único para el estado.
        items (set): El conjunto de `ItemLR0` que conforman el estado.
        transiciones (dict): Mapeo de símbolos a los IDs de los estados siguientes.
    """
    def __init__(self, id_estado):
        """Inicializa un estado LR(0) con un ID."""
        self.id_estado = id_estado
        self.items = set()
        self.transiciones = {}  # Mapea: simbolo -> id_estado_siguiente

    def agregar_item(self, item):
        """Añade un item al conjunto del estado."""
        self.items.add(item)

    def __eq__(self, otro):
        """
        Compara dos estados basándose en sus conjuntos de items.
        Dos estados son iguales si contienen exactamente los mismos items.
        """
        return isinstance(otro, EstadoLR0) and self.items == otro.items

    def __hash__(self):
        """
        Genera un hash para el estado basado en su conjunto de items.
        Se usa un frozenset para que el conjunto mutable sea hasheable.
        """
        return hash(frozenset(self.items))

    def __repr__(self):
        """Devuelve una representación legible del estado y sus items."""
        items_str = '\n  '.join(sorted([str(item) for item in self.items]))
        return f"Estado {self.id_estado}:\n  {items_str}"