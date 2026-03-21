"""
ABRAMGOCHI — Paso 2: Predicción de Secuencias
===============================================
Los agentes ahora aprenden qué palabras vienen después de otras.
La red relacional se convierte en un modelo de predicción.

Principio Kohn-Sham aplicado:
    La densidad ρ(r) = probabilidad de la siguiente palabra
    No observamos la intención — solo la distribución emergente.

Author: Abraham
Framework: H.A.S. | Genoma Cognitivo
Date: March 2026
"""

import random
import networkx as nx
from collections import defaultdict, Counter

# =====================
# 📖 VOCABULARIO
# =====================
VOCABULARIO = [
    "agente", "red", "mente", "campo", "nodo",
    "energía", "patrón", "densidad", "relación", "sistema",
    "emergente", "adaptación", "evolución", "conexión", "flujo"
]

# =====================
# 🧠 MEMORIA DE SECUENCIAS
# =====================
class MemoriaRelacional:
    """
    Cada agente aprende qué palabras tienden a seguir a otras.
    
    Es como un cerebro mínimo:
        "después de 'agente' → suele venir 'red' o 'mente'"
    
    Esto es la base de cualquier modelo de lenguaje.
    """
    
    def __init__(self):
        # Para cada palabra, cuenta qué palabras la siguen
        self.siguiente = defaultdict(Counter)
    
    def aprender(self, secuencia):
        """Aprende de una secuencia de palabras."""
        for i in range(len(secuencia) - 1):
            actual = secuencia[i]
            siguiente = secuencia[i + 1]
            self.siguiente[actual][siguiente] += 1
    
    def predecir(self, palabra_actual):
        """
        Predice la siguiente palabra más probable.
        
        Densidad = distribución de probabilidad sobre el vocabulario.
        Solo lo que emerge de las relaciones aprendidas.
        """
        if palabra_actual not in self.siguiente:
            return random.choice(VOCABULARIO)
        
        opciones = self.siguiente[palabra_actual]
        total = sum(opciones.values())
        
        # Muestreo probabilístico — no siempre la más común
        # (permite creatividad, evita colapso a una sola respuesta)
        r = random.uniform(0, total)
        acumulado = 0
        for palabra, conteo in opciones.items():
            acumulado += conteo
            if r <= acumulado:
                return palabra
        
        return random.choice(VOCABULARIO)
    
    def distribucion(self, palabra_actual):
        """Muestra la distribución de probabilidad completa."""
        if palabra_actual not in self.siguiente:
            return {}
        opciones = self.siguiente[palabra_actual]
        total = sum(opciones.values())
        return {p: round(c/total, 3) for p, c in opciones.most_common()}


# =====================
# 🌐 RED RELACIONAL CON MEMORIA
# =====================
def crear_red_predictiva(n=8, p=0.5):
    """Cada nodo tiene su propia memoria de secuencias."""
    G = nx.erdos_renyi_graph(n=n, p=p)
    memorias = {nodo: MemoriaRelacional() for nodo in G.nodes()}
    estado = {nodo: random.choice(VOCABULARIO) for nodo in G.nodes()}
    return G, estado, memorias


# =====================
# 📡 INTERCAMBIO Y APRENDIZAJE
# =====================
def intercambiar_y_aprender(G, estado, memorias):
    """
    Cada agente:
    1. Observa la secuencia [su palabra → palabra del vecino]
    2. Aprende esa transición
    3. Predice su próxima palabra basándose en lo aprendido
    """
    nuevo_estado = {}
    
    for nodo in G.nodes():
        vecinos = list(G.neighbors(nodo))
        
        if vecinos:
            # Aprende de cada vecino
            for vecino in vecinos:
                secuencia = [estado[nodo], estado[vecino]]
                memorias[nodo].aprender(secuencia)
            
            # Predice su siguiente palabra
            nuevo_estado[nodo] = memorias[nodo].predecir(estado[nodo])
        else:
            nuevo_estado[nodo] = estado[nodo]
    
    return nuevo_estado, memorias


