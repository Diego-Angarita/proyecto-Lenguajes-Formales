"""
ArbolSintactico.py
==================
Implementación de Árbol de Análisis Sintáctico (Parse Tree)
Esta es una MEJORA CONCRETA usando árboles como estructura de datos
"""

class NodoArbol:
    """Representa un nodo en el árbol de análisis sintáctico"""
    
    def __init__(self, simbolo, tipo='no_terminal'):
        self.simbolo = simbolo
        self.tipo = tipo  # 'terminal' o 'no_terminal'
        self.hijos = []
        self.padre = None
        self.nivel = 0
    
    def agregar_hijo(self, hijo):
        """Agregar un hijo al nodo"""
        self.hijos.append(hijo)
        hijo.padre = self
        hijo.nivel = self.nivel + 1
    
    def es_hoja(self):
        """Verifica si el nodo es una hoja (terminal)"""
        return len(self.hijos) == 0
    
    def obtener_hojas(self):
        """Obtiene todas las hojas del subárbol (orden izquierda-derecha)"""
        if self.es_hoja():
            return [self]
        
        hojas = []
        for hijo in self.hijos:
            hojas.extend(hijo.obtener_hojas())
        return hojas
    
    def __repr__(self):
        return f"Nodo({self.simbolo}, hijos={len(self.hijos)})"
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        """Imprime el árbol en formato visual"""
        print(prefijo + ("└── " if es_ultimo else "├── ") + self.simbolo)
        
        prefijo += "    " if es_ultimo else "│   "
        
        for i, hijo in enumerate(self.hijos):
            hijo.imprimir_arbol(prefijo, i == len(self.hijos) - 1)


class ArbolSintactico:
    """Árbol de análisis sintáctico completo"""
    
    def __init__(self, raiz=None):
        self.raiz = raiz
    
    def imprimir(self):
        """Imprime el árbol completo"""
        if self.raiz:
            print("\n=== Árbol de Análisis Sintáctico ===")
            self.raiz.imprimir_arbol()
        else:
            print("Árbol vacío")
    
    def obtener_cadena_derivada(self):
        """Obtiene la cadena de entrada original (hojas del árbol)"""
        if not self.raiz:
            return ""
        hojas = self.raiz.obtener_hojas()
        return ''.join(hoja.simbolo for hoja in hojas if hoja.simbolo != 'e')
    
    def altura(self):
        """Calcula la altura del árbol"""
        return self._altura_recursiva(self.raiz)
    
    def _altura_recursiva(self, nodo):
        if not nodo or nodo.es_hoja():
            return 0
        return 1 + max(self._altura_recursiva(hijo) for hijo in nodo.hijos)
    
    def contar_nodos(self):
        """Cuenta el número total de nodos"""
        return self._contar_nodos_recursivo(self.raiz)
    
    def _contar_nodos_recursivo(self, nodo):
        if not nodo:
            return 0
        return 1 + sum(self._contar_nodos_recursivo(hijo) for hijo in nodo.hijos)