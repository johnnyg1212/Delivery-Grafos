import random
import unittest

from dijkstra import dijkstra, distancias_a_partir_de, para_dicionario

try:
    import networkx as nx
except ImportError:
    nx = None


def bairro_de_brinquedo():
    ruas = [
        ("L", "A", 200), ("A", "B", 150), ("A", "C", 300), ("B", "C", 100),
        ("B", "D", 250), ("C", "D", 120), ("D", "E", 180),
    ]
    grafo = {}
    for u, v, peso in ruas:
        grafo.setdefault(u, {})[v] = peso
        grafo.setdefault(v, {})[u] = peso
    return grafo


class TestDijkstra(unittest.TestCase):
    def test_bairro_de_brinquedo(self):
        caminho, distancia = dijkstra(bairro_de_brinquedo(), "L", "E")
        self.assertEqual(caminho, ["L", "A", "B", "C", "D", "E"])
        self.assertEqual(distancia, 750)

    def test_origem_igual_ao_destino(self):
        caminho, distancia = dijkstra(bairro_de_brinquedo(), "A", "A")
        self.assertEqual(caminho, ["A"])
        self.assertEqual(distancia, 0)

    def test_sem_caminho(self):
        grafo = {"A": {"B": 1}, "B": {"A": 1}, "C": {}}
        with self.assertRaises(LookupError):
            dijkstra(grafo, "A", "C")

    def test_rua_de_mao_unica(self):
        grafo = {"A": {"B": 5}, "B": {"C": 5}, "C": {"A": 1}}
        self.assertEqual(dijkstra(grafo, "A", "C"), (["A", "B", "C"], 10))
        self.assertEqual(dijkstra(grafo, "C", "B"), (["C", "A", "B"], 6))

    def test_peso_negativo(self):
        grafo = {"A": {"B": -1}, "B": {}}
        with self.assertRaises(ValueError):
            dijkstra(grafo, "A", "B")

    def test_distancias_a_partir_de(self):
        distancias = distancias_a_partir_de(bairro_de_brinquedo(), "L")
        self.assertEqual(distancias["E"], 750)
        self.assertEqual(distancias["B"], 350)

    @unittest.skipIf(nx is None, "networkx não instalado")
    def test_igual_ao_networkx_em_grafos_aleatorios(self):
        gerador = random.Random(42)
        for _ in range(200):
            n = gerador.randint(3, 25)
            g = nx.gnp_random_graph(n, 0.25, seed=gerador.randint(0, 10**6), directed=True)
            for u, v in g.edges:
                g[u][v]["length"] = gerador.randint(1, 50)
            origem, destino = gerador.sample(range(n), 2)
            dicionario = para_dicionario(g)
            try:
                esperado = nx.dijkstra_path_length(g, origem, destino, weight="length")
            except nx.NetworkXNoPath:
                with self.assertRaises(LookupError):
                    dijkstra(dicionario, origem, destino)
                continue
            caminho, distancia = dijkstra(dicionario, origem, destino)
            self.assertEqual(distancia, esperado)
            soma = sum(dicionario[u][v] for u, v in zip(caminho[:-1], caminho[1:]))
            self.assertEqual(soma, esperado)

    @unittest.skipIf(nx is None, "networkx não instalado")
    def test_multidigrafo_usa_a_menor_aresta_paralela(self):
        g = nx.MultiDiGraph()
        g.add_edge("A", "B", length=10)
        g.add_edge("A", "B", length=4)
        self.assertEqual(para_dicionario(g), {"A": {"B": 4}, "B": {}})


if __name__ == "__main__":
    unittest.main()
