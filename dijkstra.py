import heapq


def dijkstra(grafo, origem, destino):
    distancias = {origem: 0.0}
    antecessor = {}
    confirmados = set()
    fila = [(0.0, 0, origem)]
    desempate = 1

    while fila:
        distancia, _, vertice = heapq.heappop(fila)
        if vertice in confirmados:
            continue
        confirmados.add(vertice)
        if vertice == destino:
            break
        for vizinho, peso in grafo.get(vertice, {}).items():
            if peso < 0:
                raise ValueError("Dijkstra não aceita pesos negativos")
            nova = distancia + peso
            if vizinho not in distancias or nova < distancias[vizinho]:
                distancias[vizinho] = nova
                antecessor[vizinho] = vertice
                heapq.heappush(fila, (nova, desempate, vizinho))
                desempate += 1

    if destino not in confirmados:
        raise LookupError(f"Não existe caminho de {origem} até {destino}")

    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(antecessor[caminho[-1]])
    caminho.reverse()
    return caminho, distancias[destino]


def distancias_a_partir_de(grafo, origem):
    distancias = {origem: 0.0}
    confirmados = set()
    fila = [(0.0, 0, origem)]
    desempate = 1

    while fila:
        distancia, _, vertice = heapq.heappop(fila)
        if vertice in confirmados:
            continue
        confirmados.add(vertice)
        for vizinho, peso in grafo.get(vertice, {}).items():
            nova = distancia + peso
            if vizinho not in distancias or nova < distancias[vizinho]:
                distancias[vizinho] = nova
                heapq.heappush(fila, (nova, desempate, vizinho))
                desempate += 1
    return distancias


def para_dicionario(grafo_networkx, atributo="length"):
    resultado = {}
    for u, vizinhos in grafo_networkx.adjacency():
        resultado[u] = {}
        for v, arestas in vizinhos.items():
            if isinstance(arestas, dict) and atributo not in arestas:
                peso = min(dados[atributo] for dados in arestas.values())
            else:
                peso = arestas[atributo]
            resultado[u][v] = peso
    return resultado
