#!/usr/bin/env python3
"""
Analizador Sintáctico Dual: LL(1) y SLR(1)

Este programa implementa dos tipos de analizadores sintácticos para gramáticas libres de contexto:
- LL(1): Analizador predictivo descendente (Top-Down)
- SLR(1): Analizador LR simplificado ascendente (Bottom-Up)

El programa determina automáticamente qué tipo de analizador es aplicable para una gramática
dada y permite al usuario seleccionar entre ambos si están disponibles.

Autor: Proyecto de Lenguajes Formales y Autómatas
"""

from Gramatica import Gramatica
from First_Follow import First_Follow
from AnalizadorLL1 import AnalizadorLL1
from AnalizadorSLR1 import AnalizadorSLR1

def main():
    """
    Función principal que coordina el análisis sintáctico dual LL(1)/SLR(1)
    
    Flujo de ejecución:
    1. Parsea la gramática de entrada
    2. Calcula conjuntos PRIMERO y SIGUIENTE
    3. Construye ambos analizadores sintácticos
    4. Determina cuáles son aplicables y ofrece opciones al usuario
    """
    # Fase 1: Inicialización y parseo de la gramática de entrada
    gramatica = Gramatica()
    gramatica.parsear_entrada()
    
    # Fase 2: Cálculo de conjuntos fundamentales para análisis sintáctico
    first_follow = First_Follow(gramatica)
    first_follow.calcular_primero()    # Conjuntos PRIMERO para análisis predictivo
    first_follow.calcular_siguiente()  # Conjuntos SIGUIENTE para resolución de conflictos
    
    # Modo depuración: Descomentar para ver los conjuntos calculados
    # first_follow.imprimir_conjuntos()
    
    # Fase 3: Construcción del analizador LL(1) (Top-Down)
    analizador_ll1 = AnalizadorLL1(gramatica, first_follow)
    es_ll1 = analizador_ll1.construir_tabla_analisis()
    
    # Modo depuración: Descomentar para ver la tabla LL(1)
    # if es_ll1:
    #     analizador_ll1.imprimir_tabla()
    
    # Fase 4: Construcción del analizador SLR(1) (Bottom-Up)
    analizador_slr1 = AnalizadorSLR1(gramatica, first_follow)
    es_slr1 = analizador_slr1.construir_tabla_analisis()
    
    # Modo depuración: Descomentar para ver el autómata LR(0)
    # if es_slr1:
    #     analizador_slr1.imprimir_estados()
    
    # Fase 5: Determinación de compatibilidad y selección de analizador
    if es_ll1 and es_slr1:
        # Caso 1: Gramática compatible con ambos analizadores - Ofrecer selección
        while True:
            print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
            eleccion_both = input().strip()
            
            if eleccion_both == 'Q' or eleccion_both == 'q':
                break
            
            if eleccion_both not in ['T', 't', 'B', 'b']:
                continue
            
            # Procesar cadenas de entrada hasta encontrar línea vacía
            while True:
                linea = input().strip()
                if linea == '':
                    break
                
                # Ejecutar el analizador seleccionado por el usuario
                if eleccion_both in ['T', 't']:
                    resultado = analizador_ll1.analizar(linea)  # Análisis Top-Down
                else:
                    resultado = analizador_slr1.analizar(linea)  # Análisis Bottom-Up
                
                print("si" if resultado else "no")
    
    elif es_ll1 and not es_slr1:
        # Caso 2: Solo compatible con LL(1) - Gramática no ambigua para análisis descendente
        print("La gramatica es LL(1).")
        while True:
            print("Enter a string to analyze or Q to quit:")
            entrada = input().strip()
            if entrada == 'Q' or entrada == 'q':
                break
            if entrada == '':
                continue
            
            resultado = analizador_ll1.analizar(entrada)
            print("yes" if resultado else "no")
    
    elif not es_ll1 and es_slr1:
        # Caso 3: Solo compatible con SLR(1) - Gramática requiere análisis ascendente
        print("Gramatica es SLR(1).")
        while True:
            print("Ingresa una cadena para analizar o presiona Q para salir")
            entrada = input().strip()
            if entrada == 'Q' or entrada == 'q':
                break
            if entrada == '':
                continue
            
            resultado = analizador_slr1.analizar(entrada)
            print("SI" if resultado else "NO")
    
    else:
        # Caso 4: Gramática incompatible con ambos analizadores - Requiere técnicas más avanzadas
        print("La gramatica ingresada no se pueda analizar con ninguno de los 2 algoritmos")

if __name__ == "__main__":
    main()
