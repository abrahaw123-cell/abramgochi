"""
ABRAMGOCHI — Paso 3: Texto Real y Compresión
=============================================
El sistema ahora aprende de texto real.
La red relacional comprime lenguaje natural —
exactamente lo que evalúa el concurso Parameter Golf.

Métrica objetivo: bits por byte (menor = mejor)

Author: Abraham
Framework: H.A.S. | Genoma Cognitivo
Date: March 2026
"""

import random
import math
import re
import networkx as nx
from collections import defaultdict, Counter

# =====================
# 📖 TOKENIZADOR SIMPLE
# =====================
def tokenizar(texto):
    """
    Convierte texto en tokens (palabras limpias).
    Simple pero efectivo — sin dependencias externas.
    
    Paso futuro: tokenizador BPE para mayor compresión.
    """
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)
    tokens = texto.split()
    return [t for t in tokens if len(t) > 1]


# =====================
# 🧠 MEMORIA RELACIONAL MEJORADA
# =====================
class MemoriaRelacional:
    """
    Memoria de transiciones entre tokens.
    Aprende: dado token A, ¿cuál es el siguiente más probable?
    
    Kohn-Sham:
        La distribución de probabilidad ES la densidad ρ(r).
        No observamos la intención del texto — solo su densidad.
    """
    
    def __init__(self, contexto=2):
        self.contexto = contexto  # cuántas palabras anteriores considera
        self.siguiente = defaultdict(Counter)
        self.total_tokens = 0
    
    def aprender_texto(self, tokens):
        """Aprende todas las transiciones en un texto."""
        self.total_tokens += len(tokens)
        
        for i in range(len(tokens) - self.contexto):
            # Contexto = ventana de palabras anteriores
            clave = tuple(tokens[i:i + self.contexto])
            siguiente = tokens[i + self.contexto]
            self.siguiente[clave][siguiente] += 1
    
    def predecir(self, contexto_actual):
        """Predice siguiente token dado el contexto."""
        clave = tuple(contexto_actual[-self.contexto:])
        
        if clave not in self.siguiente:
            # Fallback: busca contexto más corto
            clave_corta = (contexto_actual[-1],)
            if clave_corta in self.siguiente:
                opciones = self.siguiente[clave_corta]
            else:
                return None
        else:
            opciones = self.siguiente[clave]
        
        total = sum(opciones.values())
        r = random.uniform(0, total)
        acumulado = 0
        for token, conteo in opciones.items():
            acumulado += conteo
            if r <= acumulado:
                return token
        return None
    
    def probabilidad(self, contexto_actual, siguiente_token):
        """P(siguiente | contexto) — para calcular bits por byte."""
        clave = tuple(contexto_actual[-self.contexto:])
        
        if clave not in self.siguiente:
            return 1 / 10000  # probabilidad mínima
        
        opciones = self.siguiente[clave]
        total = sum(opciones.values())
        conteo = opciones.get(siguiente_token, 0)
        
        # Suavizado de Laplace — evita probabilidad cero
        return (conteo + 1) / (total + len(opciones) + 1)


# =====================
# 🌐 RED RELACIONAL
# =====================
def crear_red_texto(n=8, p=0.6, contexto=2):
    """
    Cada nodo tiene su propia memoria.
    Diferentes nodos aprenden de diferentes partes del texto —
    la red distribuye el aprendizaje.
    """
    G = nx.erdos_renyi_graph(n=n, p=p)
    memorias = {nodo: MemoriaRelacional(contexto=contexto) 
                for nodo in G.nodes()}
    return G, memorias


