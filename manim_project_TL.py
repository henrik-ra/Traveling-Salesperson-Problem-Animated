from manim import *
from manim_svg_animations import *
import os
import random
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
import itertools
from itertools import permutations
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

from basics import CustomGraph

# voices: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts

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

        # Adding labels
        self.label_color = label_color
        self.add_labels()

         # Make edges invisible initially
        for edge in self.edges:
            self.edges[edge].set_opacity(0)
    
    def add_labels(self):
        labels = VGroup()
        for vertex in self.vertices:
            label = Text(str(vertex), color=self.label_color, font_size=24)
            label.move_to(self[vertex].get_center())
            labels.add(label)
        self.add(labels)  # Füge die Labels zum Graphen hinzu


    def get_edges_with_initial_opacity_zero(self):
    # Set initial opacity of edges to 0 and return them
        for edge in self.edges.values():
            edge.set_opacity(0)
        return self.edges.values()
    
    def add_labels(self):
        labels = VGroup()
        for vertex in self.vertices:
            label = Text(str(vertex), color=self.label_color, font_size=24)
            label.move_to(self[vertex].get_center())
            labels.add(label)
        return labels  # Return the group of labels
    
    def set_edge_style(self, edge, color=None, stroke_width=None):
        if edge in self.edges:
            if color is not None:
                self.edges[edge].set_color(color)
            if stroke_width is not None:
                self.edges[edge].set_stroke(width=stroke_width)

