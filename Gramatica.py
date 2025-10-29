"""
Módulo de Gramática
Maneja la representación de gramáticas libres de contexto y operaciones básicas
"""

class Gramatica:
    def __init__(self):
        self.producciones = {}  # Diccionario: NoTerminal -> Lista de producciones
        self.no_terminales = set()
        self.terminales = set()
        self.simbolo_inicial = 'S'
        
    def agregar_produccion(self, no_terminal, produccion):
        """Agregar una regla de producción a la gramática"""
        if no_terminal not in self.producciones:
            self.producciones[no_terminal] = []
        self.producciones[no_terminal].append(produccion)
        self.no_terminales.add(no_terminal)
        
        # Identificar terminales
        for simbolo in produccion:
            if simbolo != 'e' and not simbolo.isupper() and simbolo != '$':
                self.terminales.add(simbolo)
    
    def parsear_entrada(self):
        """Parsear gramática desde entrada estándar"""
        n = int(input().strip())
        
        for _ in range(n):
            linea = input().strip()
            # Verificar si la línea contiene '->'
            if '->' in linea:
                partes = linea.split('->')
                no_terminal = partes[0].strip()
                
                # Parsear producciones separadas por espacios
                producciones_str = partes[1].strip().split()
                
                for prod in producciones_str:
                    # Convertir string a lista de símbolos
                    produccion = list(prod)
                    self.agregar_produccion(no_terminal, produccion)
            else:
                # Formato alternativo: primer carácter es el no terminal
                partes = linea.split()
                if partes and len(partes) >= 1:
                    no_terminal = partes[0][0]  # Primer carácter del primer elemento
                    
                    # El resto de la línea contiene producciones
                    for i in range(1, len(partes)):
                        produccion = list(partes[i])
                        self.agregar_produccion(no_terminal, produccion)
        
        # Agregar $ a terminales para fin de cadena
        self.terminales.add('$')
    
    def obtener_producciones(self, no_terminal):
        """Obtener todas las producciones para un no terminal"""
        return self.producciones.get(no_terminal, [])
    
    def __str__(self):
        """Representación en string de la gramática"""
        resultado = []
        for nt in sorted(self.producciones.keys()):
            prods = [''.join(p) for p in self.producciones[nt]]
            resultado.append(f"{nt} -> {' | '.join(prods)}")
        return '\n'.join(resultado)
        