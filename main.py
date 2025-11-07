#!/usr/bin/env python3
"""
Punto de Entrada del Analizador Sintáctico Dual

Este script es el orquestador principal del proyecto. Su función es:
1. Recibir una gramática libre de contexto desde la entrada estándar.
2. Intentar construir un analizador LL(1) y un analizador SLR(1) para ella.
3. Informar al usuario sobre la compatibilidad de la gramática con cada tipo
   de analizador.
4. Permitir al usuario analizar cadenas de entrada utilizando el analizador
   o analizadores compatibles.
"""

import time  # Se mantiene la importación

from Gramatica import Gramatica
from First_Follow import First_Follow
from AnalizadorLL1 import AnalizadorLL1
from AnalizadorSLR1 import AnalizadorSLR1

def main():
    """
    Función principal que coordina todo el proceso de análisis.

    El flujo de ejecución es secuencial:
    1. Parseo de la gramática.
    2. Cálculo de conjuntos FIRST y FOLLOW.
    3. Construcción de ambos analizadores.
    4. Interacción con el usuario para el análisis de cadenas.
    """
    
    # Fase 1: Leer y parsear la gramática proporcionada por el usuario.
    # --- MEDICIÓN ELIMINADA DE ESTA SECCIÓN ---
    print("Por favor, introduce la gramática:")
    gramatica = Gramatica()
    gramatica.parsear_entrada()
    
    print("\nGramática parseada:")
    print(gramatica)

    # --- INICIO DE MEDICIONES ---

    # Fase 2: Calcular los conjuntos FIRST y FOLLOW
    first_follow = First_Follow(gramatica)
    
    # Medición de FIRST
    start_time_first = time.perf_counter()
    first_follow.calcular_first()
    end_time_first = time.perf_counter()
    print(f"\nCálculo de FIRST (en {end_time_first - start_time_first:.6f} segundos)")

    # Medición de FOLLOW
    start_time_follow = time.perf_counter()
    first_follow.calcular_follow()
    end_time_follow = time.perf_counter()
    print(f"Cálculo de FOLLOW (en {end_time_follow - start_time_follow:.6f} segundos)")

    # Fase 3: Construir el analizador LL(1)
    analizador_ll1 = AnalizadorLL1(gramatica, first_follow)
    
    # Medición de tabla LL(1)
    start_time_ll1 = time.perf_counter()
    es_ll1 = analizador_ll1.construir_tabla_analisis()
    end_time_ll1 = time.perf_counter()
    print(f"\nConstrucción de tabla LL(1) (en {end_time_ll1 - start_time_ll1:.6f} segundos)")

    # Fase 4: Construir el analizador SLR(1)
    analizador_slr1 = AnalizadorSLR1(gramatica, first_follow)
    
    # Medición de tabla SLR(1)
    start_time_slr1 = time.perf_counter()
    es_slr1 = analizador_slr1.construir_tabla_analisis()
    end_time_slr1 = time.perf_counter()
    print(f"Construcción de tabla SLR(1) (en {end_time_slr1 - start_time_slr1:.6f} segundos)")

    # --- FIN DE MEDICIONES ---

    # Fase 5: Informar al usuario y proceder con el análisis de cadenas.
    print("\n--- Resultados del Análisis de la Gramática ---")
    if es_ll1:
        print("La gramática es compatible con LL(1).")
    else:
        print("La gramática NO es compatible con LL(1).")
    
    if es_slr1:
        print("La gramática es compatible con SLR(1).")
    else:
        print("La gramática NO es compatible con SLR(1).")
    print("--------------------------------------------\n")

    # Bucle principal de interacción con el usuario.
    if es_ll1 and es_slr1:
        # Caso 1: Ambos analizadores están disponibles.
        while True:
            eleccion = input("Selecciona un analizador (T: LL(1), B: SLR(1), Q: salir): ").strip().upper()
            if eleccion == 'Q':
                break
            if eleccion in ['T', 'B']:
                analizador = analizador_ll1 if eleccion == 'T' else analizador_slr1
                analizar_cadenas(analizador)
    
    elif es_ll1:
        # Caso 2: Solo LL(1) está disponible.
        print("Usando el analizador LL(1).")
        analizar_cadenas(analizador_ll1)

    elif es_slr1:
        # Caso 3: Solo SLR(1) está disponible.
        print("Usando el analizador SLR(1).")
        analizar_cadenas(analizador_slr1)

    else:
        # Caso 4: Ningún analizador es compatible.
        print("La gramática no es compatible con LL(1) ni con SLR(1). No se pueden analizar cadenas.")

def analizar_cadenas(analizador):
    """
    Recibe un analizador y entra en un bucle para analizar cadenas.

    Args:
        analizador: Una instancia de AnalizadorLL1 o AnalizadorSLR1.
    """
    while True:
        linea = input("Introduce una cadena para analizar (o presiona Enter para volver): ").strip()
        if not linea:
            break
        
        # --- MEDICIÓN ELIMINADA DE ESTA SECCIÓN ---
        resultado = analizador.analizar(linea)
        
        # Se revierte a la impresión original
        print("Resultado:", "si" if resultado else "no")
    print("-" * 20)

if __name__ == "__main__":
    main()