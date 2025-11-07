"""
Módulo de Representación de Gramáticas Libres de Contexto

Este módulo define la estructura de datos fundamental para representar gramáticas
libres de contexto (CFG) y proporciona métodos para:
- Parsear gramáticas desde entrada estándar
- Clasificar símbolos en terminales y no terminales
- Gestionar reglas de producción
- Proporcionar acceso estructurado a las producciones

Formato de entrada soportado:
- Formato estándar: A -> abc def
- Formato alternativo: A abc def (primer carácter es el no terminal)
"""

class Gramatica:
    """
    Representación de una Gramática Libre de Contexto (CFG)
    
    Atributos:
        producciones: Mapeo de no terminales a sus reglas de producción
        no_terminales: Conjunto de símbolos no terminales (mayúsculas)
        terminales: Conjunto de símbolos terminales (minúsculas y símbolos especiales)
        simbolo_inicial: Símbolo de inicio de la gramática (por defecto 'S')
    """
    def __init__(self):
        self.producciones = {}      # Dict[str, List[List[str]]]: NoTerminal -> Lista de producciones
        self.no_terminales = set()  # Set[str]: Símbolos no terminales identificados
        self.terminales = set()     # Set[str]: Símbolos terminales identificados
        self.simbolo_inicial = 'S'  # str: Símbolo inicial por defecto
        
    def agregar_produccion(self, no_terminal, produccion):
        """
        Agregar una regla de producción a la gramática
        
        Args:
            no_terminal (str): Símbolo no terminal del lado izquierdo
            produccion (List[str]): Secuencia de símbolos del lado derecho
            
        Efectos secundarios:
            - Actualiza el conjunto de no terminales
            - Clasifica automáticamente los símbolos como terminales o no terminales
        """
        if no_terminal not in self.producciones:
            self.producciones[no_terminal] = []
        self.producciones[no_terminal].append(produccion)
        self.no_terminales.add(no_terminal)
        
        # Clasificación automática de símbolos terminales
        # Criterio: minúsculas y símbolos especiales (excepto epsilon 'e' y fin de cadena '$')
        for simbolo in produccion:
            if simbolo != 'e' and not simbolo.isupper() and simbolo != '$':
                self.terminales.add(simbolo)
    
    def parsear_entrada(self):
        """
        Parsear gramática desde entrada estándar
        
        Formato de entrada esperado:
        - Primera línea: número de reglas de producción
        - Siguientes líneas: reglas en formato "A -> abc def" o "A abc def"
        
        Maneja dos formatos:
        1. Estándar: "A -> abc def" (múltiples producciones separadas por espacios)
        2. Compacto: "A abc def" (primer carácter es el no terminal)
        """
        n = int(input().strip())
        primer_no_terminal = None
        
        for i in range(n):
            linea = input().strip()
            
            # Detección automática del formato de entrada
            if '->' in linea:
                # Formato estándar: A -> produccion1 produccion2 ...
                partes = linea.split('->')
                no_terminal = partes[0].strip()
                
                # El primer no terminal encontrado será el símbolo inicial
                if primer_no_terminal is None:
                    primer_no_terminal = no_terminal
                
                # Extraer múltiples producciones separadas por espacios
                producciones_str = partes[1].strip().split()
                
                for prod in producciones_str:
                    # Descomponer cada producción en símbolos individuales
                    produccion = list(prod)
                    self.agregar_produccion(no_terminal, produccion)
            else:
                # Formato compacto: A produccion1 produccion2 ...
                partes = linea.split()
                if partes and len(partes) >= 1:
                    no_terminal = partes[0][0]  # Extraer no terminal del primer carácter
                    
                    # El primer no terminal encontrado será el símbolo inicial
                    if primer_no_terminal is None:
                        primer_no_terminal = no_terminal
                    
                    # Procesar cada producción restante
                    for j in range(1, len(partes)):
                        produccion = list(partes[j])
                        self.agregar_produccion(no_terminal, produccion)
        
        # Establecer el símbolo inicial como el primer no terminal encontrado
        if primer_no_terminal is not None:
            self.simbolo_inicial = primer_no_terminal
        
        # Agregar marcador de fin de cadena al conjunto de terminales
        self.terminales.add('$')
    
    def obtener_producciones(self, no_terminal):
        """
        Obtener todas las producciones para un no terminal específico
        
        Args:
            no_terminal (str): Símbolo no terminal a consultar
            
        Returns:
            List[List[str]]: Lista de producciones (cada producción es una lista de símbolos)
        """
        return self.producciones.get(no_terminal, [])
    
    def __str__(self):
        """
        Representación textual de la gramática en formato BNF
        
        Returns:
            str: Gramática formateada como "A -> prod1 | prod2 | ..."
        """
        resultado = []
        for nt in sorted(self.producciones.keys()):
            # Convertir cada producción (lista) a string y unir con '|'
            prods = [''.join(p) for p in self.producciones[nt]]
            resultado.append(f"{nt} -> {' | '.join(prods)}")
        return '\n'.join(resultado)
        