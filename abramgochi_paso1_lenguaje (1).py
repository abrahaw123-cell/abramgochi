"""
ABRAMGOCHI — Paso 1: Lenguaje
==============================
Los agentes ahora manejan palabras, no solo números.
Cada nodo tiene un token (palabra) que intercambia
con sus vecinos — primer paso hacia compresión de lenguaje.

Author: Abraham
Framework: H.A.S. | Genoma Cognitivo
Date: March 2026
"""

import random
import networkx as nx
from collections import Counter

# =====================
# 📖 VOCABULARIO
# =====================
# Estas son las "palabras" que conoce el sistema.
# Más adelante vendrán de texto real (FineWeb, etc.)
VOCABULARIO = [
    "agente", "red", "mente", "campo", "nodo",
    "energía", "patrón", "densidad", "relación", "sistema",
    "emergente", "adaptación", "evolución", "conexión", "flujo"
]

# =====================
# 🌐 RED RELACIONAL
# =====================
def crear_red_lenguaje(n=8, p=0.5):
    """
    Crea la red de agentes.
    Cada agente tiene un token (palabra) inicial aleatorio.
    La red es el V_eff(r) — el campo que condiciona a todos.
    """
    G = nx.erdos_renyi_graph(n=n, p=p)
    
    # Cada nodo = un agente con una palabra
    estado = {
        nodo: random.choice(VOCABULARIO)
        for nodo in G.nodes()
    }
    
    return G, estado

# =====================
# 🧠 INTERCAMBIO DE TOKENS
# =====================
def actualizar_lenguaje(G, estado):
    """
    Cada agente mira a sus vecinos y aprende de ellos.
    
    Regla: adopta la palabra más frecuente entre sus vecinos.
    Si hay empate — elige aleatoriamente entre las más comunes.
    
    Esto es compresión básica: las palabras más "relacionadas"
    tienden a converger en los mismos nodos.
    """
    nuevo_estado = {}
    
    for nodo in G.nodes():
        vecinos = list(G.neighbors(nodo))
        
        if vecinos:
            # Recolecta palabras de vecinos
            palabras_vecinos = [estado[v] for v in vecinos]
            
            # Cuenta cuáles aparecen más
            conteo = Counter(palabras_vecinos)
            mas_comun = conteo.most_common(1)[0][0]
            
            # El agente adopta la palabra más frecuente
            # con algo de ruido (no siempre copia — a veces innova)
            if random.random() < 0.8:
                nuevo_estado[nodo] = mas_comun
            else:
                nuevo_estado[nodo] = random.choice(VOCABULARIO)
        else:
            # Sin vecinos — mantiene su palabra
            nuevo_estado[nodo] = estado[nodo]
    
    return nuevo_estado

# =====================
# 📊 MEMORIA DE PATRONES
# =====================
def registrar_patrones(historial):
    """
    Aprende qué palabras aparecen juntas frecuentemente.
    Esto es el inicio de la compresión de lenguaje:
    si "agente" y "red" siempre aparecen juntos,
    el sistema los comprime como un patrón.
    """
    patrones = Counter()
    
    for estado in historial:
        palabras = list(estado.values())
        # Registra pares de palabras que coexisten
        for i in range(len(palabras)):
            for j in range(i+1, len(palabras)):
                par = tuple(sorted([palabras[i], palabras[j]]))
                patrones[par] += 1
    
    return patrones

# =====================
# 🧬 MUTACIÓN DE VOCABULARIO
# =====================
def mutar_vocabulario(estado, tasa=0.1):
    """
    hijo = copia(padre) + mutación
    
    Con pequeña probabilidad, un agente introduce
    una palabra nueva al sistema — igual que la mutación
    genética introduce variación.
    """
    nuevo = estado.copy()
    for nodo in nuevo:
        if random.random() < tasa:
            nuevo[nodo] = random.choice(VOCABULARIO)
    return nuevo

# =====================
# 🚀 EJECUCIÓN
# =====================
if __name__ == "__main__":
    
    print("\n" + "="*50)
    print("  ABRAMGOCHI — Paso 1: Lenguaje")
    print("  Agentes con tokens de vocabulario")
    print("="*50 + "\n")
    
    # Crear red
    G, estado = crear_red_lenguaje(n=8, p=0.5)
    
    print("Estado inicial de los agentes:")
    for nodo, palabra in estado.items():
        vecinos = list(G.neighbors(nodo))
        print(f"  Nodo {nodo}: '{palabra}' | vecinos: {vecinos}")
    
    # Historial para aprender patrones
    historial = [estado.copy()]
    
    print("\n📡 Simulando intercambio de lenguaje...\n")
    
    for paso in range(5):
        estado = actualizar_lenguaje(G, estado)
        estado = mutar_vocabulario(estado, tasa=0.1)
        historial.append(estado.copy())
        
        # Palabra más dominante en este paso
        conteo_global = Counter(estado.values())
        dominante = conteo_global.most_common(1)[0]
        
        print(f"Paso {paso+1}: palabra dominante = '{dominante[0]}' "
              f"({dominante[1]} nodos) | estado: {list(estado.values())}")
    
    # Patrones aprendidos
    print("\n🔍 Patrones de co-ocurrencia aprendidos:")
    patrones = registrar_patrones(historial)
    for par, frecuencia in patrones.most_common(5):
        print(f"  {par[0]} + {par[1]} → {frecuencia} veces")
    
    print("\n✅ Paso 1 completo.")
    print("El sistema ya maneja lenguaje básico.")
    print("Siguiente: Paso 2 — predicción de secuencias.\n")
