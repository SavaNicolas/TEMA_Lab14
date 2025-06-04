import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._storeScelto = None
        self._nodoScelto = None


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        # prendo store dall'input
        store = self._storeScelto.store_id
        # controlli
        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona uno store!!!"))
            self._view.update_page()
            return

        # converto in intero
        try:
            store = int(store)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("store non valido"))
            self._view.update_page()
            return

        # prendo k dall'input
        k = self._view._txtIntK.value
        # controlli
        if k is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona un numero massimo di giorni!!!"))
            self._view.update_page()
            return

        # converto in intero
        try:
            k = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("numero di giorni non valido"))
            self._view.update_page()
            return

        # creo grafo
        self._model.buildGraph(store,k)

        #posso riempire la tendina dei nodi
        nodi = self._model.getNodes()
        self.fillDDNodi(nodi)
        self._view.update_page()

        # posso abilitare bottoni

        self._view._btnCerca.disabled = False
        self._view._ddNode.disabled = False
        self._view._btnRicorsione.disabled = False

        # stampo txt result
        self._view.txt_result.controls.append(ft.Text("grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"il grafo ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()


    def handleCerca(self, e):

        # prendo store dall'input
        nodo = self._nodoScelto
        # controlli
        if nodo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona uno store!!!"))
            self._view.update_page()
            return

        #chiamo algoritmo
        listaNodi = self._model.getDFSNodesFromTree(nodo)
        self._view.txt_result.controls.append(ft.Text(f"percorso più lungo partendo da: {nodo.order_id}"))
        for nodo in listaNodi:
            self._view.txt_result.controls.append(ft.Text(nodo))
        self._view.update_page()

    def handleRicorsione(self, e):
        # prendo store dall'input
        nodo = self._nodoScelto
        # controlli
        if nodo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona uno store!!!"))
            self._view.update_page()
            return

        # chiamo algoritmo
        path,peso=self._model.getBestPath(nodo)
        self._view.txt_result.controls.append(ft.Text(f"Percorso con peso massimo partendo da {nodo.order_id}: {peso}"))
        for nodo in path:
            self._view.txt_result.controls.append(ft.Text(nodo))
        self._view.update_page()

    def fillDDStore(self):
        for store in self.getAllNodes():  # sto appendendo al dropdown l'oggetto reatiler
            self._view._ddStore.options.append(
                ft.dropdown.Option(key=store.store_id,  # 🔑 Chiave univoca dell'opzione
                                   text=store.store_name,  # 🏷️ Testo visibile nel menu a tendina
                                   data=store,
                                   # 📦 Oggetto completo, utile per accedere a tutti gli attributi dopo la selezione
                                   on_click=self.read_store))  # salvati l'oggetto da qualche parte

    def read_store(self, e):
        self._storeScelto = e.control.data  # l'abbiamo inizializzata a None
        # e.control.data è il risultato di onclick sopra

    def fillDDNodi(self,nodi):
        for ordine in nodi:  # sto appendendo al dropdown l'oggetto reatiler
            self._view._ddNode.options.append(
                ft.dropdown.Option(key=ordine.order_id,  # 🔑 Chiave univoca dell'opzione
                                   text=ordine.order_id,  # 🏷️ Testo visibile nel menu a tendina
                                   data=ordine,
                                   # 📦 Oggetto completo, utile per accedere a tutti gli attributi dopo la selezione
                                   on_click=self.read_nodi))  # salvati l'oggetto da qualche parte

    def read_nodi(self, e):
        self._nodoScelto = e.control.data  # l'abbiamo inizializzata a None
        # e.control.data è il risultato di onclick sopra

    def getAllNodes(self):
        return self._model.getAllStores()

    def getNodes(self):
        return self._model.getNodes()

