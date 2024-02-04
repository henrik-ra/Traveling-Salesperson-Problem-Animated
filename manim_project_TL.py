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

        # Teil 2: Lower Bound 
        # self.lower_bound()

        # Teil 3: Christofides-Algorithmus (
        # self.christofides_algorithm()  

    def symmetric_vs_asymmetric(self):
        with self.voiceover(text="There are symmetrical and asymmetrical TSPs.") as tracker:

            text_symmetrical = Text("Symmetrical", font_size=36).move_to(LEFT*2)
            text_asymmetrical = Text("Asymmetrical", font_size=36).move_to(RIGHT*2)
            text_vs = Text("vs", font_size=36)
  

            self.play(Write(text_symmetrical), Write(text_asymmetrical), Write(text_vs))

        
        with self.voiceover(text= "First we will explain the symmetrical TSP") as tracker:
            self.play(
                text_symmetrical.animate.move_to(ORIGIN).to_edge(UP),
                FadeOut(text_vs),
                FadeOut(text_asymmetrical),
            )

        with self.voiceover(text="A TSP is called symmetrical, if the edges between two nodes have the same value in both directions. This means the way form one town to another would be exact the same in both directions. This isn't really accurate because of conditions of the landscape or construction sites.") as tracker:

            positions_sym = {
            0: LEFT * 2 + UP,
            1: ORIGIN + UP * 2,
            2: RIGHT * 2 + UP,
            3: RIGHT  + DOWN,
            4: LEFT  + DOWN,
            }
            # Erstellen des Graphen mit Kanten
            graph_sym = CustomGraph(list(positions_sym.keys()), [], layout=positions_sym, labels=True)
            self.play(Create(graph_sym))

            edges_sym = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

            label_offsets_sym = {
            (0, 1): (LEFT+UP) * 0.2,
            (1, 2): (UP + RIGHT) * 0.2,
            (2, 3): (DOWN + RIGHT) * 0.2,
            (3, 4): DOWN * 0.2,
            (4, 0): (DOWN+LEFT) * 0.2,
                }
            
            edge_labels_sym = ["4", "3", "7", "8", "5"]
            line_positions_sym = {
            (0, 1): (positions_sym[0] + RIGHT * 0.2 + UP * 0.2, positions_sym[1] + 0.1* DOWN+LEFT * 0.3),
            (1, 2): (positions_sym[1] + RIGHT * 0.3 + DOWN * 0.1, positions_sym[2] + 0.2* UP+LEFT * 0.2),
            (2, 3): (positions_sym[2] + DOWN * 0.3, positions_sym[3] + UP * 0.3 + RIGHT * 0.1),
            (3, 4): (positions_sym[3] + LEFT * 0.3, positions_sym[4] + RIGHT * 0.3),
            (4, 0): (positions_sym[4] + LEFT * 0.1 + UP * 0.3, positions_sym[0] + DOWN * 0.3),
                }

            
        
            lines_and_labels_sym = VGroup()
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_sym):
                start_pos, end_pos = line_positions_sym[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_sym = Line(start_pos, end_pos, color=WHITE)
                label_pos_sym = mid_pos + label_offsets_sym[edge]  # Verschiebung anwenden
                label_sym = Text(edge_labels_sym[i], font_size=24).move_to(label_pos_sym)
                lines_and_labels_sym.add(line_sym, label_sym)

                self.play(Create(line_sym), Write(label_sym), run_time=0.5)
            
        with self.voiceover(text="Thats why there is also a asymmetrical TSP.") as tracker:
            text_asymmetrical = Text("Asymmetrical", font_size=36).move_to(ORIGIN).to_edge(UP)
            group = VGroup(graph_sym, lines_and_labels_sym, text_symmetrical) 
            self.play(FadeOut(group))
            self.play(Write(text_asymmetrical))

        with self.voiceover(text="The TSP is called asymetrical if there are two edges between every node and they don't have the same weight. As you can see the graph is then directed. This is way more accurate to the real world, but this is also twice as complex to solve then the symmetrical. This is why we only observe symmetrical TSPs in the following.") as tracker:
            positions_asym = {
            0: LEFT * 2 + UP,
            1: ORIGIN + UP * 2,
            2: RIGHT * 2 + UP,
            3: RIGHT  + DOWN,
            4: LEFT  + DOWN,
            }
             
            graph_asym = CustomGraph(list(positions_asym.keys()), [], layout=positions_asym, labels=True)
            self.play(Create(graph_asym))
        
            edges_asym = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1,0), (2,1), (3,2), (4,3), (0,4)]

            label_offsets_asym = {
            # Äußere Kanten
            (0, 1): (LEFT+UP) * 0.3,
            (1, 2): (UP + RIGHT) * 0.3,
            (2, 3): (DOWN + RIGHT) * 0.3,
            (3, 4): DOWN * 0.3,
            (4, 0): (DOWN+LEFT) * 0.3,
            # Innere Kanten
            (1, 0): (RIGHT+DOWN) * 0.3,
            (2, 1): (DOWN + LEFT) * 0.3,
            (3, 2): (UP + LEFT) * 0.3,
            (4, 3): UP * 0.3,
            (0, 4): (UP+RIGHT) * 0.3,
                }
            
            edge_labels_asym = [
                # Äußere Kanten
                "4", "3", "7", "8", "5", 
                # Innere Kannten 
                "2", "5", "6", "6", "4"
                ]
            
            line_positions_asym = {
            # Äußere Kanten
            (0, 1): (positions_asym[0] + RIGHT * 0.1 + UP * 0.3, positions_asym[1] + LEFT * 0.2 + UP*0.2),
            (1, 2): (positions_asym[1] + RIGHT * 0.2 + UP * 0.2, positions_asym[2] + 0.3* UP + LEFT * 0.1),
            (2, 3): (positions_asym[2] + DOWN * 0.3 + RIGHT * 0.1, positions_asym[3] + UP * 0.2 + RIGHT * 0.2),
            (3, 4): (positions_asym[3] + LEFT * 0.3 + DOWN * 0.1, positions_asym[4] + RIGHT * 0.3 + DOWN * 0.1),
            (4, 0): (positions_asym[4] + LEFT * 0.2 + UP * 0.2, positions_asym[0] + DOWN * 0.3 + LEFT * 0.1),
            # Innere Kanten
            (1, 0): (positions_asym[1] + LEFT * 0.2 + DOWN * 0.2, positions_asym[0] + RIGHT * 0.3),
            (2, 1): (positions_asym[2] + LEFT * 0.3, positions_asym[1] + 0.2 * DOWN + RIGHT * 0.2),
            (3, 2): (positions_asym[3] + UP * 0.3, positions_asym[2] + DOWN * 0.3 + LEFT * 0.2),
            (4, 3): (positions_asym[4] + UP * 0.1 + RIGHT * 0.3, positions_asym[3] + LEFT * 0.3 + UP * 0.1),
            (0, 4): (positions_asym[0] + RIGHT * 0.2 + DOWN * 0.3, positions_asym[4] + UP * 0.3),
                }

            lines_and_labels_asym = VGroup()
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_asym):
                start_pos, end_pos = line_positions_asym[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_asym = Arrow(start_pos, end_pos, color=WHITE)
                label_pos_asym = mid_pos + label_offsets_asym[edge]  # Verschiebung anwenden
                label_asym = Text(edge_labels_asym[i], font_size=24).move_to(label_pos_asym)
                lines_and_labels_asym.add(line_asym, label_asym)

                self.play(Create(line_asym), Write(label_asym), run_time=0.5)

            group = VGroup(lines_and_labels_asym, graph_asym, text_asymmetrical)
        
        with self.voiceover(text="now we go on with the next topic") as tracker:
            self.play(FadeOut(group))

    def lower_bound(self):
        # Code für die Erklärung des Lower Bound
        with self.voiceover(text="We need to point out how good is our approximated solution compared to the optimum.") as tracker:
            # Erstellen des Textobjekts
            solution_text = Text("How good is our solution?", font_size=40).move_to(ORIGIN)
        
            # Text einblenden
            self.play(Write(solution_text))
        
        with self.voiceover(text="In some business cases there is a treshold given by the supervisor so you don't need to know how near the solution is to the optimum but in a theroetic case we want to know this.") as tracker:
            self.wait(4)

        with self.voiceover(text="As we know to determine the optimum is not economically sensible so we need to find an other value to measure our solution.") as tracker:
            self.wait(4)
            self.play(FadeOut(solution_text))
        
        with self.voiceover(text="So lets imagine we have these nodes as a tsp") as tracker:

            positions_ap = {
            0: LEFT * 4 + UP * 2,
            1: LEFT * 2 + UP * 2,
            2: LEFT * 2 + DOWN * 2,
            3: LEFT * 4 + DOWN * 2,
            4: ORIGIN,
            5: RIGHT * 2 + UP * 2,
            6: RIGHT * 4 + UP * 2,
            7: RIGHT * 2 + DOWN * 2,
            8: RIGHT * 4 + DOWN * 2,
            9: UP * 2,
            }

            # Alle Knoten initial erstellen
            graph_ap = CustomGraph(list(positions_ap.keys()), [], layout=positions_ap, labels=True)

            # Graphen ohne Kanten zeichnen
            self.play(Create(graph_ap))
        
        with self.voiceover(text="and this is our approximated solution.") as tracker:
            header_text = Text("Approximated", font_size=48).to_edge(UP)
        
            # Überschrift zeichnen
            self.play(Write(header_text))
  
            edges_ap = [
            (0, 1), (1, 9), (9, 5), (5, 6), 
            (6,8), (8,7), (7,4), (4,2), (2,3), (3,0) 
            
            ]

            # Manuelle Verschiebungen für jedes Label
            label_offsets_ap = {
            (0, 1): UP * 0.2,
            (1, 9): UP * 0.2,
            (9, 5): UP * 0.2,
            (5, 6): UP * 0.2,
            (6, 8): LEFT * 0.2,
            (8, 7): UP * 0.2,
            (7, 4): (UP+RIGHT) * 0.2,
            (4, 2): (UP + LEFT) * 0.2,
            (2, 3): UP * 0.2,
            (3,0): LEFT * 0.2,
            }

            edge_labels_ap = ["4", "3", "7", "8", "15", "2", "9", "4", "8", "19"] 
            line_positions_ap = {
            (0, 1): (positions_ap[0] + RIGHT * 0.3, positions_ap[1] + LEFT * 0.3),
            (1, 9): (positions_ap[1] + RIGHT * 0.3, positions_ap[9] + LEFT * 0.3),
            (9, 5): (positions_ap[9] + RIGHT * 0.3, positions_ap[5] + LEFT * 0.3),
            (5, 6): (positions_ap[5] + RIGHT * 0.3, positions_ap[6] + LEFT * 0.3),
            (6, 8): (positions_ap[6] + DOWN * 0.3, positions_ap[8] + UP * 0.3),
            (8, 7): (positions_ap[8] + LEFT * 0.3, positions_ap[7] + RIGHT * 0.3),
            (7, 4): (positions_ap[7] + (LEFT+UP) * 0.2, positions_ap[4] + (RIGHT+DOWN) * 0.2),
            (4, 2): (positions_ap[4] + (LEFT+DOWN) * 0.2, positions_ap[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_ap[2] + LEFT * 0.3, positions_ap[3] + RIGHT * 0.3),
            (3, 0): (positions_ap[3] + UP * 0.3, positions_ap[0] + DOWN * 0.3), 
            }

            lines_and_labels_ap = VGroup()
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_ap):
                start_pos, end_pos = line_positions_ap[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_ap = Line(start_pos, end_pos, color=WHITE)
                label_pos_ap = mid_pos + label_offsets_ap[edge]  # Verschiebung anwenden
                label_ap = Text(edge_labels_ap[i], font_size=24).move_to(label_pos_ap)
                lines_and_labels_ap.add(line_ap, label_ap)

                self.play(Create(line_ap), Write(label_ap), run_time=0.5)
        
            self.wait(2)

        with self.voiceover(text="We take a look at all the weights and sum them up.") as tracker:
            # Gleichungstext erstellen
            equation_text_ap = Text("4 + 3 + 7 + 8 + 15 + 2 + 9 + 4 + 8 + 19 = 79", font_size=36).to_edge(DOWN, buff=1)

            # Texte zeichnen
            self.play(Write(equation_text_ap))
            self.wait(2)

        with self.voiceover(text="This is the value for our approximated solution.") as tracker:

            approximated_text = Text("Approximated = 79", font_size=36).next_to(equation_text_ap, DOWN)

            # Texte zeichnen
            self.play(Write(approximated_text))
            self.wait(2)

        with self.voiceover(text="But now we still don't now how good this is compared to the optimum.") as tracker:

            all_objects_ap = VGroup(graph_ap, equation_text_ap, header_text, lines_and_labels_ap) 

            self.play(FadeOut(all_objects_ap))
            self.play(approximated_text.animate.move_to(ORIGIN).to_edge(LEFT))
            greater_than_1 = Text(">", font_size=36).next_to(approximated_text, RIGHT)
            optimum_text = Text("Optimum = ?", font_size=36).next_to(greater_than_1, RIGHT)
            greater_than_2 = Text(">", font_size=36).next_to(optimum_text, RIGHT)
   
            header_lb = Text("Lower Bound", font_size=36)

            self.wait(0.5)

            self.play(
                Write(greater_than_1), 
                Write(optimum_text), 
                Write(greater_than_2)
            )
            self.wait(2)

            
        
        with self.voiceover(text="For this we use the lower bound.") as tracker:
            # Lower Bound Text rechts von greater_than_2 positionieren und einblenden
            header_lb.next_to(greater_than_2, RIGHT)
            self.play(Write(header_lb))
        
        with self.voiceover(text="The lower bound is the value of the sum of every weight of every edge in a minimum spanning tree."):
            all_objects = VGroup(approximated_text, greater_than_1, optimum_text, greater_than_2)
            self.play(FadeOut(all_objects))
            self.wait(0.5)
            self.play(header_lb.animate.move_to(ORIGIN).to_edge(UP))


        with self.voiceover(text="So imagine we have these nodes from before.") as tracker:
            # Knotenpositionen definieren
            positions_lb = {
            0: LEFT * 4 + UP * 2,
            1: LEFT * 2 + UP * 2,
            2: LEFT * 2 + DOWN * 2,
            3: LEFT * 4 + DOWN * 2,
            4: ORIGIN,
            5: RIGHT * 2 + UP * 2,
            6: RIGHT * 4 + UP * 2,
            7: RIGHT * 2 + DOWN * 2,
            8: RIGHT * 4 + DOWN * 2,
            9: UP * 2,
            }

            # Alle Knoten initial erstellen
            graph_lb = CustomGraph(list(positions_lb.keys()), [], layout=positions_lb, labels=True)

            # Graphen ohne Kanten zeichnen
            self.play(Create(graph_lb))
            

        with self.voiceover(text="We add the edges and their weights to the nodes so we get our minimal spanning tree.") as tracker:
            self.wait(2)

            # Kanten definieren, die einen MST bilden (hier als Beispiel ausgewählt)
            edges_lb = [
            (0, 1), (1, 9), (9, 5), (5, 6), 
            (9,4), (4, 7), (7, 8), (4,2), (2, 3), 
            
            ]

            # Manuelle Verschiebungen für jedes Label
            label_offsets_lb = {
            (0, 1): UP * 0.2,
            (1, 9): UP * 0.2,
            (9, 5): UP * 0.2,
            (5, 6): UP * 0.2,
            (9, 4): LEFT * 0.2,
            (4, 7): (UP + RIGHT) * 0.2,
            (7, 8): UP * 0.2,
            (4, 2): (UP + LEFT) * 0.2,
            (2, 3): UP * 0.2,
            }

            edge_labels_lb = ["4", "3", "7", "8", "5", "9", "2", "4", "8"] 
            line_positions_lb = {
            (0, 1): (positions_lb[0] + RIGHT * 0.3, positions_lb[1] + LEFT * 0.3),
            (1, 9): (positions_lb[1] + RIGHT * 0.3, positions_lb[9] + LEFT * 0.3),
            (9, 5): (positions_lb[9] + RIGHT * 0.3, positions_lb[5] + LEFT * 0.3),
            (5, 6): (positions_lb[5] + RIGHT * 0.3, positions_lb[6] + LEFT * 0.3),
            (9, 4): (positions_lb[9] + DOWN * 0.3, positions_lb[4] + UP * 0.3),
            (4, 7): (positions_lb[4] + (RIGHT+DOWN) * 0.2, positions_lb[7] + (LEFT+UP) * 0.2),
            (7, 8): (positions_lb[7] + RIGHT * 0.3, positions_lb[8] + LEFT * 0.3),
            (4, 2): (positions_lb[4] + (LEFT+DOWN) * 0.2, positions_lb[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_lb[2] + LEFT * 0.3, positions_lb[3] + RIGHT * 0.3), 
            }
            
            lines_and_labels_lb = VGroup()
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_lb):
                start_pos, end_pos = line_positions_lb[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_lb = Line(start_pos, end_pos, color=WHITE)
                label_pos_lb = mid_pos + label_offsets_lb[edge]  # Verschiebung anwenden
                label_lb = Text(edge_labels_lb[i], font_size=24).move_to(label_pos_lb)
                lines_and_labels_lb.add(line_lb, label_lb)


                self.play(Create(line_lb), Write(label_lb), run_time=0.5)
        
            self.wait(2)

        with self.voiceover(text="We take again a look at all the weights and sum them up.") as tracker:
            # Gleichungstext erstellen
            equation_text = Text("4 + 3 + 7 + 8 + 5 + 9 + 2 + 4 + 8 = 50", font_size=36).to_edge(DOWN, buff=1)

            # Texte zeichnen
            self.play(Write(equation_text))
            self.wait(2)

        with self.voiceover(text="This is the value of our lower bound.") as tracker:
            # "Lower Bound"-Text erstellen und direkt unter der Gleichung positionieren
            lower_bound_text = Text("Lower Bound = 50", font_size=36).next_to(equation_text, DOWN)

            # Texte zeichnen
            self.play(Write(lower_bound_text))

        with self.voiceover(text="Now we have a value which we can compare to our approximated solution and we know how good it is!") as tracker:
            all_objects_ap = VGroup(graph_lb, equation_text, header_lb, lines_and_labels_lb) 

            self.play(FadeOut(all_objects_ap))
            self.wait(0.5)
            self.play(lower_bound_text.animate.move_to(ORIGIN+RIGHT*4))
            approximated_text = Text("Approximated = 79", font_size=36).move_to(4*LEFT + ORIGIN) 
            greater_than_3 =Text(">", font_size=36).move_to(ORIGIN)
            self.play(Write(approximated_text), Write(greater_than_3))

            self.wait(2)
        
        # with self.voiceover(text="") as tracker:
        #     pass



    # def christofides_algorithm(self):
    #     with self.voiceover(text="In the following we will explain the christofides algorithm.") as tracker:
    #         pass

    #     with self.voiceover(text="This is an heuritstic algorithm to solve the TSP in a heritic way.") as tracker:
    #         pass

    #     with self.voiceover(text="This algorithm guarantees a solution that is at most fifthy percent longer than the optimal round trip") as tracker:
    #         pass

    #     with self.voiceover(text="First we will create a minimal spanning tree with every node by using the algrithm of Prim.") as tracker:
    #         #O(n log n) 
    #         pass

    #     with self.voiceover(text="Then we search for every node in the graph with an odd degree, meaning an odd number of edges by using the algorithm of Blossom") as tracker:
    #         #O(n^3) n = node
    #         pass

    #     with self.voiceover(text="After finding all the nodes with an odd degree we need to find a minimum perfect matching in the subgraph consisting only of the odd degree vertices. A perfect matching means every vertex is paired, and minimal means the sum of the lengths of the edges in the pairing is minimized.") as tracker:
    #         #O(n)
    #         pass

    #     with self.voiceover(text="Then we need to combine the minimum spanning tree with the perfect matching to obtain a multigraph in which every vertex has an even degree.") as tracker:
    #         #O(n)
    #         pass
        
    #     with self.voiceover(text="Since every vertex has an even degree, there exists an Eulerian circuit in this graph. An Eulerian circuit is a path that visits each edge exactly once. We need to find it.") as tracker:
    #         #O(n)
    #         pass

    #     with self.voiceover(text="There it is!") as tracker:
    #         pass

    #     with self.voiceover(text="Last thing to do is to Transform the Eulerian circuit into a Hamiltonian circuit by skipping any vertex visited more than once, to get a round trip that visits each vertex exactly once.") as tracker:
    #         #O(n)
    #         pass

    #     with self.voiceover(text="There it is. Our heuristic result!") as tracker:
    #         pass

    #     with self.voiceover(text="In summary, the time complexity of the Christofides algorithm is mainly determined by the step of finding a minimum perfect matching, which is O(n^3). Therefore, the overall complexity of the Christofides algorithm is O(n^3).") as tracker:
    #         pass


if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} AzureExample")