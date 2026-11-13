import random
from pathlib import Path

import folium
import networkx as nx
import osmnx as ox

from dijkstra import distancias_a_partir_de, dijkstra, para_dicionario

BAIRRO = "Cidade Universitária I, Limeira, São Paulo, Brazil"
LOJA_LATLON = None
QUANTIDADE_CLIENTES = 5
SEMENTE = 7
PASTA_SAIDA = Path(__file__).parent / "saida"


def vertice_mais_proximo(grafo, lat, lon):
    return min(
        grafo.nodes,
        key=lambda v: (grafo.nodes[v]["y"] - lat) ** 2 + (grafo.nodes[v]["x"] - lon) ** 2,
    )


def escolher_loja(grafo):
    if LOJA_LATLON is not None:
        return vertice_mais_proximo(grafo, *LOJA_LATLON)
    return min(grafo.nodes, key=lambda v: grafo.nodes[v]["x"])


def escolher_clientes(distancias, loja):
    ordenados = sorted((v for v in distancias if v != loja), key=distancias.get)
    gerador = random.Random(SEMENTE)
    passo = len(ordenados) / QUANTIDADE_CLIENTES
    clientes = []
    for i in range(QUANTIDADE_CLIENTES):
        faixa = ordenados[int(i * passo):int((i + 1) * passo)]
        clientes.append(gerador.choice(faixa))
    return clientes


def melhor_trecho(grafo, u, v):
    return min(grafo.get_edge_data(u, v).values(), key=lambda d: d["length"])


def ruas_da_rota(grafo, caminho):
    ruas = []
    for u, v in zip(caminho[:-1], caminho[1:]):
        nome = melhor_trecho(grafo, u, v).get("name", "rua sem nome")
        if isinstance(nome, list):
            nome = nome[0]
        if not ruas or ruas[-1] != nome:
            ruas.append(nome)
    return ruas


def pontos_da_rota(grafo, caminho):
    pontos = []
    for u, v in zip(caminho[:-1], caminho[1:]):
        geometria = melhor_trecho(grafo, u, v).get("geometry")
        if geometria is not None:
            trecho = [(lat, lon) for lon, lat in geometria.coords]
        else:
            trecho = [
                (grafo.nodes[u]["y"], grafo.nodes[u]["x"]),
                (grafo.nodes[v]["y"], grafo.nodes[v]["x"]),
            ]
        pontos.extend(trecho)
    return pontos


def desenhar_mapa(grafo, loja, clientes, destino, caminho, arquivo):
    centro = [grafo.nodes[loja]["y"], grafo.nodes[loja]["x"]]
    mapa = folium.Map(location=centro, zoom_start=16, tiles="OpenStreetMap")
    for aresta in ox.graph_to_gdfs(grafo, nodes=False).geometry:
        pontos = [(lat, lon) for lon, lat in aresta.coords]
        folium.PolyLine(pontos, color="#9aa0a6", weight=2).add_to(mapa)
    folium.PolyLine(pontos_da_rota(grafo, caminho), color="#d93025", weight=6).add_to(mapa)
    folium.Marker(centro, tooltip="Loja", icon=folium.Icon(color="green")).add_to(mapa)
    for numero, cliente in enumerate(clientes, start=1):
        cor = "red" if cliente == destino else "blue"
        folium.Marker(
            [grafo.nodes[cliente]["y"], grafo.nodes[cliente]["x"]],
            tooltip=f"Cliente {numero}",
            icon=folium.Icon(color=cor),
        ).add_to(mapa)
    mapa.save(arquivo)


def carregar_grafo():
    print("Baixando as ruas do bairro (pode levar um minuto)...")
    grafo = ox.graph_from_place(BAIRRO, network_type="bike")
    return ox.truncate.largest_component(grafo, strongly=True)


def main():
    grafo = carregar_grafo()
    print(f"Esquinas (vértices): {grafo.number_of_nodes()}")
    print(f"Trechos de rua (arestas): {grafo.number_of_edges()}")
    print(f"Grafo conexo: {nx.is_strongly_connected(grafo)}")

    pesos = para_dicionario(grafo)
    loja = escolher_loja(grafo)
    clientes = escolher_clientes(distancias_a_partir_de(pesos, loja), loja)

    print("\nClientes disponíveis:")
    for numero, cliente in enumerate(clientes, start=1):
        _, distancia = dijkstra(pesos, loja, cliente)
        print(f"  {numero}) Cliente {numero} a {distancia:.0f} m")

    escolha = int(input("\nDigite o número do cliente: "))
    destino = clientes[escolha - 1]
    caminho, distancia = dijkstra(pesos, loja, destino)

    print(f"\nDistância total: {distancia:.0f} m")
    print(f"Esquinas no caminho: {len(caminho)}")
    print("Passe por:", " -> ".join(ruas_da_rota(grafo, caminho)))

    PASTA_SAIDA.mkdir(exist_ok=True)
    arquivo = PASTA_SAIDA / f"rota_cliente_{escolha}.html"
    desenhar_mapa(grafo, loja, clientes, destino, caminho, arquivo)
    print(f"Mapa salvo em {arquivo}. Abra esse arquivo no navegador.")


if __name__ == "__main__":
    main()
