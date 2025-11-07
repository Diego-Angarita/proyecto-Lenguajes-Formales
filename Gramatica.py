"""
Módulo de Representación de Gramáticas Libres de Contexto (CFG)

Este módulo es el núcleo para la representación de una gramática. Se encarga de
almacenar, procesar y proporcionar acceso a los componentes de una gramática,
tales como producciones, símbolos terminales y no terminales.

Funcionalidades clave:
- Parseo de gramáticas desde la entrada estándar.
- Clasificación automática de símbolos.
- Estructura de datos optimizada para el acceso a producciones.
"""

class Gramatica:
    """
    Representa una Gramática Libre de Contexto (CFG).

    Esta clase almacena la definición de una gramática, incluyendo sus producciones,
    símbolos y el símbolo inicial. La estructura está diseñada para facilitar
    los algoritmos de análisis sintáctico.

    Atributos:
        producciones (dict): Un diccionario que mapea cada no terminal a una lista
        de sus producciones. Cada producción es una lista de símbolos.
        Ej: {'S': [['A', 'b'], ['c']]}
        no_terminales (set): Un conjunto que contiene todos los símbolos no terminales.
        terminales (set): Un conjunto que contiene todos los símbolos terminales.
        simbolo_inicial (str): El símbolo inicial de la gramática.
    """
    def __init__(self):
        """Inicializa una gramática vacía."""
        self.producciones = {}
        self.no_terminales = set()
        self.terminales = set()
        self.simbolo_inicial = 'S'  # Valor por defecto, se sobrescribe durante el parseo.

    def agregar_produccion(self, no_terminal, produccion):
        """
        Añade una regla de producción y actualiza los conjuntos de símbolos.

        Este método es el único punto de entrada para añadir producciones,
        asegurando que la gramática se mantenga consistente.

        Args:
            no_terminal (str): El no terminal del lado izquierdo de la producción.
            produccion (list[str]): La secuencia de símbolos en el lado derecho.
        """
        # Asegura que el no terminal tenga una entrada en el diccionario.
        if no_terminal not in self.producciones:
            self.producciones[no_terminal] = []
        self.producciones[no_terminal].append(produccion)
        self.no_terminales.add(no_terminal)

        # Identifica y registra los símbolos terminales basándose en la convención
        # de que los terminales son minúsculas o símbolos no alfabéticos.
        for simbolo in produccion:
            if simbolo != 'e' and not simbolo.isupper() and simbolo != '$':
                self.terminales.add(simbolo)

    def parsear_entrada(self):
        """
        Parsea una gramática desde la entrada estándar.

        El método lee la definición de la gramática, que consiste en el número
        de reglas seguido de las reglas mismas. Es flexible y soporta dos
        formatos comunes para definir las producciones.

        Formatos de entrada soportados:
        1. "A -> a b | c": Múltiples producciones para un no terminal en una línea.
        2. "A a b c": Un no terminal seguido de sus producciones.

        El primer no terminal leído se establece como el símbolo inicial.
        """
        try:
            n = int(input().strip())
        except (ValueError, EOFError):
            n = 0
            
        primer_no_terminal = None

        for _ in range(n):
            try:
                linea = input().strip()
            except EOFError:
                break

            if not linea:
                continue

            # Detección automática del formato de la regla.
            if '->' in linea:
                # Formato: "A -> prod1 prod2 ..."
                partes = linea.split('->')
                no_terminal = partes[0].strip()
                producciones_str = partes[1].strip().split()
            else:
                # Formato: "A prod1 prod2 ..."
                partes = linea.split()
                no_terminal = partes[0]
                producciones_str = partes[1:]

            # Establece el símbolo inicial con el primer no terminal encontrado.
            if primer_no_terminal is None:
                primer_no_terminal = no_terminal

            for prod_str in producciones_str:
                produccion = list(prod_str) if prod_str != 'e' else ['e']
                self.agregar_produccion(no_terminal, produccion)

        if primer_no_terminal:
            self.simbolo_inicial = primer_no_terminal

        # El símbolo '$' se añade explícitamente para representar el fin de la cadena.
        self.terminales.add('$')

    def obtener_producciones(self, no_terminal):
        """
        Devuelve todas las producciones para un no terminal dado.

        Args:
            no_terminal (str): El símbolo no terminal a consultar.

        Returns:
            list[list[str]]: Una lista de producciones. Si el no terminal
                             no existe, devuelve una lista vacía.
        """
        return self.producciones.get(no_terminal, [])

    def __str__(self):
        """
        Genera una representación en cadena de la gramática en formato BNF.

        Returns:
            str: Una cadena multilinea que representa la gramática, ideal para
            visualización. Ej: "S -> A b | c".
        """
        resultado = []
        # Ordena los no terminales para una salida consistente.
        for nt in sorted(self.producciones.keys()):
            prods_str = ["".join(p) for p in self.producciones[nt]]
            resultado.append(f"{nt} -> {' | '.join(prods_str)}")
        return '\n'.join(resultado)