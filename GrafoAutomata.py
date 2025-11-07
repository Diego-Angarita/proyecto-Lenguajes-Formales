"""
GrafoAutomata.py
================
Implementación de Grafo Dirigido para el Autómata LR(0)
MEJORA: Usa estructura de datos de GRAFO con algoritmos avanzados
"""

from collections import deque, defaultdict

class Vertice:
    """Representa un estado (vértice) en el grafo del autómata"""
    
    def __init__(self, id_estado, items=None):
        self.id = id_estado
        self.items = items if items else set()
        self.vecinos = {}  # simbolo -> id_estado_destino
    
    def agregar_transicion(self, simbolo, destino_id):
        """Agregar arista de transición"""
        self.vecinos[simbolo] = destino_id
    
    def __repr__(self):
        return f"V{self.id}(items={len(self.items)}, trans={len(self.vecinos)})"


class GrafoAutomata:
    """Grafo dirigido que representa el autómata LR(0)"""
    
    def __init__(self):
        self.vertices = {}  # id -> Vertice
        self.aristas = []   # Lista de (origen, simbolo, destino)
        self.estado_inicial = None
        self.estados_finales = set()
    
    def agregar_vertice(self, id_estado, items=None):
        """Agregar un estado (vértice) al grafo"""
        if id_estado not in self.vertices:
            self.vertices[id_estado] = Vertice(id_estado, items)
        return self.vertices[id_estado]
    
    def agregar_arista(self, origen_id, simbolo, destino_id):
        """Agregar una transición (arista) entre estados"""
        if origen_id in self.vertices:
            self.vertices[origen_id].agregar_transicion(simbolo, destino_id)
            self.aristas.append((origen_id, simbolo, destino_id))
    
    def obtener_vecinos(self, estado_id):
        """Obtener todos los vecinos de un estado"""
        if estado_id in self.vertices:
            return self.vertices[estado_id].vecinos
        return {}
    
    def bfs_alcanzables(self, inicio_id):
        """
        BFS: Encuentra todos los estados alcanzables desde un estado inicial
        Retorna conjunto de IDs de estados alcanzables
        """
        alcanzables = set()
        cola = deque([inicio_id])
        visitados = {inicio_id}
        
        while cola:
            actual = cola.popleft()
            alcanzables.add(actual)
            
            vecinos = self.obtener_vecinos(actual)
            for simbolo, destino in vecinos.items():
                if destino not in visitados:
                    visitados.add(destino)
                    cola.append(destino)
        
        return alcanzables
    
    def dfs_ciclos(self, inicio_id):
        """
        DFS: Detecta si hay ciclos alcanzables desde un estado
        Retorna True si encuentra un ciclo
        """
        visitados = set()
        pila_recursion = set()
        
        def dfs_recursivo(nodo_id):
            visitados.add(nodo_id)
            pila_recursion.add(nodo_id)
            
            vecinos = self.obtener_vecinos(nodo_id)
            for simbolo, vecino_id in vecinos.items():
                if vecino_id not in visitados:
                    if dfs_recursivo(vecino_id):
                        return True
                elif vecino_id in pila_recursion:
                    return True  # Ciclo detectado
            
            pila_recursion.remove(nodo_id)
            return False
        
        return dfs_recursivo(inicio_id)
    
    def encontrar_estados_inutiles(self):
        """
        Encuentra estados que no son alcanzables o que no llevan a ningún estado final
        Retorna (no_alcanzables, sin_salida)
        """
        if self.estado_inicial is None:
            return set(self.vertices.keys()), set()
        
        # Estados alcanzables desde el inicio
        alcanzables = self.bfs_alcanzables(self.estado_inicial)
        no_alcanzables = set(self.vertices.keys()) - alcanzables
        
        # Estados que no llevan a ningún estado final
        sin_salida = set()
        if self.estados_finales:
            # Construir grafo inverso
            grafo_inverso = defaultdict(list)
            for origen, simbolo, destino in self.aristas:
                grafo_inverso[destino].append(origen)
            
            # BFS desde estados finales en grafo inverso
            cola = deque(self.estados_finales)
            util = set(self.estados_finales)
            
            while cola:
                actual = cola.popleft()
                for predecesor in grafo_inverso[actual]:
                    if predecesor not in util:
                        util.add(predecesor)
                        cola.append(predecesor)
            
            sin_salida = alcanzables - util
        
        return no_alcanzables, sin_salida
    
    def camino_mas_corto(self, origen_id, destino_id):
        """
        Encuentra el camino más corto entre dos estados
        Retorna lista de (estado_id, simbolo) o None si no hay camino
        """
        if origen_id not in self.vertices or destino_id not in self.vertices:
            return None
        
        cola = deque([(origen_id, [])])
        visitados = {origen_id}
        
        while cola:
            actual, camino = cola.popleft()
            
            if actual == destino_id:
                return camino
            
            vecinos = self.obtener_vecinos(actual)
            for simbolo, vecino_id in vecinos.items():
                if vecino_id not in visitados:
                    visitados.add(vecino_id)
                    nuevo_camino = camino + [(actual, simbolo)]
                    cola.append((vecino_id, nuevo_camino))
        
        return None  # No hay camino
    
    def grado_entrada(self):
        """Calcula el grado de entrada de cada vértice"""
        grados = {v: 0 for v in self.vertices}
        for origen, simbolo, destino in self.aristas:
            grados[destino] += 1
        return grados
    
    def grado_salida(self):
        """Calcula el grado de salida de cada vértice"""
        grados = {v: len(self.vertices[v].vecinos) for v in self.vertices}
        return grados
    
    def es_determinista(self):
        """
        Verifica si el autómata es determinista
        (no hay múltiples transiciones con el mismo símbolo desde un estado)
        """
        for vertice in self.vertices.values():
            simbolos = list(vertice.vecinos.keys())
            if len(simbolos) != len(set(simbolos)):
                return False
        return True
    
    def componentes_fuertemente_conexas(self):
        """
        Algoritmo de Tarjan para encontrar componentes fuertemente conexas
        Útil para análisis avanzado del autómata
        """
        indice_contador = [0]
        pila = []
        indices = {}
        low_link = {}
        en_pila = set()
        componentes = []
        
        def tarjan(v):
            indices[v] = indice_contador[0]
            low_link[v] = indice_contador[0]
            indice_contador[0] += 1
            pila.append(v)
            en_pila.add(v)
            
            vecinos = self.obtener_vecinos(v)
            for simbolo, w in vecinos.items():
                if w not in indices:
                    tarjan(w)
                    low_link[v] = min(low_link[v], low_link[w])
                elif w in en_pila:
                    low_link[v] = min(low_link[v], indices[w])
            
            if low_link[v] == indices[v]:
                componente = []
                while True:
                    w = pila.pop()
                    en_pila.remove(w)
                    componente.append(w)
                    if w == v:
                        break
                componentes.append(componente)
        
        for v in self.vertices:
            if v not in indices:
                tarjan(v)
        
        return componentes