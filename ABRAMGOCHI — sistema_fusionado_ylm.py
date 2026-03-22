ABRAMGOCHI — sistema_fusionado_ylm.py
H.A.S. Framework | Genoma Cognitivo | Abraham 2026
import random
import math
import networkx as nx
# =========================================================
# ■ UTILIDADES
# =========================================================
def dot(a, b):
 return a[0]*b[0] + a[1]*b[1]
def normalizar(v):
 mag = math.sqrt(v[0]**2 + v[1]**2) # CORREGIDO: ** no *
 return (v[0]/mag, v[1]/mag) if mag != 0 else (0,0)
# =========================================================
# ■■ CAMPO KOHN-SHAM (SIMPLIFICADO)
# =========================================================
class KohnShamField:
 def curvatura(self, estado):
 return abs(estado - 50) / 50
 def v_eff(self, vecinos):
 return sum(vecinos)/len(vecinos)/100 if vecinos else 0.5
 def funcion_onda(self, estado, v_eff):
 return estado * (1 - v_eff) + random.gauss(0, 1)
 def eigenvalor(self, curvatura, v_eff):
 return -0.5 * curvatura + v_eff
 def densidad(self, phi):
 return phi**2
 def colapsar(self, estado, vecinos):
 k = self.curvatura(estado)
 ve = self.v_eff(vecinos)
 phi = self.funcion_onda(estado, ve)
 e = self.eigenvalor(k, ve)
 rho = self.densidad(phi)
 return {"phi": phi, "epsilon": e, "rho": rho}
# =========================================================
# ■ MOLÉCULA CON DIRECCIÓN (Ylm SIMPLIFICADO)
# =========================================================
class Molecula:
 def __init__(self, i): # CORREGIDO: __init__
 self.id = i
 self.energia = random.uniform(40, 60)
 self.carga = random.uniform(0, 1)
 self.campo = KohnShamField()
 # Dirección tipo Ylm
 ang = 2 * math.pi * i / 10
 self.direccion = (math.cos(ang), math.sin(ang))
 self.historial = []
 def colapsar(self, vecinos):
 res = self.campo.colapsar(self.energia, vecinos)
 self.historial.append(res)
 return res
 def transferir(self, siguiente):
 if not self.historial:
 return 0
 rho = self.historial[-1]["rho"]
 base = min(0.3, rho * 0.001 * random.uniform(0.8, 1.2))
 # Alineación tipo Ylm
 alineacion = max(0, dot(self.direccion, siguiente.direccion))
 transferencia = base * alineacion
 # Aplicar relevo
 siguiente.carga = min(1.0, siguiente.carga + transferencia)
 siguiente.energia = min(100, siguiente.energia + transferencia * 0.1)
 # Evolución geométrica de dirección
 dx = self.direccion[0] + random.uniform(-0.05, 0.05)
 dy = self.direccion[1] + random.uniform(-0.05, 0.05)
 self.direccion = normalizar((dx, dy))
 return transferencia
# =========================================================
# ■ CADENA DE RELEVO
# =========================================================
class Cadena:
 def __init__(self, n=8): # CORREGIDO: __init__
 self.moleculas = [Molecula(i) for i in range(n)]
 def paso(self):
 energia_total = 0
 for i, m in enumerate(self.moleculas[:-1]):
 vecinos = [x.energia for x in self.moleculas
 if abs(x.id - m.id) == 1]
 m.colapsar(vecinos)
 m.transferir(self.moleculas[i+1])
 energia_total += m.energia
 return energia_total / len(self.moleculas)
# =========================================================
# ■ RED ABRAMGOCHI
# =========================================================
class Red:
 def __init__(self, n=8): # CORREGIDO: __init__
 self.G = nx.erdos_renyi_graph(n, 0.6)
 self.estado = {node: random.uniform(40, 60) for node in self.G.nodes()}
 self.campo = KohnShamField()
 def actualizar(self):
 nuevo = {}
 densidades = {}
 for nodo in self.G.nodes():
 vecinos = [self.estado[v] for v in self.G.neighbors(nodo)]
 res = self.campo.colapsar(self.estado[nodo], vecinos)
 nuevo[nodo] = max(0, min(100,
 self.estado[nodo] + (res["rho"] * 0.01)
 ))
 densidades[nodo] = res["rho"]
 self.estado = nuevo
 return densidades
 def fitness(self):
 return sum(self.estado.values()) / len(self.estado) / 100
# =========================================================
# ■ SISTEMA FUSIONADO
# =========================================================
class Sistema:
 def __init__(self): # CORREGIDO: __init__
 self.red = Red()
 self.cadena = Cadena()
 def ciclo(self):
 densidades = self.red.actualizar()
 fitness = self.red.fitness()
 # Acoplamiento red → moléculas
 nodos = list(densidades.keys())
 for i, m in enumerate(self.cadena.moleculas):
 m.energia = 40 + densidades[nodos[i % len(nodos)]] * 0.1
 energia = self.cadena.paso()
 return fitness, energia
# =========================================================
# ■ EJECUCIÓN
# =========================================================
if __name__ == "__main__": # CORREGIDO: __name__ y __main__
 sistema = Sistema()
 print("\n" + "="*50)
 print(" ■ Sistema ABRAMGOCHI + Relevo + Ylm activo")
 print(" H.A.S. Framework | Genoma Cognitivo | Abraham")
 print("="*50 + "\n")
 fitness_hist = []
 energia_hist = []
 for i in range(20):
 f, e = sistema.ciclo()
 fitness_hist.append(f)
 energia_hist.append(e)
 print(f" Paso {i+1:2d} | Fitness: {f:.3f} | Energía: {e:.2f}")
 print(f"\n Fitness final: {fitness_hist[-1]:.4f}")
 print(f" Energía final: {energia_hist[-1]:.2f}")
 print(f" Tendencia: {'↑ subiendo' if energia_hist[-1] > energia_hist[0] else '↓ bajando'}")
 print(f"\n Sistema fusionado completado. ■")