# =====================
# ✍️ GENERACIÓN DE TEXTO
# =====================
def generar_texto(memorias, inicio=None, longitud=10):
    """
    Genera una secuencia de texto usando las memorias colectivas.
    
    Combina las memorias de todos los agentes —
    la densidad colectiva de la red produce el texto.
    
    Equivalente a ρ(r) = |φᵢ(r)|² acumulado de toda la red.
    """
    # Combina todas las memorias en una sola
    memoria_colectiva = MemoriaRelacional()
    for memoria in memorias.values():
        for palabra, siguientes in memoria.siguiente.items():
            for siguiente, conteo in siguientes.items():
                memoria_colectiva.siguiente[palabra][siguiente] += conteo
    
    # Genera texto
    if inicio is None:
        inicio = random.choice(VOCABULARIO)
    
    texto = [inicio]
    palabra_actual = inicio
    
    for _ in range(longitud - 1):
        siguiente = memoria_colectiva.predecir(palabra_actual)
        texto.append(siguiente)
        palabra_actual = siguiente
    
    return texto, memoria_colectiva


# =====================
# 📐 COMPRESIÓN (bits por símbolo)
# =====================
def calcular_entropia(memoria_colectiva):
    """
    Mide qué tan bien comprime el sistema el lenguaje.
    Menor entropía = mejor compresión = modelo más eficiente.
    
    Esto es lo que mide el concurso Parameter Golf:
    bits por byte sobre el conjunto de validación.
    """
    import math
    
    entropias = []
    for palabra, siguientes in memoria_colectiva.siguiente.items():
        total = sum(siguientes.values())
        entropia = 0
        for conteo in siguientes.values():
            p = conteo / total
            if p > 0:
                entropia -= p * math.log2(p)
        entropias.append(entropia)
    
    return sum(entropias) / len(entropias) if entropias else 0


# =====================
# 🚀 EJECUCIÓN
# =====================
if __name__ == "__main__":
    
    print("\n" + "="*55)
    print("  ABRAMGOCHI — Paso 2: Predicción de Secuencias")
    print("  La red aprende qué palabras vienen después")
    print("="*55 + "\n")
    
    # Crear red con memoria
    G, estado, memorias = crear_red_predictiva(n=8, p=0.5)
    
    print(f"Red creada: {len(G.nodes())} agentes, {len(G.edges())} conexiones\n")
    print("Estado inicial:", list(estado.values()))
    
    # Fase de aprendizaje
    print("\n📡 Fase de aprendizaje — intercambio relacional...\n")
    
    for paso in range(10):
        estado, memorias = intercambiar_y_aprender(G, estado, memorias)
        
        if paso % 3 == 0:
            dominante = Counter(estado.values()).most_common(1)[0]
            print(f"Paso {paso+1}: dominante='{dominante[0]}' | "
                  f"estado={list(estado.values())}")
    
    # Generar texto
    print("\n✍️  Generando texto desde la memoria colectiva...\n")
    
    for i in range(3):
        inicio = random.choice(VOCABULARIO)
        texto, memoria_colectiva = generar_texto(memorias, inicio=inicio, longitud=8)
        print(f"  Secuencia {i+1}: {' → '.join(texto)}")
    
    # Distribución de probabilidad
    print("\n📊 Distribución aprendida para 'agente':")
    _, mem_col = generar_texto(memorias, longitud=1)
    dist = mem_col.distribucion("agente")
    if dist:
        for palabra, prob in list(dist.items())[:5]:
            barra = "█" * int(prob * 30)
            print(f"  '{palabra}': {barra} {prob}")
    else:
        print("  (aún sin datos suficientes para 'agente')")
    
    # Entropía / compresión
    entropia = calcular_entropia(mem_col)
    print(f"\n📐 Entropía del modelo: {entropia:.3f} bits/símbolo")
    print(f"   (menor = mejor compresión)")
    
    print("\n✅ Paso 2 completo.")
    print("El sistema ya predice secuencias de lenguaje.")
    print("Siguiente: Paso 3 — comprimir texto real.\n")
