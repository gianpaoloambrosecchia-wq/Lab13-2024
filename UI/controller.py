import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []


    def fillDD(self):
        self._listYear = self._model.getAllYears()
        self._listShape = self._model.getAllShapes()
        for y in self._listYear:
            self._view.ddyear.options.append(
                ft.dropdown.Option(y)
            )
        for shape in self._listShape:
            self._view.ddshape.options.append(
                ft.dropdown.Option(shape)
            )
        self._view.update_page()


    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        if year is None or shape is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un anno e una forma dagli appositi menù", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(year, shape)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {numNodes}", color="blue")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {numEdges}", color="blue")
        )
        nodi_con_peso = self._model.getWeightNeighbors()
        for n in nodi_con_peso:
            self._view.txt_result.controls.append(
                ft.Text(f"Nodo {n[0]}, somma pesi su archi = {n[1]}")
            )
        self._view.update_page()


    def handle_path(self, e):
        path, distTot = self._model.getPath()
        grafo = self._model.getGraph()
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(
            ft.Text(f"La distanza totale è: {distTot}", color="blue")
        )
        for i in range(len(path)-1):
            self._view.txtOut2.controls.append(
                ft.Text(f"{path[i]} -- {path[i+1]} | peso = {grafo[path[i]][path[i+1]]['weight']} | distanza = {path[i].distance(path[i+1])}")
            )
        self._view.update_page()
