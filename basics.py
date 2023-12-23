from manim import *
from manim_svg_animations import *

import os
import random
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
import itertools

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class CustomGraph(Graph):
    def __init__(self, vertices, edges, layout="circular", layout_scale=2.5, label_color=WHITE, *args, **kwargs):
        # Standardkonfigurationen für Knoten und Kanten
        default_vertex_config = {
            "color": DARK_BLUE,  # Dunkelblauer Farbton für Knoten
            "radius": 0.3,
            "stroke_color": WHITE,
            "stroke_width": 3,
            "fill_opacity": 1
        }
        default_edge_config = {
            "stroke_color": GREY,
            "stroke_width": 3,
        }

        # Aktualisieren der Konfigurationen mit benutzerdefinierten Einstellungen
        vertex_config = kwargs.pop("vertex_config", {})
        edge_config = kwargs.pop("edge_config", {})
        default_vertex_config.update(vertex_config)
        default_edge_config.update(edge_config)

        # Hinzufügen der Layout-Parameter zu kwargs
        kwargs["layout"] = layout
        kwargs["layout_scale"] = layout_scale

        # Initialisieren des Basis-Graphen
        super().__init__(vertices, edges, vertex_config=default_vertex_config, edge_config=default_edge_config, *args, **kwargs)



        # Hinzufügen der Labels mit der gewünschten Farbe
        self.label_color = label_color
        self.add_labels()

    def add_labels(self):
        for vertex in self.vertices:
            label = Tex(str(vertex), color=self.label_color)
            label.move_to(self[vertex].get_center())
            self.add(label)
            




# class Graph_TSP(Graph):
#     def __init__(
#         self,
#         vertices,
#         dist_matrix=None,
#         vertex_config=None,
#         edge_config=None,
#         labels=True,
#         label_scale=0.6,
#         label_color=WHITE,
#         **kwargs,
#     ):
#         super().__init__(vertices, dist_matrix, vertex_config, edge_config, labels, label_scale, label_color, **kwargs)

#     def get_all_edges(self, edge_type=Line, buff=None):
#         """Creates and returns a dictionary of all possible edges between vertices."""
#         edge_dict = {}
#         for u, v in itertools.combinations(self.vertices.keys(), 2):
#             edge_dict[(u, v)] = self.create_edge(u, v, edge_type=edge_type, buff=buff)
#         return edge_dict

#     def create_edge(self, u, v, edge_type=Line, buff=None):
#         """Creates an edge between two vertices using the specified edge_type and buffer."""
#         return edge_type(
#             self.vertices[u].get_center(),
#             self.vertices[v].get_center(),
#             color=self.edge_config.get("color", REDUCIBLE_VIOLET),
#             stroke_width=self.edge_config.get("stroke_width", 3),
#             buff=buff if buff is not None else self.edge_config.get("buff", 0),
#         )

#     def get_dist_matrix(self):
#         """Returns the distance matrix of the graph."""
#         return self.dist_matrix

#     def get_neighboring_edges(self, vertex, buff=None):
#         """Returns a dictionary of edges connected to a given vertex."""
#         neighbors = get_neighbors(vertex, len(self.vertices))
#         return {(vertex, other): self.create_edge(vertex, other, buff=buff) for other in neighbors}


