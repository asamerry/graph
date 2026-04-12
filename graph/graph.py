import plotly.graph_objects as go

class Graph:
    def __init__(self): 
        self._vertices = {}; self._edges = {}

    def vertices(self): return self._vertices
    def edges(self): return self._edges

    def add_vertex(self, label: str, x: float, y: float, size: float, color: str): 
        self._vertices[label] = {"x": x, "y": y, "size": size, "color": color}
    
    def add_edge(self, v1_label: str, v2_label: str, width: float=1.0): 
        def check_input(v):
            if v not in self._vertices.keys():
                print(f"Cannot add edge to non-existing vertex of label \"{v}\"")
                exit(1)
        check_input(v1_label); check_input(v2_label)

        self._edges[(v1_label, v2_label)] = {"width": width}
    
    def complete_graph(self) -> None:
        vertices = list(self._vertices.keys())
        n = len(vertices)
        for i in range(n):
            for j in range(i+1, n):
                e = (vertices[i], vertices[j])
                if e not in self._edges.keys():
                    self.add_edge(*e)

    def plot(self):
        edge_x = []; edge_y = []; edge_widths = []
        for edge, info in self._edges.items():
            edge_x.append(self._vertices[edge[0]]["x"])
            edge_x.append(self._vertices[edge[1]]["x"])
            edge_x.append(None)
            edge_y.append(self._vertices[edge[0]]["y"])
            edge_y.append(self._vertices[edge[1]]["y"])
            edge_y.append(None)

            edge_widths.append(info["width"])

        def make_edge(edge_x, edge_y, width):
            return go.Scatter(
                x = edge_x, y = edge_y, 
                mode = "lines",
                line = dict(
                    width = width, color = "#e0e0e0"
                ),
                hoverinfo = "text"
            )

        edge_traces = [make_edge(edge_x[3*i:3*i+3], edge_y[3*i:3*i+3], edge_widths[i]) for i in range(len(edge_widths))]

        vertex_x = []; vertex_y = []; vertex_sizes = []; vertex_colors = []; vertex_labels = []
        for label, info in self._vertices.items():
            vertex_labels.append(label)
            vertex_x.append(info["x"])
            vertex_y.append(info["y"])
            vertex_sizes.append(info["size"])
            vertex_colors.append(info["color"])

        vertex_trace = go.Scatter(
            x = vertex_x, y = vertex_y, 
            mode = "markers",
            hoverinfo = "text",
            marker = dict(
                size = vertex_sizes,
                color = vertex_colors,
                opacity = 1,
                line = dict(
                    width = 0
                )
            )
        )

        vertex_trace.text = vertex_labels

        fig = go.Figure(
            data = [*edge_traces, vertex_trace],
            layout = go.Layout(
                title = dict(
                    #text = "Network of Mathematics",
                    font = dict(
                        size = 16
                    )
                ),
                paper_bgcolor = "#000", plot_bgcolor = "#000",
                showlegend = False,
                hovermode = "closest",
                xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
                yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)
            )
        )

        fig.show()
