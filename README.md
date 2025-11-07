# proyecto-Lenguajes-Formales
Proyecto final de lenguajes formales con gramaticas libres de contexto


def imprimir_estadisticas(self):
        """Imprime estadísticas del grafo"""
        print("\n=== Estadísticas del Autómata ===")
        print(f"Total de estados: {len(self.vertices)}")
        print(f"Total de transiciones: {len(self.aristas)}")
        print(f"Es determinista: {self.es_determinista()}")
        
        grados_entrada = self.grado_entrada()
        grados_salida = self.grado_salida()
        
        print(f"\nEstado con más transiciones de entrada: "
              f"Estado {max(grados_entrada, key=grados_entrada.get)} "
              f"({max(grados_entrada.values())} transiciones)")
        
        print(f"Estado con más transiciones de salida: "
              f"Estado {max(grados_salida, key=grados_salida.get)} "
              f"({max(grados_salida.values())} transiciones)")
        
        if self.estado_inicial:
            alcanzables = self.bfs_alcanzables(self.estado_inicial)
            print(f"\nEstados alcanzables desde inicio: {len(alcanzables)}")
            
            no_alcanzables, sin_salida = self.encontrar_estados_inutiles()
            if no_alcanzables:
                print(f"Estados NO alcanzables: {no_alcanzables}")
            if sin_salida:
                print(f"Estados sin salida útil: {sin_salida}")