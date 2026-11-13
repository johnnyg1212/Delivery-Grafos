# Algoritmo de Dijkstra para Bairro real de Limeira- SP  
## Grupo 3 - Tópicos em Computação e Informática
- João Guilherme Fernandes Frota
- Gabriel Hebert

## Tema : Dijkstra

## O que o projeto faz

Modela um bairro real de Limeira como grafo (esquinas são vértices, trechos de rua são arestas, o peso é o comprimento em metros), define uma loja de delivery na borda do bairro e calcula, com o algoritmo de Dijkstra implementado pelo grupo, a rota de bicicleta da loja até o cliente escolhido. A rota é mostrada sobre o mapa real das ruas.

## Arquivos

- `dijkstra.py`: algoritmo de Dijkstra escrito pelo grupo, sem biblioteca de grafos.
- `main.py`: baixa as ruas do bairro (OpenStreetMap), escolhe a loja e os clientes, calcula a rota e gera o mapa.
- `test_dijkstra.py`: testes do algoritmo, inclusive a comparação com o NetworkX em 200 grafos aleatórios.
- `requirements.txt`: bibliotecas necessárias.

## Como rodar

```
python -m pip install -r requirements.txt
python -m unittest -v
python main.py
```

Antes de rodar o `main.py`, ajuste no topo do arquivo:

- `BAIRRO`: nome do bairro no formato `"Nome do Bairro, Limeira, São Paulo, Brazil"`.
- `LOJA_LATLON`: coordenadas `(latitude, longitude)` de um lote na borda do bairro. Com `None`, a loja fica na esquina mais a oeste.

O mapa é salvo na pasta `saida/`. Abra o arquivo `.html` no navegador.
