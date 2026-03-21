"""
ABRAMGOCHI — Sistema Completo
==============================
Adaptive Behavioral Relational Agent Model with
Genetic Optimization and Cognitive Hereditary Intelligence

Version: 1.0
Author: Abraham
Framework: H.A.S. (Human Anticipation Strategist)
Project: Genoma Cognitivo
Date: March 2026

OpenAI Model Craft Challenge — Parameter Golf
Target: minimize bits per byte on FineWeb validation set
Constraint: model fits in 16 MB, trains in <10 min on 8xH100

Theoretical foundation — Kohn-Sham equation (DFT):
    [-½∇² + V_eff(r)] φᵢ(r) = εᵢ φᵢ(r)

    ∇²       → internal cognitive tension of each agent
    V_eff(r) → relational network field (effective environment)
    φᵢ(r)   → latent behavioral pattern (unobservable)
    εᵢ       → stable behavioral energy level
    ρ(r)     → observable output = |φᵢ(r)|²
"""

import random
import math
import re
import os
import hashlib
import datetime
import networkx as nx
from collections import defaultdict, Counter

# =========================================================
# 🔐 AUTENTICACIÓN Y LOGS
# =========================================================

USUARIOS = {
    "admin":  {"password": "1234", "rol": "admin"},
    "viewer": {"password": "0000", "rol": "viewer"}
}

def login():
    user = input("Usuario: ")
    pwd  = input("Password: ")
    if user in USUARIOS and USUARIOS[user]["password"] == pwd:
        print(f"✅ Acceso como '{USUARIOS[user]['rol']}'")
        return user, USUARIOS[user]["rol"]
    print("❌ Acceso denegado")
    return None, None

def log(user, accion):
    os.makedirs("logs", exist_ok=True)
    with open("logs/abramgochi.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {user} | {accion}\n")

def hash_estado(estado):
    return hashlib.sha256(str(sorted(estado.items())).encode()).hexdigest()


# =========================================================
# 📖 TOKENIZADOR
# =========================================================

