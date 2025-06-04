import copy
import warnings

import networkx as nx
from networkx.algorithms.shortest_paths.unweighted import predecessor

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
        self._nodi=[]

        #ricorsione
        self._bestPath = []  # percorso che mi da peso massimo
        self._bestScore = 0  # peso massimo


    #creo grafo
    def buildGraph(self,store_id,k):
        self._grafo.clear()
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

    def getDFSNodesFromTree(self,source):
        tree=nx.dfs_tree(self._grafo,source)
        nodi=list(tree.nodes())
        #CICLO SU TUTTI I NODI
        return nodi[1:]
        #ordine diverso da bfs perchè va sempre con l'adiacente

    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())


    def getAllStores(self):
        return DAO.getAllStores()

    def getNodes(self):
        return self._nodi


    ########parte 2#####
    def getBestPath(self,start):
        self._bestPath = [] #percorso che mi da peso massimo
        self._bestScore = 0 #peso massimo
        parziale= [start] #parziale inizia con il nodo di partenza

        vicini= self._grafo.neighbors(start) #mi trovo i vicino da iterare
        for v in vicini:
            if v != start:
                #posso aggiungerlo? si perchè start non ha predecessori
                parziale.append(v)#questo per partire sempre da una situa in cui parziale ha 2 oggetti
                self._ricorsione(parziale)
                parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self,parziale):
        # Verifico che parziale sia una soluzione, e verifico se migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        #verifico se posso aggiungere un nuovo nodo(dai vicini:in questo caso sono i successori)
            #VINCOLO: non deve essere in parziale il vicino dell'ultimo nodo aggiunto e l'arco deve essere minore di quello precedente
        for v in self._grafo.neighbors(parziale[-1]):
            if (v not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] > self._grafo[parziale[-1]][v]["weight"]):
                #precedente>successivo (decrescente)
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

        #aggiungo nodo e faccio ricorsione
    def score(self, listOfNodes):
        if len(listOfNodes) < 2:
            warnings.warn("Errore in score, attesa lista lunga almeno 2.")
        totPeso = 0
        for i in range(len(listOfNodes) - 1):
            totPeso += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return totPeso