class AzureExample(VoiceoverScene):
    def construct(self):

        # Initalisierung des Voiceovers
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        ) 

        # Teil 1: Symmetrisch vs. Asymmetrisch
        self.symmetric_vs_asymmetric()

        # Teil 2: Lower Bound (Hier können Sie Ihren eigenen Code einfügen)
        self.lower_bound()

        # Teil 3: Christofides-Algorithmus (Hier können Sie Ihren eigenen Code einfügen)
        self.christofides_algorithm()

    def create_graph(self, is_symmetric, ab: str, bc: str, ca: str):
        # Erstellen eines CustomGraph-Objekts
        vertices = ["A", "B", "C"]
        edges = [("A", "B"), ("B", "C"), ("C", "A")]

        graph = CustomGraph(vertices, edges)

        # Machen Sie alle Kanten sichtbar
        for edge in graph.edges.values():
            edge.set_opacity(1)

        # Farb- und Stiländerungen, wenn asymmetrisch
        if not is_symmetric:
            graph.set_edge_style(("B", "C"), color=RED)
            graph.set_edge_style(("C", "A"), color=BLUE)

        # Zahlen an den Kanten hinzufügen
        edge_labels = VGroup()
        edge_labels.add(Text(ab, font_size=24).move_to(graph.edges[("A", "B")].get_center())).shift(UP + RIGHT)
        edge_labels.add(Text(bc, font_size=24).move_to(graph.edges[("B", "C")].get_center())).shift(LEFT)
        edge_labels.add(Text(ca, font_size=24).move_to(graph.edges[("C", "A")].get_center())).shift(DOWN + RIGHT)

        graph.add(edge_labels)

        return graph.shift(DOWN)    

    def symmetric_vs_asymmetric(self):

        with self.voiceover(text="Now we will explain the difference between the symmetrical and asymmetrical Traveling Salesman Problem") as tracker:
        # Titel
            title = Text("Symmetrical vs. Asymmetrical", font_size=36)
            self.play(Write(title))
            self.wait(1)
            self.play(FadeOut(title))

        with self.voiceover(text="TSP is called symetrical if the edges between two nodes have the same value in both directions. The graph is then called undirected.") as tracker:
            # Symmetrisches TSP
            symm_title = Text("Symmetrical TSP", font_size=24).to_edge(UP, buff=MED_SMALL_BUFF)
            symm_graph = self.create_graph(is_symmetric=True, ab="36km", bc="50km", ca="41km")
            self.play(FadeIn(symm_title, symm_graph))
            self.wait(2)
            self.play(FadeOut(symm_title, symm_graph))

        with self.voiceover(text="With this assumption it is easier to use heristic approaches because you just have to calculate the distance in one direction.") as tracker:
            pass
        
        with self.voiceover(text="As you can imagine in reality there isn't something like a symetrical TSP. That's why there is also an asymetrical TSP.") as tracker:
            pass

        with self.voiceover(text="The TSP is called asymetrical if there are two edges between every node and they don't have the same weight. The graph is then called directed.") as tracker:
            asymm_title = Text("Asymmetrical TSP", font_size=24).to_edge(UP, buff=MED_SMALL_BUFF)
            asymm_graph = self.create_graph(is_symmetric=False,  ab="36km", bc="50km", ca="41km")
            self.play(FadeIn(asymm_title, asymm_graph))
            self.wait(2)
            self.play(FadeOut(asymm_title, asymm_graph))

        with self.voiceover(text="You can imagine that in reality there are only asymitrical TSPs because the differnce between two cities are never the same in both directions because of the construction of the roads or other obstacles.") as tracker:
            pass

        with self.voiceover(text="in the following we will consider the TSP as symitrical so it is easier to understand.") as tracker:
            pass


    def lower_bound(self):
        # Code für die Erklärung des Lower Bound
        with self.voiceover(text="Now we need to point out how to know if our heristic result is near the optimum") as tracker:
            pass
        
        with self.voiceover(text="In some business cases there is a treshold given by the supervisor so you don't need to know how near the result is to the optimum but in a theroetic case we want to know it") as tracker:
            pass

        with self.voiceover(text="As we know to determine the optimum is not economically sensible so we need to find an other value to measure our result") as tracker:
            pass
        
        with self.voiceover(text="This value is the lower bound") as tracker:
            pass

        with self.voiceover(text="The lower bound is the value of the sum from every weight of edge in a minimum spanning tree.") as tracker:
            pass

        with self.voiceover(text="This value is lower then the optimum but in many cases very close to it.") as tracker:
            pass

        with self.voiceover(text="So to gat an idea how good the heristic result is you need to compare it to the lower bound which is easier to calculate then the optimum.") as tracker:
            pass

    def christofides_algorithm(self):
        with self.voiceover(text="In the following we will explain the christofides algorithm.") as tracker:
            pass

        with self.voiceover(text="This is an heuritstic algorithm to solve the TSP in a heritic way.") as tracker:
            pass

        with self.voiceover(text="This algorithm guarantees a solution that is at most fifthy percent longer than the optimal round trip") as tracker:
            pass

        with self.voiceover(text="First we will create a minimal spanning tree with every node by using the algrithm of Prim.") as tracker:
            #O(n log n) 
            pass

        with self.voiceover(text="Then we search for every node in the graph with an odd degree, meaning an odd number of edges by using the algorithm of Blossom") as tracker:
            #O(n^3) n = node
            pass

        with self.voiceover(text="After finding all the nodes with an odd degree we need to find a minimum perfect matching in the subgraph consisting only of the odd degree vertices. A perfect matching means every vertex is paired, and minimal means the sum of the lengths of the edges in the pairing is minimized.") as tracker:
            #O(n)
            pass

        with self.voiceover(text="Then we need to combine the minimum spanning tree with the perfect matching to obtain a multigraph in which every vertex has an even degree.") as tracker:
            #O(n)
            pass
        
        with self.voiceover(text="Since every vertex has an even degree, there exists an Eulerian circuit in this graph. An Eulerian circuit is a path that visits each edge exactly once. We need to find it.") as tracker:
            #O(n)
            pass

        with self.voiceover(text="There it is!") as tracker:
            pass

        with self.voiceover(text="Last thing to do is to Transform the Eulerian circuit into a Hamiltonian circuit by skipping any vertex visited more than once, to get a round trip that visits each vertex exactly once.") as tracker:
            #O(n)
            pass

        with self.voiceover(text="There it is. Our heuristic result!") as tracker:
            pass

        with self.voiceover(text="In summary, the time complexity of the Christofides algorithm is mainly determined by the step of finding a minimum perfect matching, which is O(n^3). Therefore, the overall complexity of the Christofides algorithm is O(n^3).") as tracker:
            pass


if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} AzureExample")