def distribuir_aprendizaje(G, memorias, tokens):
    """
    Distribuye el texto entre los nodos de la red.
    Cada nodo aprende una porción — luego comparten.
    
    Esto es el V_eff relacional: el conocimiento colectivo
    condiciona a cada nodo individual.
    """
    n = len(G.nodes())
    chunk_size = max(1, len(tokens) // n)
    
    for i, nodo in enumerate(G.nodes()):
        inicio = i * chunk_size
        fin = inicio + chunk_size if i < n - 1 else len(tokens)
        chunk = tokens[inicio:fin]
        memorias[nodo].aprender_texto(chunk)
    
    return memorias


def compartir_conocimiento(G, memorias):
    """
    Los nodos comparten lo que aprendieron con sus vecinos.
    La red propaga el conocimiento relacionalmente.
    
    hijo = mezcla(padre1, padre2) — herencia cognitiva.
    """
    memorias_nuevas = {nodo: MemoriaRelacional(contexto=2) 
                       for nodo in G.nodes()}
    
    for nodo in G.nodes():
        vecinos = list(G.neighbors(nodo))
        fuentes = [nodo] + vecinos
        
        # Combina conocimiento propio + vecinos
        for fuente in fuentes:
            for clave, siguientes in memorias[fuente].siguiente.items():
                for token, conteo in siguientes.items():
                    memorias_nuevas[nodo].siguiente[clave][token] += conteo
    
    return memorias_nuevas


# =====================
# 📐 MEMORIA COLECTIVA
# =====================
def memoria_colectiva(memorias):
    """Fusiona todas las memorias en una sola."""
    colectiva = MemoriaRelacional(contexto=2)
    for memoria in memorias.values():
        for clave, siguientes in memoria.siguiente.items():
            for token, conteo in siguientes.items():
                colectiva.siguiente[clave][token] += conteo
    return colectiva


# =====================
# 📊 BITS POR BYTE
# =====================
def calcular_bits_por_byte(memoria, tokens_validacion):
    """
    Métrica del concurso Parameter Golf.
    Mide qué tan bien el modelo comprime texto no visto.
    
    bits_por_byte = promedio de -log2(P(token|contexto)) / bytes_por_token
    
    Objetivo: lo más bajo posible.
    Un modelo aleatorio = ~13 bits/byte
    GPT-2 pequeño = ~3-4 bits/byte
    """
    log_prob_total = 0
    n_tokens = 0
    bytes_total = 0
    
    contexto_actual = []
    
    for token in tokens_validacion:
        if len(contexto_actual) >= 2:
            prob = memoria.probabilidad(contexto_actual, token)
            log_prob_total += math.log2(prob)
            n_tokens += 1
            bytes_total += len(token.encode('utf-8'))
        
        contexto_actual.append(token)
        if len(contexto_actual) > 2:
            contexto_actual.pop(0)
    
    if bytes_total == 0:
        return float('inf')
    
    bits_por_byte = -log_prob_total / bytes_total
    return bits_por_byte


# =====================
# ✍️ GENERACIÓN DE TEXTO
# =====================
def generar(memoria, inicio=None, longitud=20):
    """Genera texto usando la memoria colectiva."""
    if inicio is None:
        claves = list(memoria.siguiente.keys())
        if not claves:
            return []
        inicio = list(random.choice(claves))
    
    generado = list(inicio)
    contexto = list(inicio)
    
    for _ in range(longitud):
        siguiente = memoria.predecir(contexto)
        if siguiente is None:
            break
        generado.append(siguiente)
        contexto.append(siguiente)
        if len(contexto) > 2:
            contexto.pop(0)
    
    return generado


# =====================
# 🚀 EJECUCIÓN
# =====================
if __name__ == "__main__":
    
    print("\n" + "="*58)
    print("  ABRAMGOCHI — Paso 3: Texto Real y Compresión")
    print("  La red aprende de lenguaje natural")
    print("="*58 + "\n")

    # Texto de entrenamiento real
    # (En producción: reemplazar con dataset FineWeb)
    TEXTO_ENTRENAMIENTO = """
    Los sistemas complejos emergen de la interacción entre agentes simples.
    Cada agente en la red observa a sus vecinos y adapta su comportamiento.
    La inteligencia colectiva surge de las relaciones, no de los individuos.
    El campo relacional condiciona a cada agente dentro del sistema.
    La densidad del comportamiento es lo único observable desde afuera.
    Los patrones emergen sin que nadie los programe explícitamente.
    La evolución selecciona las estructuras más eficientes para comprimir información.
    El aprendizaje distribuido permite que la red procese más que cualquier nodo solo.
    La adaptación al entorno es el mecanismo fundamental de la inteligencia.
    Los sistemas relacionales superan a los sistemas centralizados en robustez.
    La herencia cognitiva transmite patrones aprendidos a nuevas generaciones.
    El comportamiento emergente no puede predecirse desde las partes individuales.
    La red distribuye el conocimiento y lo hace resiliente ante perturbaciones.
    Cada conexión entre agentes es una oportunidad de transferencia de información.
    El sistema aprende colectivamente lo que ningún agente podría aprender solo.
    La compresión eficiente del lenguaje revela la estructura profunda del pensamiento.
    Los modelos relacionales capturan dependencias que los modelos lineales pierden.
    La anticipación estratégica requiere observar densidades, no intenciones ocultas.
    El entorno efectivo moldea el comportamiento de cada agente en la red.
    La evolución genética optimiza la arquitectura sin necesidad de gradientes.
    """

    TEXTO_VALIDACION = """
    Los agentes relacionales aprenden de sus vecinos en la red.
    El sistema emergente supera la suma de sus partes individuales.
    La densidad observable es la única medida válida del comportamiento.
    La evolución selecciona las arquitecturas más eficientes.
    El aprendizaje distribuido es más robusto que el centralizado.
    """

    # Tokenizar
    tokens_train = tokenizar(TEXTO_ENTRENAMIENTO)
    tokens_val = tokenizar(TEXTO_VALIDACION)
    
    print(f"Tokens de entrenamiento: {len(tokens_train)}")
    print(f"Tokens de validación:    {len(tokens_val)}")
    print(f"Vocabulario único:       {len(set(tokens_train))}\n")

    # Crear red
    G, memorias = crear_red_texto(n=8, p=0.6, contexto=2)
    print(f"Red: {len(G.nodes())} agentes | {len(G.edges())} conexiones\n")

    # Aprendizaje distribuido
    print("📡 Distribuyendo aprendizaje por la red...")
    memorias = distribuir_aprendizaje(G, memorias, tokens_train)

    # Compartir conocimiento entre vecinos
    print("🔄 Compartiendo conocimiento entre nodos vecinos...")
    for ciclo in range(3):
        memorias = compartir_conocimiento(G, memorias)
        print(f"   Ciclo {ciclo+1} completado")

    # Memoria colectiva
    mem_col = memoria_colectiva(memorias)
    print(f"\n✅ Memoria colectiva: {len(mem_col.siguiente)} patrones aprendidos\n")

    # Generar texto
    print("✍️  Texto generado por ABRAMGOCHI:\n")
    for i in range(3):
        claves = list(mem_col.siguiente.keys())
        inicio = list(random.choice(claves))
        texto = generar(mem_col, inicio=inicio, longitud=15)
        print(f"  [{i+1}] {' '.join(texto)}")

    # Bits por byte — métrica del concurso
    print("\n📐 Evaluación de compresión:\n")
    bpb = calcular_bits_por_byte(mem_col, tokens_val)
    print(f"  Bits por byte: {bpb:.3f}")
    print(f"  Referencia — modelo aleatorio: ~13.0 bpb")
    print(f"  Referencia — GPT-2 pequeño:    ~3.5 bpb")
    print(f"  ABRAMGOCHI actual:             {bpb:.3f} bpb")
    
    mejora = ((13.0 - bpb) / 13.0) * 100
    print(f"\n  Mejora vs aleatorio: {mejora:.1f}%")

    print("\n✅ Paso 3 completo.")
    print("ABRAMGOCHI ya comprime texto real y mide bits por byte.")
    print("Siguiente: conectar a FineWeb y optimizar arquitectura.\n")