def tokenizar(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ\s']", ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return [t for t in texto.split() if 2 <= len(t) <= 20]


# =========================================================
# 🧠 MEMORIA RELACIONAL
# =========================================================

class MemoriaRelacional:
    """
    Aprende transiciones entre tokens.
    La distribución de probabilidad emergente ES la densidad ρ(r).
    Nunca observamos la intención — solo la densidad.
    """

    def __init__(self, contexto=2):
        self.contexto  = contexto
        self.siguiente = defaultdict(Counter)

    def aprender(self, tokens):
        for i in range(len(tokens) - self.contexto):
            clave = tuple(tokens[i : i + self.contexto])
            self.siguiente[clave][tokens[i + self.contexto]] += 1

    def predecir(self, ctx):
        for n in range(self.contexto, 0, -1):
            clave = tuple(ctx[-n:])
            if clave in self.siguiente:
                ops   = self.siguiente[clave]
                total = sum(ops.values())
                r, ac = random.uniform(0, total), 0
                for tok, cnt in ops.items():
                    ac += cnt
                    if r <= ac:
                        return tok
        return None

    def prob(self, ctx, sig):
        for n in range(self.contexto, 0, -1):
            clave = tuple(ctx[-n:])
            if clave in self.siguiente:
                ops   = self.siguiente[clave]
                total = sum(ops.values())
                return (ops.get(sig, 0) + 1) / (total + len(ops) + 1)
        return 1e-6

    def fusionar(self, otra):
        for clave, sigs in otra.siguiente.items():
            for tok, cnt in sigs.items():
                self.siguiente[clave][tok] += cnt

    def n_patrones(self):
        return sum(len(v) for v in self.siguiente.values())


# =========================================================
# 📐 FUNCIÓN DE DIFICULTAD
# =========================================================

def calcular_dificultad(base, nivel, factor, entorno):
    """
    dificultad = base + (nivel * factor) + entorno
    Mapa directo a Kohn-Sham:
        base           → energía cinética inicial (∇²)
        nivel * factor → curva de desarrollo interno
        entorno        → potencial efectivo V_eff(r)
    """
    return base + (nivel * factor) + entorno


# =========================================================
# 🧬 EVOLUCIÓN GENÉTICA
# =========================================================

def seleccionar_mejores(poblacion, n=4):
    return sorted(poblacion, key=lambda x: x.get('fitness', 0), reverse=True)[:n]

def reproducir(p1, p2):
    """hijo = mezcla(padre1, padre2) + mutación — reproducción sexual"""
    hijo = {k: random.choice([p1[k], p2[k]]) for k in p1}
    return mutar(hijo)

def clonar(padre):
    """hijo = copia(padre) + mutación — reproducción asexual"""
    return mutar(padre.copy())

def mutar(agente, tasa=0.1):
    return {
        k: (v + random.uniform(-5, 5) if isinstance(v, (int, float)) and random.random() < tasa else v)
        for k, v in agente.items()
    }

def nueva_generacion(poblacion):
    """nueva_generación = seleccionar(mejores) + reproducir + mutar"""
    mejores = seleccionar_mejores(poblacion)
    nueva   = mejores.copy()
    while len(nueva) < len(poblacion):
        p1, p2 = random.sample(mejores, 2)
        hijo = reproducir(p1, p2) if random.random() > 0.5 else clonar(random.choice(mejores))
        nueva.append(hijo)
    return nueva


# =========================================================
# 🌐 RED ABRAMGOCHI
# =========================================================

class RedABRAMGOCHI:
    """
    Red relacional completa:
    - Aprendizaje distribuido por nodos
    - Compartición de conocimiento entre vecinos
    - Evolución genética de la arquitectura
    - Evaluación de bits por byte (métrica Parameter Golf)
    """

    def __init__(self, n_nodos=8, p_conexion=0.6, contexto=2):
        self.G         = nx.erdos_renyi_graph(n=n_nodos, p=p_conexion)
        self.contexto  = contexto
        self.memorias  = {n: MemoriaRelacional(contexto) for n in self.G.nodes()}
        self.estado    = {n: random.randint(40, 60) for n in self.G.nodes()}
        self.hash_orig = hash_estado(self.estado)
        print(f"🌐 Red: {n_nodos} agentes | {len(self.G.edges())} conexiones")

    # --- Integridad ---
    def verificar_integridad(self):
        return hash_estado(self.estado) == self.hash_orig

    # --- Actualizar estado numérico (comportamiento adaptativo) ---
    def actualizar_estado(self):
        nuevo = {}
        for nodo in self.G.nodes():
            vecinos = list(self.G.neighbors(nodo))
            promedio = (sum(self.estado[v] for v in vecinos) / len(vecinos)
                        if vecinos else self.estado[nodo])
            influencia = 0.1 if promedio < 50 else 0.3
            nuevo[nodo] = max(0, min(100,
                self.estado[nodo] + influencia * (promedio - self.estado[nodo])
                + random.uniform(-2, 2)
            ))
        self.estado = nuevo

    # --- Entrenamiento de lenguaje ---
    def entrenar(self, textos, ciclos=3):
        n     = len(self.G.nodes())
        chunk = max(1, len(textos) // n)
        print(f"\n📡 Distribuyendo {len(textos)} textos entre {n} agentes...")

        for i, nodo in enumerate(self.G.nodes()):
            for texto in textos[i * chunk : (i + 1) * chunk if i < n - 1 else len(textos)]:
                tokens = tokenizar(texto)
                if tokens:
                    self.memorias[nodo].aprender(tokens)

        print(f"🔄 Compartiendo conocimiento ({ciclos} ciclos)...")
        for c in range(ciclos):
            nuevas = {nodo: MemoriaRelacional(self.contexto) for nodo in self.G.nodes()}
            for nodo in self.G.nodes():
                nuevas[nodo].fusionar(self.memorias[nodo])
                for vecino in self.G.neighbors(nodo):
                    nuevas[nodo].fusionar(self.memorias[vecino])
            self.memorias = nuevas
            total = sum(m.n_patrones() for m in self.memorias.values())
            print(f"   Ciclo {c+1}: {total:,} patrones en la red")

    # --- Memoria colectiva ---
    def memoria_colectiva(self):
        col = MemoriaRelacional(self.contexto)
        for m in self.memorias.values():
            col.fusionar(m)
        return col

    # --- Bits por byte (métrica oficial) ---
    def evaluar_bpb(self, textos_val):
        mem = self.memoria_colectiva()
        log_p, bytes_t = 0, 0
        for texto in textos_val:
            tokens = tokenizar(texto)
            ctx    = []
            for tok in tokens:
                if len(ctx) >= self.contexto:
                    log_p  += math.log2(mem.prob(ctx, tok))
                    bytes_t += len(tok.encode('utf-8'))
                ctx.append(tok)
                if len(ctx) > self.contexto:
                    ctx.pop(0)
        return -log_p / bytes_t if bytes_t > 0 else float('inf')

    # --- Generación de texto ---
    def generar(self, longitud=20):
        mem    = self.memoria_colectiva()
        claves = list(mem.siguiente.keys())
        if not claves:
            return ""
        ctx = list(random.choice(claves))
        out = ctx.copy()
        for _ in range(longitud):
            sig = mem.predecir(ctx)
            if sig is None:
                break
            out.append(sig)
            ctx.append(sig)
            if len(ctx) > self.contexto:
                ctx.pop(0)
        return ' '.join(out)

    # --- Tamaño del modelo ---
    def tamano_bytes(self):
        mem = self.memoria_colectiva()
        return mem.n_patrones() * 50

    # --- Dificultad adaptativa ---
    def dificultad_actual(self, paso):
        entorno = sum(self.estado.values()) / len(self.estado)
        return calcular_dificultad(base=50, nivel=paso+1, factor=2.5, entorno=entorno)


# =========================================================
# 🚀 EJECUCIÓN PRINCIPAL
# =========================================================

TEXTOS_DEMO = [
    "The history of artificial intelligence began when researchers explored machines that could think and reason.",
    "Climate change represents one of the most significant challenges facing humanity in the modern era.",
    "The human brain contains billions of neurons connected through synapses giving rise to consciousness.",
    "Quantum computing leverages principles of quantum mechanics to process information in fundamentally new ways.",
    "Language is the primary tool through which humans transmit culture knowledge and identity across generations.",
    "Evolutionary biology demonstrates that all living organisms share common ancestors through natural selection.",
    "The development of the internet has fundamentally altered how humans communicate and access information.",
    "Mathematical structures underlie the physical laws governing the universe from quantum fields to relativity.",
    "Social systems emerge from interactions of individuals following simple rules producing complex behavior.",
    "Cognitive science investigates the nature of mind and intelligence across biological and artificial systems.",
    "Los sistemas complejos emergen de la interacción entre agentes simples dentro de redes relacionales.",
    "Cada agente observa a sus vecinos y adapta su comportamiento según el entorno efectivo que lo rodea.",
    "La inteligencia colectiva surge de las relaciones entre agentes no de las capacidades individuales.",
    "La densidad del comportamiento es lo único observable desde afuera de un sistema complejo.",
    "Los patrones emergen sin que nadie los programe explícitamente en el sistema relacional.",
    "La evolución selecciona las estructuras más eficientes para comprimir y transmitir información.",
    "El aprendizaje distribuido permite que la red procese más que cualquier nodo individual.",
    "La adaptación al entorno es el mecanismo fundamental de la inteligencia emergente.",
    "La herencia cognitiva transmite patrones aprendidos a nuevas generaciones del sistema.",
    "El comportamiento emergente no puede predecirse desde el análisis de las partes individuales.",
] * 8


if __name__ == "__main__":

    print("\n" + "="*58)
    print("  ABRAMGOCHI v1.0 — Sistema Completo")
    print("  H.A.S. Framework | Genoma Cognitivo")
    print("  OpenAI Model Craft Challenge — Parameter Golf")
    print("="*58 + "\n")

    # Autenticación
    user, rol = login()
    if not user:
        exit()

    log(user, "sistema iniciado")

    # Integridad
    red = RedABRAMGOCHI(n_nodos=8, p_conexion=0.6, contexto=2)

    if red.verificar_integridad():
        print("🔒 Integridad verificada ✅")
    else:
        print("⚠️  Alerta de integridad")
        log(user, "alerta de integridad")

    if rol == "admin":

        # Fase 1 — Comportamiento adaptativo
        print("\n─── Fase 1: Comportamiento Adaptativo ───")
        for paso in range(5):
            red.actualizar_estado()
            dif = red.dificultad_actual(paso)
            avg = sum(red.estado.values()) / len(red.estado)
            print(f"  Paso {paso+1} | Dificultad: {dif:.2f} | Estado medio: {avg:.2f}")

        log(user, "simulación de comportamiento ejecutada")

        # Fase 2 — Entrenamiento de lenguaje
        print("\n─── Fase 2: Entrenamiento de Lenguaje ───")
        split = int(len(TEXTOS_DEMO) * 0.8)
        train = TEXTOS_DEMO[:split]
        val   = TEXTOS_DEMO[split:]

        red.entrenar(train, ciclos=3)
        log(user, f"entrenamiento completado — {len(train)} textos")

        # Fase 3 — Evaluación
        print("\n─── Fase 3: Evaluación Parameter Golf ───")
        bpb    = red.evaluar_bpb(val)
        tamano = red.tamano_bytes()

        print(f"\n  Bits por byte:        {bpb:.3f} bpb")
        print(f"  Tamaño del modelo:    {tamano/1024:.1f} KB / 16,000 KB")
        print(f"  Uso del límite:       {tamano/1024/16000*100:.2f}%")
        print(f"\n  Referencia aleatoria: ~13.0 bpb")
        print(f"  Referencia GPT-2:     ~3.5  bpb")
        print(f"  ABRAMGOCHI:           {bpb:.3f} bpb")

        log(user, f"evaluación completada — {bpb:.3f} bpb")

        # Fase 4 — Generación
        print("\n─── Fase 4: Generación de Texto ───\n")
        for i in range(3):
            print(f"  [{i+1}] {red.generar(longitud=15)}\n")

        # Evolución genética de la población
        print("─── Fase 5: Evolución Genética ───")
        poblacion = [
            {'fitness': random.uniform(0, 1), 'conexiones': random.randint(3, 8)}
            for _ in range(8)
        ]
        for gen in range(3):
            poblacion = nueva_generacion(poblacion)
            mejor = max(poblacion, key=lambda x: x.get('fitness', 0))
            print(f"  Generación {gen+1} | Mejor fitness: {mejor['fitness']:.3f}")

        log(user, "evolución genética completada")

        print("\n✅ ABRAMGOCHI completado exitosamente.")
        print("   Sistema listo para GitHub y Parameter Golf.\n")

    elif rol == "viewer":
        print("\n👀 Modo solo lectura")
        print(f"Estado actual de la red: {red.estado}")
        log(user, "estado visualizado")
