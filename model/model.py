import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestDist = 0


    def getPath(self):
        self._bestPath = []
        self._bestDist = 0
        parziale = []
        for n in self._graph.nodes:
            parziale.append(n)
            self._ricorsione(parziale, float("-inf"))
            parziale.pop()
        return self._bestPath, self._bestDist


    def _ricorsione(self, parziale, peso_prec):
        dist = self._calcolaDistanzaTot(parziale)
        if dist > self._bestDist:
            self._bestDist = dist
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            peso_corr = self._graph[parziale[-1]][n]["weight"]
            if peso_corr > peso_prec and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, peso_corr)
                parziale.pop()

    def _calcolaDistanzaTot(self, parziale):
        distTot = 0
        for i in range(len(parziale) - 1):
            distTot += parziale[i].distance(parziale[i + 1])
        return distTot


    def buildGraph(self, year, shape):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getAllNodes()
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMap[node.id] = node
        DAO.getNumSightings(year, shape, self._idMap)
        edges = DAO.getAllEdges(self._idMap)
        for e in edges:
            self._graph.add_edge(e[0], e[1], weight = e[0].numSightings + e[1].numSightings)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getWeightNeighbors(self):
        nodi_con_peso = []
        for nodo in self._graph.nodes:
            peso = 0
            for v in self._graph.neighbors(nodo):
                peso += self._graph[nodo][v]["weight"]
            nodi_con_peso.append((nodo, peso))

        return nodi_con_peso



    def getAllYears(self):
        return DAO.getAllYears()


    def getAllShapes(self):
        return DAO.getAllShapes()


    def getGraph(self):
        return self._graph