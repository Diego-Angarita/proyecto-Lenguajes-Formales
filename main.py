#!/usr/bin/env python3
"""
Proyecto de Lenguajes Formales: Analizador LL(1) y SLR(1)
Programa principal que integra todos los componentes
"""

from Gramatica import Gramatica
from First_Follow import First_Follow
from AnalizadorLL1 import AnalizadorLL1
from AnalizadorSLR1 import AnalizadorSLR1

def main():
    # Leer gramática desde la entrada
    gramatica = Gramatica()
    gramatica.parsear_entrada()
    
    # Calcular conjuntos PRIMERO y SIGUIENTE
    first_follow = First_Follow(gramatica)
    first_follow.calcular_primero()
    first_follow.calcular_siguiente()
    
    # Descomentar para depuración:
    # first_follow.imprimir_conjuntos()
    
    # Construir analizador LL(1)
    analizador_ll1 = AnalizadorLL1(gramatica, first_follow)
    es_ll1 = analizador_ll1.construir_tabla_analisis()
    
    # Descomentar para depuración:
    # if es_ll1:
    #     analizador_ll1.imprimir_tabla()
    
    # Construir analizador SLR(1)
    analizador_slr1 = AnalizadorSLR1(gramatica, first_follow)
    es_slr1 = analizador_slr1.construir_tabla_analisis()
    
    # Descomentar para depuración:
    # if es_slr1:
    #     analizador_slr1.imprimir_estados()
    
    # Determinar en qué caso estamos
    if es_ll1 and es_slr1:
        # Caso 1: Ambos analizadores funcionan
        while True:
            print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
            eleccion_both = input().strip()
            
            if eleccion_both == 'Q' or eleccion_both == 'q':
                break
            
            if eleccion_both not in ['T', 't', 'B', 'b']:
                continue
            
            # Leer cadenas hasta línea vacía
            while True:
                linea = input().strip()
                if linea == '':
                    break
                
                if eleccion in ['T', 't']:
                    resultado = analizador_ll1.analizar(linea)
                else:
                    resultado = analizador_slr1.analizar(linea)
                
                print("yes" if resultado else "no")
    
    elif es_ll1 and not es_slr1:
        # Caso 2: Solo LL(1)
        print("Grammar is LL(1).")
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
        # Caso 3: Solo SLR(1)
        print("Grammar is SLR(1).")
        while True:
            print("Enter a string to analyze or Q to quit:")
            entrada = input().strip()
            if entrada == 'Q' or entrada == 'q':
                break
            if entrada == '':
                continue
            
            resultado = analizador_slr1.analizar(entrada)
            print("yes" if resultado else "no")
    
    else:
        # Caso 4: Ningún analizador funciona
        print("Grammar is neither LL(1) nor SLR(1).")

if __name__ == "__main__":
    main()