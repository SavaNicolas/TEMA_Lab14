import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._storeAll = DAO.getAllStores()  # lista con tutti gli store, per avere l'id map
        # creo grafo
        self._grafo = nx.DiGraph()
        # mappa di oggetti
        self.idMapStore = {}
        for p in self._storeAll:
            self.idMapStore[p.store_id] = p

        #mappa di nodi inizializzata a none
        self.idMap = {}


    #creo grafo
    def buildGraph(self,store_id,k):
        self._nodi = DAO.getNodes(store_id) #ordini dello store selezionato
        #creo mappa di nodi
        for p in self._nodi:
            self.idMap[p.order_id] = p
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._nodi)
        # aggiungo archi
        self.addEdges(k,store_id)

    def addEdges(self,k,store_id):
        edges = DAO.getEdges(k, store_id, self.idMap)  # mi restituisce una lista di archi: [arco1,arco2,...]

        for edge in edges:
            self._grafo.add_edge(edge.nodo1, edge.nodo2, weight=edge.peso)


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())


    def getAllStores(self):
        return DAO.getAllStores()

