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

        # self.symmetric_vs_asymmetric()

        # self.lower_bound()

        # self.christofides_algorithm()  

    def symmetric_vs_asymmetric(self):
        with self.voiceover(text="There are symmetrical and asymmetrical TSPs.") as tracker:
            text_symmetrical = Text("Symmetrical").move_to(LEFT*3)
            text_asymmetrical = Text("Asymmetrical").move_to(RIGHT*3)
            text_vs = Text("vs")
  
            self.play(Write(text_symmetrical), Write(text_asymmetrical), Write(text_vs))

        with self.voiceover(text= "First we will explain the symmetrical TSP") as tracker:
            self.play(
                text_symmetrical.animate.move_to(ORIGIN).to_edge(UP),
                FadeOut(text_vs),
                FadeOut(text_asymmetrical)
            )

        with self.voiceover(text="A TSP is called symmetrical, if the edges between two nodes have the same value in both directions. This means the way form one town to another would be exact the same in both directions. This isn't really accurate in real life because of conditions of the landscape or construction sites.") as tracker:
            
            positions_sym = {
            0: LEFT * 2 + UP,
            1: ORIGIN + UP * 2,
            2: RIGHT * 2 + UP,
            3: RIGHT  + DOWN,
            4: LEFT  + DOWN,
            }
            # Erstellen des Graphen mit Kanten
            graph_sym =  CustomGraph(list(positions_sym.keys()), [], layout=positions_sym)
            labels_sym = graph_sym.add_labels()
            
            self.play(Create(graph_sym))
            self.add(labels_sym)
            self.play(FadeIn(labels_sym), run_time=0.5)


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
            text_asymmetrical = Text("Asymmetrical").move_to(ORIGIN).to_edge(UP)
            group = VGroup(graph_sym, lines_and_labels_sym, text_symmetrical, labels_sym) 
            self.play(FadeOut(group))
            self.play(Write(text_asymmetrical))

        with self.voiceover(text="The TSP is called asymmetrical if there are two edges between every node and they don't have the same weight. As you can see the graph is then directed. This is way more accurate to the real world, but this is also more complex to solve then the symmetrical. In this video we will only show you ways of solving the symmetrical TSP.") as tracker:
            positions_asym = {
            0: LEFT * 2 + UP,
            1: ORIGIN + UP * 2,
            2: RIGHT * 2 + UP,
            3: RIGHT  + DOWN,
            4: LEFT  + DOWN,
            }
             
            graph_asym = CustomGraph(list(positions_asym.keys()), [], layout=positions_asym)
            labels_asym = graph_asym.add_labels()

            self.play(Create(graph_asym))
            self.add(labels_asym)
            self.play(FadeIn(labels_asym), run_time=0.5)
        
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

            group = VGroup(lines_and_labels_asym, graph_asym, text_asymmetrical, labels_asym)
        
        with self.voiceover(text="Let's take a look at how the TSP can be solved") as tracker:
            self.clear()

    def lower_bound(self):
        # Code für die Erklärung des Lower Bound
        with self.voiceover(text="We need to point out how good is our approximated solution compared to the optimum. In some business cases there is a treshold given by the supervisor so you don't need to know how near the solution is to the optimum but in a theroetic case we want to know this. For large TSP to determine the optimum is not economically sensible because of the complexity so we need to find an other value to measure our solution.") as tracker:
            # Erstellen des Textobjekts
            solution_text = Text("How good is our solution?").move_to(ORIGIN)
        
            # Text einblenden
            self.play(Write(solution_text))

        with self.voiceover(text="So lets imagine we have these nodes as a tsp") as tracker:
            self.play(FadeOut(solution_text))
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
            graph_ap = CustomGraph(list(positions_ap.keys()), [], layout=positions_ap)
            labels_ap = graph_ap.add_labels()

            self.play(Create(graph_ap))
            self.add(labels_ap)
            self.play(FadeIn(labels_ap), run_time=0.5)
        
        with self.voiceover(text="and this is our approximated solution.") as tracker:
            header_text = Text("Approximated").to_edge(UP)
        
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

                self.play(Create(line_ap), Write(label_ap), run_time=0.2)
        
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

            all_objects_ap = VGroup(graph_ap, equation_text_ap, header_text, lines_and_labels_ap, labels_ap) 

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
            graph_lb = CustomGraph(list(positions_lb.keys()), [], layout=positions_lb,)
            labels_lb = graph_lb.add_labels()
            self.play(Create(graph_lb))
            
            self.add(labels_lb)
            self.play(FadeIn(labels_lb), run_time=0.5)
            

        with self.voiceover(text="We add the edges and their weights to the nodes so we get our minimal spanning tree.") as tracker:
  

            # Kanten definieren, die einen MST bilden 
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


                self.play(Create(line_lb), Write(label_lb), run_time=0.2)
        
   

        with self.voiceover(text="We take again a look at all the weights and sum them up.") as tracker:
            # Gleichungstext erstellen
            equation_text = Text("4 + 3 + 7 + 8 + 5 + 9 + 2 + 4 + 8 = 50", font_size=36).to_edge(DOWN, buff=1)

            # Texte zeichnen
            self.play(Write(equation_text))


        with self.voiceover(text="This is the value of our lower bound.") as tracker:
            # "Lower Bound"-Text erstellen und direkt unter der Gleichung positionieren
            lower_bound_text = Text("Lower Bound = 50", font_size=36).next_to(equation_text, DOWN)

            # Texte zeichnen
            self.play(Write(lower_bound_text))

        with self.voiceover(text="Now we have a value which we can compare to our approximated solution and we know how good it is!") as tracker:
            all_objects_lb = VGroup(graph_lb, equation_text, header_lb, lines_and_labels_lb, labels_lb) 

            self.play(FadeOut(all_objects_lb))
            self.wait(0.5)
            self.play(lower_bound_text.animate.move_to(ORIGIN+RIGHT*4))
            approximated_text = Text("Approximated = 79", font_size=36).move_to(4*LEFT + ORIGIN) 
            greater_than_3 =Text(">", font_size=36).move_to(ORIGIN)
            self.play(Write(approximated_text), Write(greater_than_3))
        
        with self.voiceover(text="Now we can continue with the approximated algorithms") as tracker:
            self.play(FadeOut(approximated_text), FadeOut(greater_than_3), FadeOut(lower_bound_text))

    def christofides_algorithm(self):
        with self.voiceover(text="In the following we will explain the christofides algorithm. This is an approximated algorithm to solve the TSP. This algorithm guarantees a solution that is at most fifthy percent longer than the optimal round trip.") as tracker:
            title = Text("Christofides Algorithm").to_edge(UP)
            self.play(Write(title))

        with self.voiceover(text="First we will create a minimal spanning tree with every node.") as tracker:
            #O(n log n) 
            line1 = Text("1. Find a minimum spanning tree T of a graph G.", font_size=24).to_edge(LEFT).move_to(UP)
            self.play(Write(line1))

        with self.voiceover(text="Then we search for every node in the graph with an odd degree, meaning an odd number of edges.") as tracker:
            #O(n^3) n = node
            line2 = Text("2. Let V_odd be the set of vertices with odd degree in T.", font_size=24).to_edge(LEFT).next_to(line1, DOWN, buff=0.5)
            self.play(Write(line2))

        with self.voiceover(text="After finding all the nodes with an odd degree we need to find a minimum perfect matching, so we need to find edges with minimum weight so every node gets an even degree.") as tracker:
            #O(n)
            line3 = Text("3. Find a minimum perfect matching M in the subgraph induced by V_odd.", font_size=24).to_edge(LEFT).next_to(line2, DOWN, buff=0.5)
            self.play(Write(line3))

        with self.voiceover(text="Then we need to combine the minimum spanning tree with the perfect matching to obtain a multigraph in which every vertex has an even degree.") as tracker:
            #O(n)
            line4 = Text("4. Combine the edges of M and T to form a multigraph H.", font_size=24).to_edge(LEFT).next_to(line3, DOWN, buff=0.5)
            self.play(Write(line4))
        
        with self.voiceover(text="Since every vertex has an even degree, there exists an Eulerian circuit in this graph which we need to find. An Eulerian circuit is a path that visits each edge exactly once.") as tracker:
            #O(n)
            line5 = Text("5. Find an Eulerian circuit in H.", font_size=24).to_edge(LEFT).next_to(line4, DOWN, buff=0.5)
            self.play(Write(line5))

        with self.voiceover(text="Now we convert the Eulerian circuit to a Hamiltonian circuit by skipping repeated vertices.") as tracker:
            #O(n)
            line6 = Text("6. Convert the Eulerian circuit to a Hamiltonian circuit by skipping repeated vertices.", font_size=24).to_edge(LEFT).next_to(line5, DOWN, buff=0.5)
            self.play(Write(line6))
        
        with self.voiceover(text= "Let's take a look at the graph to visualize this algorithm.") as tracker:

            # On3 = Text(r"O($\bm{O(n^3)}$)", font_size=36).next_to(title, DOWN)

            group = VGroup(line1, line2, line3, line4, line5, line6)
            self.play(FadeOut(group))

            positions_mst = {
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
            graph_mst = CustomGraph(list(positions_mst.keys()), [], layout=positions_mst)
            labels_mst = graph_mst.add_labels()
            self.play(Create(graph_mst))

            self.add(labels_mst)
            self.play(FadeIn(labels_mst), run_time=0.5)
        
        with self.voiceover(text= "Like explained before we create a minimal spanning tree.") as tracker:
            # Kanten definieren, die einen MST bilden 
            edges_mst = [
            (0, 1), (1, 9), (9, 5), (5, 6), 
            (4, 9), (4, 7), (7, 8), (4,2), (2, 3), 
            ]


            line_positions_mst = {
            (0, 1): (positions_mst[0] + RIGHT * 0.3, positions_mst[1] + LEFT * 0.3),
            (1, 9): (positions_mst[1] + RIGHT * 0.3, positions_mst[9] + LEFT * 0.3),
            (9, 5): (positions_mst[9] + RIGHT * 0.3, positions_mst[5] + LEFT * 0.3),
            (5, 6): (positions_mst[5] + RIGHT * 0.3, positions_mst[6] + LEFT * 0.3),
            (9, 4): (positions_mst[9] + RIGHT * 0.2 + DOWN * 0.2, positions_mst[4] + RIGHT * 0.2 + UP * 0.2, ),
            (4, 7): (positions_mst[4] + (RIGHT+DOWN) * 0.2, positions_mst[7] + (LEFT+UP) * 0.2),
            (7, 8): (positions_mst[7] + RIGHT * 0.3, positions_mst[8] + LEFT * 0.3),
            (4, 2): (positions_mst[4] + (LEFT+DOWN) * 0.2, positions_mst[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_mst[2] + LEFT * 0.3, positions_mst[3] + RIGHT * 0.3),
            (0, 3): (positions_mst[0] + DOWN * 0.3, positions_mst[3] + UP * 0.3),
            (4, 9): (positions_mst[4] + UP * 0.2 + LEFT*0.2, positions_mst[9] + DOWN * 0.2 + LEFT*0.2),
            (6, 8): (positions_mst[6] + DOWN * 0.3, positions_mst[8] + UP * 0.3),
            (3, 2): (positions_mst[3] + RIGHT * 0.3, positions_mst[2] + LEFT * 0.3,),
            (2, 4): (positions_mst[2] + (RIGHT+UP) * 0.2, positions_mst[4] + (LEFT+DOWN) * 0.2,),
            (8, 6): (positions_mst[8] + UP * 0.3, positions_mst[6] + DOWN * 0.3),
            (6, 5): (positions_mst[6] + LEFT * 0.3, positions_mst[5] + RIGHT * 0.3),
            (9, 1): (positions_mst[9] + LEFT * 0.3, positions_mst[1] + RIGHT * 0.3),
            (1, 0): (positions_mst[1] + LEFT * 0.3, positions_mst[0] + RIGHT * 0.3),
            (5, 9): (positions_mst[5] + LEFT * 0.3, positions_mst[9] + RIGHT * 0.3),
            }
            
            lines_mst = VGroup()
            lines_to_remove = VGroup()
            edges_to_remove = [(9,4), (4,9)]
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_mst): # i muss mit aufegrufen werden, da es sich um ein Tupel handelt
                start_pos_mst, end_pos_mst = line_positions_mst[edge]

                line_mst = Line(start_pos_mst, end_pos_mst, color=WHITE)
                if edge in edges_to_remove:
                    lines_to_remove.add(line_mst)
                else:
                    lines_mst.add(line_mst)

                self.play(Create(line_mst), run_time=0.2)
        
        with self.voiceover(text= "Now we point out every node with an odd degree") as tracker:
            highlight_nodes = [0, 9, 6, 4, 3, 8]  # Knoten, die hervorgehoben werden sollen

            circles = VGroup()
            for node in highlight_nodes:
                # Position des aktuellen Knotens abrufen
                node_position = positions_mst[node]
    
                # Einen roten Kreis um den Knoten zeichnen
                highlight_circle = Circle(radius=0.5, color=RED).move_to(node_position)
                circles.add(highlight_circle)
                # Zeigen Sie den roten Kreis auf dem Bildschirm an
                self.play(Create(highlight_circle), run_time=0.5)

                
        
        with self.voiceover(text= "We can now point out the minimal perfect matching, so we add edges with the minimum weight until every node has an even degree.") as tracker:
            self.play(FadeOut(circles), run_time=0.2)
            edges_mst_2 = [
            (0, 3), (9, 4), (6, 8),  
            ]
            
            # Linien für jede Kante und Labels erstellen
            for i, edge in enumerate(edges_mst_2): # i muss mit aufegrufen werden, da es sich um ein Tupel handelt
                start_pos_mst, end_pos_mst = line_positions_mst[edge]

                line_mst = Line(start_pos_mst, end_pos_mst, color=RED)
                if edge in edges_to_remove:
                    lines_to_remove.add(line_mst)
                else:
                    lines_mst.add(line_mst)

                self.play(Create(line_mst), run_time=0.5)
        
        with self.voiceover(text= "Now we are going to find an eulerian tour which hits every edge exact once.") as tracker:
            # Kanten, die hervorgehoben werden sollen
            highlight_edges = [(0, 3), (3, 2), (2, 4), (4,7), (7,8), (8, 6), (6, 5), (5,9), (9,4), (4,9), (9, 1), (1,0)]
            
            # Texte, die den Kanten entsprechen
            texts = ["0", "→", "3", "→", "2", "→", "4", "→", "7", "→", "8", "→", "6", "→", "5", "→", "9", "→ ", "4", "→", "9", "→", "1", "", "", ""]

            # Basisposition für den ersten Text
            base_position = np.array([-5, -3, 0])  # Startposition am unteren Bildschirmrand links

            # Die Gruppe für alle Texte, um sie zu verwalten
            all_texts = VGroup()
            j = 0 

            for i, edge in enumerate(highlight_edges):
                # Positionen für die Start- und Endpunkte der Kante aus dem Dictionary abrufen
                start_pos, end_pos = line_positions_mst[edge]
                
                # Hervorgehobene Linie erstellen
                highlight_line = Line(start_pos, end_pos, color=YELLOW, stroke_width=10)
                
                # Zeigen Sie die hervorgehobene Linie auf dem Bildschirm an
                self.play(Create(highlight_line), run_time=0.2)
                
                # Aktualisieren der Basisposition für den nächsten Text, so dass er rechts vom aktuellen steht
                if j == 0:  # Ab dem zweiten Text die Position anpassen
                    text = Text(texts[j], font_size=24).move_to(base_position)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1
                else:
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1

                self.wait(1)

                self.play(FadeOut(highlight_line), run_time=0.5)
        
        with self.voiceover(text= "The last step will be to convert the euleric circle into a hamilton circle, so we have to delete all edges which make the circle visit a node which we have seen before. In our case these are the edges between 9 and 4.") as tracker:
            
            # Positionen definieren
            position_x1 = np.array([3.45, -3, 0])  # Links oben
            position_x2 = np.array([4.4, -3, 0])  # Rechts unten

            # Erstellen der "X"-Zeichen
            x_mark_1 = self.create_x_mark(position_x1)
            x_mark_2 = self.create_x_mark(position_x2)

            # Zeichnen der "X"-Zeichen
            self.play(Create(x_mark_1), Create(x_mark_2), FadeOut(lines_to_remove))

        with self.voiceover(text="If we take a look at the time complexity of the Christofides algorithm it is mainly determined by the step of finding a minimum perfect matching, which is n to the third power.") as tracker:
            self.play(FadeOut(graph_mst), 
                      FadeOut(all_texts), 
                              FadeOut(x_mark_1), 
                              FadeOut(x_mark_2),
                              FadeOut(lines_mst),
                              FadeOut(labels_mst)
                              )
            
            axes = Axes(
                x_range=[0, 20],  # x-Achsenbereich von 0 bis 5
                y_range=[0, 300], # y-Achsenbereich von 0 bis 32, um die Kurve im Diagramm zu halten
                y_length=5,
                x_length=8,
                tips=False,  
                axis_config={"include_ticks": False, "color": WHITE},  # Achsenfarbe
            )

            # Hinzufügen der Achsen und des Graphen zur Szene
            self.add(axes)
            # self.play(Create(exponential_curve), Write(exponential_label).next_to(exponential_curve, UP, buff=0.1))
            self.wait()  # Warten am Ende der Animation

            bold_template = TexTemplate()
            bold_template.add_to_preamble(r"\usepackage{bm}")

            def plot_function(function, color, label, position=RIGHT, range=[0,20]):
                function0 = axes.plot(function, x_range=range).set_stroke(width=3).set_color(color)
                return function0, Tex(label, tex_template=bold_template).set_color(color).scale(0.6).next_to(function0.point_from_proportion(1), position)
            
            # Christofides
            quad, quad_tag  = plot_function(lambda x: x**3, YELLOW, r"$\bm{O(n^3)}$ Christofides", range=[0,6.72])
            self.play(LaggedStart(quad.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(quad_tag))

            # self.wait(5)
            # # exponential
            # exp, exp_tag  = plot_function(lambda x: 2**x, BLUE, r"$\bm{O(2^n)}$", position=LEFT, range=[0,8.229])
            # self.play(LaggedStart(exp.animate.set_stroke(opacity=0.3)))
            # self.play(FadeIn(exp_tag))

            # # diagram = VGroup(axes, exp_tag, exp)
        
            # self.wait(3)
            # # exponential but a little bit faster
            # exp2, exp2_tag  = plot_function(lambda x: 2**(x-1), GREEN, r"$\bm{O(2^{n-1})}$", position=RIGHT, range=[0,9.229])
            # self.play(LaggedStart(exp2.animate.set_stroke(opacity=0.3)))
            # self.play(FadeIn(exp2_tag))

            # self.play(FadeIn(On3))
            self.wait(2)
            self.clear()
            # self.play(FadeOut(On3), FadeOut(title))
           
    def create_x_mark(self, position):
            # Erstellen eines "X" an der gegebenen Position
            line1 = Line(position + np.array([-0.25, 0.25, 0]), position + np.array([0.25, -0.25, 0]), color=RED)
            line2 = Line(position + np.array([-0.25, -0.25, 0]), position + np.array([0.25, 0.25, 0]), color=RED)
            return VGroup(line1, line2)
    



    if __name__ == "__main__":
        os.system(f"manim -pqh --disable_caching {__file__} AzureExample")