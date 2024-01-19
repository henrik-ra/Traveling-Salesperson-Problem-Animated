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

# USE CLASS CUSTOMGRAPH TO CREATE GRAPHS

# branch and bound

class GraphBaB(MovingCameraScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5]
        # edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
        #          (1, 7), (5, 7), (2, 8), (1, 9)]
        edges = [(1,2), (2,3), (3,4), (4,5), (5,1)]
        linie1 =Line(LEFT*2, RIGHT*2)
        linie2 =Line(LEFT*2, RIGHT*2)
        linie3 =Line(LEFT*2, RIGHT*2)
        linie4 =Line(LEFT*2, RIGHT*2)
        linie5 =Line(LEFT*2, RIGHT*2)

        def create_edge_from_vertex_centers(graph, start_node, end_node, buffer=0.32):
            # Berechnung der Richtung der Linie
            direction = graph.vertices[end_node].get_center() - graph.vertices[start_node].get_center()
            direction = direction / np.linalg.norm(direction) * buffer

            # Erstellen der Linie vom Rand des Startknotens zum Rand des Endknotens
            start_point = graph.vertices[start_node].get_center() + direction
            end_point = graph.vertices[end_node].get_center() - direction
            edge = Line(start_point, end_point)
            edge.set_stroke(GREY, width=3)
            return edge
        
        def draw_line (node1, node2, node3, node4, node5, node6, color):
            kreis1 = Circle(color=color, radius=0.5)
            kreis1.surround(node1)

            kreis2 = Circle(color=color, radius=0.6)
            kreis2.surround(node2)

            kreis3 = Circle(color=color)
            kreis3.surround(node3)

            kreis4 = Circle(color=color)
            kreis4.surround(node4)

            kreis5 = Circle(color=color, radius=0.7)
            kreis5.surround(node5)

            kreis6 = Circle(color=color)
            kreis6.surround(node6)

            linie1 = Line(kreis1.get_center(), kreis2.get_center(), buff=0.3)
            linie1.set_stroke(color)

            linie2 = Line(kreis2.get_center(), kreis3.get_center(), buff=0.3)
            linie2.set_stroke(color)

            linie3 = Line(kreis3.get_center(), kreis4.get_center(), buff=0.3)
            linie3.set_stroke(color)

            linie4 = Line(kreis4.get_center(), kreis5.get_center(), buff=0.3)
            linie4.set_stroke(color)

            linie5 = Line(kreis5.get_center(), kreis6.get_center(), buff=0.3)
            linie5.set_stroke(color)

            self.play(Create(linie1), run_time = 0.5)
            self.play(Create(linie2), run_time = 0.5)
            self.play(Create(linie3), run_time = 0.5)
            self.play(Create(linie4), run_time = 0.5)
            self.play(Create(linie5), run_time = 0.5)


        with self.voiceover(text="Another way of solving the TSP is with the help of the branch and bound method. Let's start with a simple TSP example. Again we have a set of cities and need to find the shortest possible route visiting each city exactly once.") as tracker:

            self.wait(3)
            bab_text = Text("Branch and Bound").shift(UP*3.5)
            self.play(Write(bab_text))

            graph = CustomGraph(vertices, edges).shift(RIGHT * 0)

            labels = graph.add_labels()

            self.wait(3.5)

            # Animate the nodes
            for vertex in graph.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            
            # Add and animate the labels
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(4)

            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(edge.animate.set_opacity(1), run_time=0.5)

            

            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(FadeOut(edge), run_time=0.5)
            

            # Group the graph and labels together
            graph_with_labels = VGroup(graph, labels) 

            self.play(
                self.camera.frame.animate.scale(1.1)
            )

            self.play(graph_with_labels.animate.shift(LEFT*5).scale(0.5), run_time=1)

            
        with self.voiceover(text="The Branch-and-Bound method begins by constructing a tree of all possibilities. First we need a Graph. Let's use the same graph and start at node one. ") as tracker:
            
            self.wait(1.5)
            self.play(FadeOut(bab_text))
            self.wait(4)

            graph2 = CustomGraph(vertices, edges).shift(RIGHT * 4)

            labels = graph2.add_labels()

            vertex_groups = {}
            for vertex in graph2.vertices:
                label = labels[vertex - 1] 
                vertex_groups[vertex] = VGroup(graph2.vertices[vertex], label)

            for vertex in graph2.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            
            # Add and animate the labels
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(2)

            kreis_um_knoten1 = Circle(color=RED)
            kreis_um_knoten1.surround(graph.vertices[1])

            # Animiere das Erscheinen des Kreises
            self.play(Create(kreis_um_knoten1))

        with self.voiceover(text="Now we have to look at the next possible nodes. In this case we have four options. We can go to node 2, 3, 4 or 5. ") as tracker:

            self.wait(3)
            kreis_um_knoten2 = Circle(color=RED)
            kreis_um_knoten2.surround(graph.vertices[2])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])
            

            # Zeichne eine rote Linie zwischen den Mittelpunkten der Kreise
            linie_zwischen_kreis1_und_2 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten2.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_2.set_color(RED)

            linie_zwischen_kreis1_und_3 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_3.set_color(RED)

            linie_zwischen_kreis1_und_4 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_4.set_color(RED)

            linie_zwischen_kreis1_und_5 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten5.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_5.set_color(RED)

            self.play(Create(linie_zwischen_kreis1_und_2))
            self.play(Create(kreis_um_knoten2))

            self.play(Create(linie_zwischen_kreis1_und_3))
            self.play(Create(kreis_um_knoten3))

            self.play(Create(linie_zwischen_kreis1_und_4))
            self.play(Create(kreis_um_knoten4))

            self.play(Create(linie_zwischen_kreis1_und_5))
            self.play(Create(kreis_um_knoten5))

            

        with self.voiceover(text="At the same time we can tranform the graph on the right to a tree with node one as the root. This tree will show all the possible routes that the salesperson can use. As explained, starting with node one the next possible nodes could be node 2, 3, 4 or 5.") as tracker:

            self.wait(3)
            
            # Bewegung von Knoten 1 in die obere Mitte
            self.play(vertex_groups[1].animate.move_to(UP * 3.75 + RIGHT * 2))

            # Bewegung der restlichen Knoten unterhalb von Knoten 1
            positions = [
                    LEFT  + UP * 2.25,  # Knoten 2
                    RIGHT + UP * 2.25,  # Knoten 3
                    RIGHT * 3 + UP * 2.25,  # Knoten 4
                    RIGHT * 5 + UP * 2.25  # Knoten 5
            ]
            for i, node in enumerate([2, 3, 4, 5], start=0):
                self.play(vertex_groups[node].animate.move_to(positions[i]))

            self.wait(5)

            # Erstellen von Kanten als Linien von Knoten 1 zu den Knoten 2, 3, 4 und 5
            for node in [2, 3, 4, 5]:
                edge = create_edge_from_vertex_centers(graph2, 1, node)
                self.play(Create(edge), run_time=0.5)

        with self.voiceover(text="This would be the first version of the tree. Now we have to take a look at the next steps. Let's say we choose node 2 as the second node to travel to.") as tracker:

            self.wait(7)
            

            linie_zwischen_kreis1_und_2_weiß = Line(kreis_um_knoten1.get_center(), kreis_um_knoten2.get_center(), buff=0.2)


            self.play(FadeOut(linie_zwischen_kreis1_und_2, 
                              linie_zwischen_kreis1_und_3, 
                              linie_zwischen_kreis1_und_4, 
                              linie_zwischen_kreis1_und_5, 
                              kreis_um_knoten1,
                              kreis_um_knoten2,
                              kreis_um_knoten3, 
                              kreis_um_knoten4, 
                              kreis_um_knoten5))
            
            self.play(Create(linie_zwischen_kreis1_und_2_weiß))


        with self.voiceover(text="Starting from node 2, the next options would be node 3, 4 or 5.") as tracker:


            kreis_um_knoten2 = Circle(color=RED)
            kreis_um_knoten2.surround(graph.vertices[2])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])
            

            # Zeichne eine rote Linie zwischen den Mittelpunkten der Kreise
            linie_zwischen_kreis2_und_3 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_3.set_color(RED)

            linie_zwischen_kreis2_und_4 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_4.set_color(RED)

            linie_zwischen_kreis2_und_5 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten5.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_5.set_color(RED)

            self.play(Create(kreis_um_knoten2))
            
            self.play(Create(linie_zwischen_kreis2_und_3))
            self.play(Create(kreis_um_knoten3))

            self.play(Create(linie_zwischen_kreis2_und_4))
            self.play(Create(kreis_um_knoten4))

            self.play(Create(linie_zwischen_kreis2_und_5))
            self.play(Create(kreis_um_knoten5))

        with self.voiceover(text="Now we can create the next step at the tree. Again the next possible nodes to travel to would be node 3, 4 and 5. ") as tracker:

            self.camera.frame.save_state()

            # Bewege die Kamera zu Knoten 2 und zoome hinein
            self.play(
                self.camera.frame.animate.move_to(LEFT * 0.5).scale(0.7)
            )

            self.wait(2)

            vertex3 = [3, 4, 5]
            graph3 = CustomGraph(vertex3, [])

            

            relative_positionen = {
                3: LEFT * 1.5 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
                4: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
                5: RIGHT * 1.5 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
            }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
            for node in vertex3:
                graph3.vertices[node].move_to(graph2.vertices[2].get_center() + relative_positionen[node])


            for vertex in graph3.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)


            for node in vertex3:
                kante_von_2_zu_node = Line(graph2.vertices[2].get_center(), graph3.vertices[node].get_center(), buff=0.3)
                kante_von_2_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_2_zu_node), run_time=0.5)

            labels = graph3.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            # Setze die Kamera zurück auf die ursprüngliche Einstellung
            self.play(Restore(self.camera.frame))


        with self.voiceover(text="Let's continue creating one possible route. We decide to travel to node 5 as our next city. ") as tracker:

            self.wait(3)

            linie_zwischen_kreis2_und_5_weiß = Line(kreis_um_knoten2.get_center(), kreis_um_knoten5.get_center(), buff=0.2)


            self.play(FadeOut(kreis_um_knoten2, linie_zwischen_kreis2_und_3, linie_zwischen_kreis2_und_4, linie_zwischen_kreis2_und_5, kreis_um_knoten3, kreis_um_knoten4, kreis_um_knoten5))
            
            self.play(Create(linie_zwischen_kreis2_und_5_weiß))



        with self.voiceover(text="Starting from node 5, there are two cities left that have not been visited yet. Node 3 and 4.") as tracker:

            self.wait(2)

            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            # Zeichne eine rote Linie zwischen den Mittelpunkten der Kreise
            linie_zwischen_kreis5_und_3 = Line(kreis_um_knoten5.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis5_und_3.set_color(RED)

            linie_zwischen_kreis5_und_4 = Line(kreis_um_knoten5.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis5_und_4.set_color(RED)

            self.play(Create(kreis_um_knoten5))

            self.play(Create(linie_zwischen_kreis5_und_3))
            self.play(Create(kreis_um_knoten3))
            
            self.play(Create(linie_zwischen_kreis5_und_4))
            self.play(Create(kreis_um_knoten4))
            


        with self.voiceover(text="Let's go back to the tree and add the last two options, node 3 and 4") as tracker:

            self.camera.frame.save_state()

            # Bewege die Kamera zu Knoten 2 und zoome hinein
            self.play(
                self.camera.frame.animate.move_to(DOWN * 1 + 0.5 * RIGHT).scale(0.7)
            )
            self.wait(4)

            vertex4 = [3, 4]
            graph4 = CustomGraph(vertex4, [])

            relative_positionen4 = {
                3: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
                4: RIGHT * 0.75 + DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
            }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
            for node in vertex4:
                graph4.vertices[node].move_to(graph3.vertices[5].get_center() + relative_positionen4[node])

            for vertex in graph4.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)


            for node in vertex4:
                kante_von_5_zu_node = Line(graph3.vertices[5].get_center(), graph4.vertices[node].get_center(), buff=0.3)
                kante_von_5_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_5_zu_node), run_time=0.5)

            labels = graph4.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            # Setze die Kamera zurück auf die ursprüngliche Einstellung
            self.play(Restore(self.camera.frame))


        with self.voiceover(text="This time we choose node 3 as the next city.") as tracker:

            self.wait(3)

            linie_zwischen_kreis5_und_3_weiß = Line(kreis_um_knoten5.get_center(), kreis_um_knoten3.get_center(), buff=0.2)


            self.play(FadeOut(kreis_um_knoten5, kreis_um_knoten3, kreis_um_knoten4, linie_zwischen_kreis5_und_3, linie_zwischen_kreis5_und_4))
            
            self.play(Create(linie_zwischen_kreis5_und_3_weiß))


        with self.voiceover(text="As you can see the last city, that we have not visited is city 4.") as tracker:

            self.wait(2)
            linie_zwischen_kreis3_und_4_weiß = Line(kreis_um_knoten3.get_center(), kreis_um_knoten4.get_center(), buff=0.2)

            self.play(Create(linie_zwischen_kreis3_und_4_weiß))


        with self.voiceover(text="Let's also add node 4 in the tree. Now we have visited every city.") as tracker:


            self.camera.frame.save_state()

            self.play(
                self.camera.frame.animate.move_to(DOWN * 2).scale(0.7)
            )

            vertex5 = [4]
            graph5 = CustomGraph(vertex5, [])

            relative_positionen5 = {
                4: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
            }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
            for node in vertex5:
                graph5.vertices[node].move_to(graph4.vertices[3].get_center() + relative_positionen5[node])

            for vertex in graph5.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)

            for node in vertex5:
                kante_von_3_zu_node = Line(graph4.vertices[3].get_center(), graph5.vertices[node].get_center(), buff=0.3)
                kante_von_3_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_3_zu_node), run_time=0.5)
            
            labels = graph5.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            self.play(Restore(self.camera.frame))

        with self.voiceover(text="At the end we have to travel to the city where we started the tour. Let's finish our route by traveling back to city 1.") as tracker:

            self.wait(3)

            linie_zwischen_kreis4_und_1_weiß = Line(kreis_um_knoten4.get_center(), kreis_um_knoten1.get_center(), buff=0.2)
            
            self.play(Create(linie_zwischen_kreis4_und_1_weiß))

        with self.voiceover(text="Now we can also finish our route on the tree by adding node 1 as our last node.") as tracker:

            self.camera.frame.save_state()

            self.play(
                self.camera.frame.animate.move_to(DOWN * 3 + RIGHT * 0.5).scale(0.7)
            )

            vertex6 = [1]
            graph6 = CustomGraph(vertex6, [])

            relative_positionen6 = {
                1: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
            }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
            for node in vertex6:
                graph6.vertices[node].move_to(graph5.vertices[4].get_center() + relative_positionen6[node])

            for vertex in graph6.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)

            for node in vertex6:
                kante_von_4_zu_node = Line(graph5.vertices[4].get_center(), graph6.vertices[node].get_center(), buff=0.3)
                kante_von_4_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_4_zu_node), run_time=0.5)
            
            labels = graph6.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            self.play(Restore(self.camera.frame))




        with self.voiceover(text="As you can see this is one possible route and the tree is not complete. Let's create the complete tree.") as tracker:

            self.wait(3)

        gesamter_baum = VGroup()

        self.camera.frame.save_state()

        self.play(
        *[FadeOut(mob)for mob in self.mobjects]
        )
            
        self.play(
            self.camera.frame.animate.scale(2.2)
        )

        vertex1_1 = [1]

        graph1_1 = CustomGraph(vertex1_1, [])

        relative_positionen1_1 = {
            1: UP * 6,         # Position von Knoten 1 relativ zu Knoten 1
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex1_1:
            graph1_1.vertices[node].move_to(relative_positionen1_1[node])

        # for vertex in graph1_1.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        labels1_1 = graph1_1.add_labels()
        self.add(labels1_1)
        # self.play(FadeIn(labels1_1), run_time=0.05)                
            
        vertex2_1 = [2, 3, 4, 5]

        graph2_1 = CustomGraph(vertex2_1, [])

        relative_positionen2_1 = {
            2: LEFT * 12 + DOWN * 2.5,  # Position von Knoten 2 relativ zu Knoten 1
            3: LEFT * 4 + DOWN * 2.5,         # Position von Knoten 3 relativ zu Knoten 1
            4: RIGHT * 4 + DOWN * 2.5,  # Position von Knoten 4 relativ zu Knoten 1
            5: RIGHT * 12 + DOWN * 2.5  # Position von Knoten 5 relativ zu Knoten 1
        }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex2_1:
            graph2_1.vertices[node].move_to(graph1_1.vertices[1].get_center() + relative_positionen2_1[node])

        # for vertex in graph2_1.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex2_1:
            kante_von_1_zu_node = Line(graph1_1.vertices[1].get_center(), graph2_1.vertices[node].get_center(), buff=0.3)
            kante_von_1_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_1_zu_node)
            # self.play(Create(kante_von_1_zu_node), run_time=0.1)

        labels2_1 = graph2_1.add_labels()
        self.add(labels2_1)
        # self.play(FadeIn(labels2_1), run_time=0.05)

        vertex3_1 = [3, 4, 5]

        graph3_1 = CustomGraph(vertex3_1, [])

        relative_positionen3_1 = {
            3: LEFT * 2.5 + DOWN * 2,  # Position von Knoten 3 relativ zu Knoten 2
            4: DOWN * 2,         # Position von Knoten 4 relativ zu Knoten 2
            5: RIGHT * 2.5 + DOWN * 2  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex3_1:
            graph3_1.vertices[node].move_to(graph2_1.vertices[2].get_center() + relative_positionen3_1[node])

        # for vertex in graph3_1.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex3_1:
            kante_von_2_zu_node = Line(graph2_1.vertices[2].get_center(), graph3_1.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels3_1 = graph3_1.add_labels()
        self.add(labels3_1)
        # self.play(FadeIn(labels3_1), run_time=0.05)

        # Vorbereitung: Sammle alle Animationsbefehle in einer Liste
        # animations = []

        # # Füge die Knoten- und Label-Animationen für jeden Graphen hinzu
        # for vertex in graph2_1.vertices.values():
        #     animations.append(GrowFromCenter(vertex))
        # animations.extend([FadeIn(label) for label in labels2_1])

        # for vertex in graph3_1.vertices.values():
        #     animations.append(GrowFromCenter(vertex))
        # animations.extend([FadeIn(label) for label in labels3_1])

        # # Füge die Kantenanimationen hinzu
        # for node in vertex2_1:
        #     kante_von_1_zu_node = Line(graph1_1.vertices[1].get_center(), graph2_1.vertices[node].get_center(), buff=0.3)
        #     kante_von_1_zu_node.set_stroke(WHITE, width=2)
        #     animations.append(Create(kante_von_1_zu_node))

        # for node in vertex3_1:
        #     kante_von_2_zu_node = Line(graph2_1.vertices[2].get_center(), graph3_1.vertices[node].get_center(), buff=0.3)
        #     kante_von_2_zu_node.set_stroke(WHITE, width=2)
        #     animations.append(Create(kante_von_2_zu_node))

        # # Spiele alle Animationen gleichzeitig ab mit einer Gesamtdauer von einer Sekunde
        # self.play(*animations, run_time=1)


        # big_graph = VGroup(graph1_1, graph2_1, graph3_1, labels1_1, labels2_1, labels3_1)
        # self.play(FadeIn(big_graph), run_time=0.1)


        vertex3_2 = [2, 4, 5]

        graph3_2 = CustomGraph(vertex3_2, [])

        relative_positionen3_2 = {
            2: LEFT * 2.5 + DOWN * 2,  # Position von Knoten 2 relativ zu Knoten 3
            4: DOWN * 2,         # Position von Knoten 4 relativ zu Knoten 3
            5: RIGHT * 2.5 + DOWN * 2  # Position von Knoten 5 relativ zu Knoten 3
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex3_2:
            graph3_2.vertices[node].move_to(graph2_1.vertices[3].get_center() + relative_positionen3_2[node])

        # for vertex in graph3_2.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex3_2:
            kante_von_3_zu_node = Line(graph2_1.vertices[3].get_center(), graph3_2.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)


        labels3_2 = graph3_2.add_labels()
        self.add(labels3_2)
        # self.play(FadeIn(labels3_2), run_time=0.05)

        vertex3_3 = [2, 3, 5]

        graph3_3 = CustomGraph(vertex3_3, [])

        relative_positionen3_3 = {
            2: LEFT * 2.5 + DOWN * 2,  # Position von Knoten 2 relativ zu Knoten 4
            3: DOWN * 2,         # Position von Knoten 3 relativ zu Knoten 4
            5: RIGHT * 2.5 + DOWN * 2  # Position von Knoten 5 relativ zu Knoten 4
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex3_3:
            graph3_3.vertices[node].move_to(graph2_1.vertices[4].get_center() + relative_positionen3_3[node])

        # for vertex in graph3_3.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex3_3:
            kante_von_4_zu_node = Line(graph2_1.vertices[4].get_center(), graph3_3.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels3_3 = graph3_3.add_labels()
        self.add(labels3_3)
        # self.play(FadeIn(labels3_3), run_time=0.05)

        vertex3_4 = [2, 3, 4]

        graph3_4 = CustomGraph(vertex3_4, [])

        relative_positionen3_4 = {
            2: LEFT * 2.5 + DOWN * 2,  # Position von Knoten 2 relativ zu Knoten 5
            3: DOWN * 2,         # Position von Knoten 3 relativ zu Knoten 5
            4: RIGHT * 2.5 + DOWN * 2  # Position von Knoten 4 relativ zu Knoten 5
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex3_4:
            graph3_4.vertices[node].move_to(graph2_1.vertices[5].get_center() + relative_positionen3_4[node])

        # for vertex in graph3_4.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex3_4:
            kante_von_5_zu_node = Line(graph2_1.vertices[5].get_center(), graph3_4.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels3_4 = graph3_4.add_labels()
        self.add(labels3_4)
        # self.play(FadeIn(labels3_4), run_time=0.05)


        vertex4_1 = [4, 5]

        graph4_1 = CustomGraph(vertex4_1, [])

        relative_positionen4_1 = {
            4: LEFT * 0.75 + DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex4_1:
            graph4_1.vertices[node].move_to(graph3_1.vertices[3].get_center() + relative_positionen4_1[node])

        # for vertex in graph4_1.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_1:
            kante_von_3_zu_node = Line(graph3_1.vertices[3].get_center(), graph4_1.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels4_1 = graph4_1.add_labels()
        self.add(labels4_1)
        # self.play(FadeIn(labels4_1), run_time=0.02)

        vertex4_2 = [3, 5]	

        graph4_2 = CustomGraph(vertex4_2, [])

        relative_positionen4_2 = {
            3: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex4_2:
            graph4_2.vertices[node].move_to(graph3_1.vertices[4].get_center() + relative_positionen4_2[node])

        # for vertex in graph4_2.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_2:
            kante_von_2_zu_node = Line(graph3_1.vertices[4].get_center(), graph4_2.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels4_2 = graph4_2.add_labels()
        self.add(labels4_2)
        # self.play(FadeIn(labels4_2), run_time=0.02)

        vertex4_3 = [3, 4]

        graph4_3 = CustomGraph(vertex4_3, [])

        relative_positionen4_3 = {
            3: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
            4: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex4_3:
            graph4_3.vertices[node].move_to(graph3_1.vertices[5].get_center() + relative_positionen4_3[node])

        # for vertex in graph4_3.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_3:
            kante_von_2_zu_node = Line(graph3_1.vertices[5].get_center(), graph4_3.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels4_3 = graph4_3.add_labels()
        self.add(labels4_3)
        # self.play(FadeIn(labels4_3), run_time=0.02)

        vertex4_4 = [4,5]

        graph4_4 = CustomGraph(vertex4_4, [])

        relative_positionen4_4 = {
            4: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 4 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex4_4:
            graph4_4.vertices[node].move_to(graph3_2.vertices[2].get_center() + relative_positionen4_4[node])

        # for vertex in graph4_4.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_4:
            kante_von_2_zu_node = Line(graph3_2.vertices[2].get_center(), graph4_4.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels4_4 = graph4_4.add_labels()
        self.add(labels4_4)
        # self.play(FadeIn(labels4_4), run_time=0.02)

        vertex4_5 = [2, 5]

        graph4_5 = CustomGraph(vertex4_5, [])

        relative_positionen4_5 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph4 angeordnet sind
        for node in vertex4_5:
            graph4_5.vertices[node].move_to(graph3_2.vertices[4].get_center() + relative_positionen4_5[node])

        # for vertex in graph4_5.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_5:
            kante_von_4_zu_node = Line(graph3_2.vertices[4].get_center(), graph4_5.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.04)

        labels4_5 = graph4_5.add_labels()
        self.add(labels4_5)
        # self.play(FadeIn(labels4_5), run_time=0.02)

        vertex4_6 = [2, 4]

        graph4_6 = CustomGraph(vertex4_6, [])

        relative_positionen4_6 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            4: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph4 angeordnet sind
        for node in vertex4_6:
            graph4_6.vertices[node].move_to(graph3_2.vertices[5].get_center() + relative_positionen4_6[node])

        # for vertex in graph4_6.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_6:
            kante_von_4_zu_node = Line(graph3_2.vertices[5].get_center(), graph4_6.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.04)

        labels4_6 = graph4_6.add_labels()
        self.add(labels4_6)
        # self.play(FadeIn(labels4_6), run_time=0.02)

        vertex4_7 = [3, 5]

        graph4_7 = CustomGraph(vertex4_7, [])

        relative_positionen4_7 = {
            3: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph4 angeordnet sind
        for node in vertex4_7:
            graph4_7.vertices[node].move_to(graph3_3.vertices[2].get_center() + relative_positionen4_7[node])
            
        # for vertex in graph4_7.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_7:
            kante_von_2_zu_node = Line(graph3_3.vertices[2].get_center(), graph4_7.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels4_7 = graph4_7.add_labels()
        self.add(labels4_7)
        # self.play(FadeIn(labels4_7), run_time=0.02)

        vertex4_8 = [2, 5]

        graph4_8 = CustomGraph(vertex4_8, [])

        relative_positionen4_8 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            5: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 5 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph4 angeordnet sind
        for node in vertex4_8:
            graph4_8.vertices[node].move_to(graph3_3.vertices[3].get_center() + relative_positionen4_8[node])

        # for vertex in graph4_8.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_8:
            kante_von_3_zu_node = Line(graph3_3.vertices[3].get_center(), graph4_8.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels4_8 = graph4_8.add_labels()
        self.add(labels4_8)
        # self.play(FadeIn(labels4_8), run_time=0.02)

        vertex4_9 = [2, 3]

        graph4_9 = CustomGraph(vertex4_9, [])

        relative_positionen4_9 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            3: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 3 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph4 angeordnet sind
        for node in vertex4_9:
            graph4_9.vertices[node].move_to(graph3_3.vertices[5].get_center() + relative_positionen4_9[node])

        # for vertex in graph4_9.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_9:
            kante_von_3_zu_node = Line(graph3_3.vertices[5].get_center(), graph4_9.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels4_9 = graph4_9.add_labels()
        self.add(labels4_9)
        # self.play(FadeIn(labels4_9), run_time=0.02)

        vertex4_10 = [3, 4]

        graph4_10 = CustomGraph(vertex4_10, [])

        relative_positionen4_10 = {
            3: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 3 relativ zu Knoten 2
            4: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph4 angeordnet sind
        for node in vertex4_10:
            graph4_10.vertices[node].move_to(graph3_4.vertices[2].get_center() + relative_positionen4_10[node])

        # for vertex in graph4_10.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)
            
        for node in vertex4_10:
            kante_von_2_zu_node = Line(graph3_4.vertices[2].get_center(), graph4_10.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels4_10 = graph4_10.add_labels()
        self.add(labels4_10)
        # self.play(FadeIn(labels4_10), run_time=0.02)

        vertex4_11 = [2, 4]
            
        graph4_11 = CustomGraph(vertex4_11, [])

        relative_positionen4_11 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            4: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 4 relativ zu Knoten 2
        }

            # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph4 angeordnet sind
        for node in vertex4_11:
            graph4_11.vertices[node].move_to(graph3_4.vertices[3].get_center() + relative_positionen4_11[node])

        # for vertex in graph4_11.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_11:
            kante_von_3_zu_node = Line(graph3_4.vertices[3].get_center(), graph4_11.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels4_11 = graph4_11.add_labels()
        self.add(labels4_11)
        # self.play(FadeIn(labels4_11), run_time=0.02)

        vertex4_12 = [2, 3]
            
        graph4_12 = CustomGraph(vertex4_12, [])

        relative_positionen4_12 = {
            2: LEFT * 0.75 + DOWN * 1.5,  # Position von Knoten 2 relativ zu Knoten 2
            3: RIGHT * 0.75 + DOWN * 1.5  # Position von Knoten 3 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph4 angeordnet sind
        for node in vertex4_12:
            graph4_12.vertices[node].move_to(graph3_4.vertices[4].get_center() + relative_positionen4_12[node])

        # for vertex in graph4_12.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex4_12:
            kante_von_3_zu_node = Line(graph3_4.vertices[4].get_center(), graph4_12.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels4_12 = graph4_12.add_labels()
        self.add(labels4_12)
        # self.play(FadeIn(labels4_12), run_time=0.02)

        vertex5_1 = [5]

        graph5_1 = CustomGraph(vertex5_1, [])

        relative_positionen5_1 = {
            5: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 2 von graph2 angeordnet sind
        for node in vertex5_1:
            graph5_1.vertices[node].move_to(graph4_1.vertices[4].get_center() + relative_positionen5_1[node])

        # for vertex in graph5_1.vertices.values():
            # self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_1:
            kante_von_4_zu_node = Line(graph4_1.vertices[4].get_center(), graph5_1.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.04)

        labels5_1 = graph5_1.add_labels()
        self.add(labels5_1)
        # self.play(FadeIn(labels5_1), run_time=0.02)

        vertex5_2 = [4]

        graph5_2 = CustomGraph(vertex5_2, [])

        relative_positionen5_2 = {
            4: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind
        for node in vertex5_2:
            graph5_2.vertices[node].move_to(graph4_1.vertices[5].get_center() + relative_positionen5_2[node])

        # for vertex in graph5_2.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_2:
            kante_von_2_zu_node = Line(graph4_1.vertices[5].get_center(), graph5_2.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels5_2 = graph5_2.add_labels()
        self.add(labels5_2)
        # self.play(FadeIn(labels5_2), run_time=0.02)

        vertex5_3 = [5]

        graph5_3 = CustomGraph(vertex5_3, [])

        relative_positionen5_3 = {
            5: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind
        for node in vertex5_3:
            graph5_3.vertices[node].move_to(graph4_2.vertices[3].get_center() + relative_positionen5_3[node])

        # for vertex in graph5_3.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_3:
            kante_von_4_zu_node = Line(graph4_2.vertices[3].get_center(), graph5_3.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.04)

        labels5_3 = graph5_3.add_labels()
        self.add(labels5_3)
        # self.play(FadeIn(labels5_3), run_time=0.02)

        vertex5_4 = [3]

        graph5_4 = CustomGraph(vertex5_4, [])

        relative_positionen5_4 = {
            3: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind
        for node in vertex5_4:
            graph5_4.vertices[node].move_to(graph4_2.vertices[5].get_center() + relative_positionen5_4[node])

        # for vertex in graph5_4.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_4:
            kante_von_2_zu_node = Line(graph4_2.vertices[5].get_center(), graph5_4.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels5_4 = graph5_4.add_labels()
        self.add(labels5_4)
        # self.play(FadeIn(labels5_4), run_time=0.02)

        vertex5_5 = [4]

        graph5_5 = CustomGraph(vertex5_5, [])

        relative_positionen5_5 = {
            4: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind

        for node in vertex5_5:
            graph5_5.vertices[node].move_to(graph4_3.vertices[3].get_center() + relative_positionen5_5[node])

        # for vertex in graph5_5.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_5:
            kante_von_3_zu_node = Line(graph4_3.vertices[3].get_center(), graph5_5.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.04)

        labels5_5 = graph5_5.add_labels()
        self.add(labels5_5)
        # self.play(FadeIn(labels5_5), run_time=0.02)

        vertex5_6 = [3]

        graph5_6 = CustomGraph(vertex5_6, [])

        relative_positionen5_6 = {
            3: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind

        for node in vertex5_6:
            graph5_6.vertices[node].move_to(graph4_3.vertices[4].get_center() + relative_positionen5_6[node])

        # for vertex in graph5_6.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_6:
            kante_von_2_zu_node = Line(graph4_3.vertices[4].get_center(), graph5_6.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels5_6 = graph5_6.add_labels()
        self.add(labels5_6)
        # self.play(FadeIn(labels5_6), run_time=0.02)

        vertex5_7 = [5]

        graph5_7 = CustomGraph(vertex5_7, [])

        relative_positionen5_7 = {
            5: DOWN * 1.5,         # Position von Knoten 4 relativ zu Knoten 2
        }

        # Verschiebe graph3 so, dass Knoten 3, 4 und 5 um Knoten 4 von graph2 angeordnet sind

        for node in vertex5_7:
            graph5_7.vertices[node].move_to(graph4_4.vertices[4].get_center() + relative_positionen5_7[node])

        # for vertex in graph5_7.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.02)

        for node in vertex5_7:
            kante_von_2_zu_node = Line(graph4_4.vertices[4].get_center(), graph5_7.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.04)

        labels5_7 = graph5_7.add_labels()
        self.add(labels5_7)
        # self.play(FadeIn(labels5_7), run_time=0.02)

        vertex5_8 = [4]
        graph5_8 = CustomGraph(vertex5_8, [])
        relative_positionen5_8 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_8:
            graph5_8.vertices[node].move_to(graph4_4.vertices[5].get_center() + relative_positionen5_8[node])

        # for vertex in graph5_8.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_8:
            kante_von_3_zu_node = Line(graph4_4.vertices[5].get_center(), graph5_8.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)

        labels5_8 = graph5_8.add_labels()
        self.add(labels5_8)
        # self.play(FadeIn(labels5_8), run_time=0.05)

        vertex5_9 = [5]
        graph5_9 = CustomGraph(vertex5_9, [])
        relative_positionen5_9 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_9:
            graph5_9.vertices[node].move_to(graph4_5.vertices[2].get_center() + relative_positionen5_9[node])

        # for vertex in graph5_9.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_9:
            kante_von_2_zu_node = Line(graph4_5.vertices[2].get_center(), graph5_9.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_9 = graph5_9.add_labels()
        self.add(labels5_9)
        # self.play(FadeIn(labels5_9), run_time=0.05)

        vertex5_10 = [2]
        graph5_10 = CustomGraph(vertex5_10, [])
        relative_positionen5_10 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_10:
            graph5_10.vertices[node].move_to(graph4_5.vertices[5].get_center() + relative_positionen5_10[node])

        # for vertex in graph5_10.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_10:
            kante_von_3_zu_node = Line(graph4_5.vertices[5].get_center(), graph5_10.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)

        labels5_10 = graph5_10.add_labels()
        self.add(labels5_10)
        # self.play(FadeIn(labels5_10), run_time=0.05)

        vertex5_11 = [4]
        graph5_11 = CustomGraph(vertex5_11, [])
        relative_positionen5_11 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_11:
            graph5_11.vertices[node].move_to(graph4_6.vertices[2].get_center() + relative_positionen5_11[node])

        # for vertex in graph5_11.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_11:
            kante_von_2_zu_node = Line(graph4_6.vertices[2].get_center(), graph5_11.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_11 = graph5_11.add_labels()
        self.add(labels5_11)
        # self.play(FadeIn(labels5_11), run_time=0.05)

        vertex5_12 = [2]
        graph5_12 = CustomGraph(vertex5_12, [])
        relative_positionen5_12 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_12:
            graph5_12.vertices[node].move_to(graph4_6.vertices[4].get_center() + relative_positionen5_12[node])

        # for vertex in graph5_12.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_12:
            kante_von_4_zu_node = Line(graph4_6.vertices[4].get_center(), graph5_12.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels5_12 = graph5_12.add_labels()
        self.add(labels5_12)
        # self.play(FadeIn(labels5_12), run_time=0.05)

        vertex5_13 = [5]
        graph5_13 = CustomGraph(vertex5_13, [])
        relative_positionen5_13 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_13:
            graph5_13.vertices[node].move_to(graph4_7.vertices[3].get_center() + relative_positionen5_13[node])

        # for vertex in graph5_13.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_13:
            kante_von_4_zu_node = Line(graph4_7.vertices[3].get_center(), graph5_13.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels5_13 = graph5_13.add_labels()
        self.add(labels5_13)
        # self.play(FadeIn(labels5_13), run_time=0.05)

        vertex5_14 = [3]
        graph5_14 = CustomGraph(vertex5_14, [])
        relative_positionen5_14 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_14:
            graph5_14.vertices[node].move_to(graph4_7.vertices[5].get_center() + relative_positionen5_14[node])

        # for vertex in graph5_14.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_14:
            kante_von_4_zu_node = Line(graph4_7.vertices[5].get_center(), graph5_14.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels5_14 = graph5_14.add_labels()
        self.add(labels5_14)
        # self.play(FadeIn(labels5_14), run_time=0.05)

        vertex5_15 = [5]
        graph5_15 = CustomGraph(vertex5_15, [])
        relative_positionen5_15 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_15:
            graph5_15.vertices[node].move_to(graph4_8.vertices[2].get_center() + relative_positionen5_15[node])

        # for vertex in graph5_15.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_15:
            kante_von_2_zu_node = Line(graph4_8.vertices[2].get_center(), graph5_15.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_15 = graph5_15.add_labels()
        self.add(labels5_15)
        # self.play(FadeIn(labels5_15), run_time=0.05)

        vertex5_16 = [2]
        graph5_16 = CustomGraph(vertex5_16, [])
        relative_positionen5_16 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_16:
            graph5_16.vertices[node].move_to(graph4_8.vertices[5].get_center() + relative_positionen5_16[node])

        # for vertex in graph5_16.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_16:
            kante_von_3_zu_node = Line(graph4_8.vertices[5].get_center(), graph5_16.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)

        labels5_16 = graph5_16.add_labels()
        self.add(labels5_16)
        # self.play(FadeIn(labels5_16), run_time=0.05)

        vertex5_17 = [3]
        graph5_17 = CustomGraph(vertex5_17, [])
        relative_positionen5_17 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_17:
            graph5_17.vertices[node].move_to(graph4_9.vertices[2].get_center() + relative_positionen5_17[node])

        # for vertex in graph5_17.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_17:
            kante_von_2_zu_node = Line(graph4_9.vertices[2].get_center(), graph5_17.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_17 = graph5_17.add_labels()
        self.add(labels5_17)
        # self.play(FadeIn(labels5_17), run_time=0.05)

        vertex5_18 = [2]
        graph5_18 = CustomGraph(vertex5_18, [])
        relative_positionen5_18 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_18:
            graph5_18.vertices[node].move_to(graph4_9.vertices[3].get_center() + relative_positionen5_18[node])

        # for vertex in graph5_18.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_18:
            kante_von_3_zu_node = Line(graph4_9.vertices[3].get_center(), graph5_18.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)

        labels5_18 = graph5_18.add_labels()
        self.add(labels5_18)
        # self.play(FadeIn(labels5_18), run_time=0.05)

        vertex5_19 = [4]
        graph5_19 = CustomGraph(vertex5_19, [])
        relative_positionen5_19 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_19:
            graph5_19.vertices[node].move_to(graph4_10.vertices[3].get_center() + relative_positionen5_19[node])

        # for vertex in graph5_19.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_19:
            kante_von_2_zu_node = Line(graph4_10.vertices[3].get_center(), graph5_19.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_19 = graph5_19.add_labels()
        self.add(labels5_19)
        # self.play(FadeIn(labels5_19), run_time=0.05)

        vertex5_20 = [3]
        graph5_20 = CustomGraph(vertex5_20, [])
        relative_positionen5_20 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_20:
            graph5_20.vertices[node].move_to(graph4_10.vertices[4].get_center() + relative_positionen5_20[node])

        # for vertex in graph5_20.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_20:
            kante_von_4_zu_node = Line(graph4_10.vertices[4].get_center(), graph5_20.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels5_20 = graph5_20.add_labels()
        self.add(labels5_20)
        # self.play(FadeIn(labels5_20), run_time=0.05)

        vertex5_21 = [4]
        graph5_21 = CustomGraph(vertex5_21, [])
        relative_positionen5_21 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_21:
            graph5_21.vertices[node].move_to(graph4_11.vertices[2].get_center() + relative_positionen5_21[node])

        # for vertex in graph5_21.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_21:
            kante_von_2_zu_node = Line(graph4_11.vertices[2].get_center(), graph5_21.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_21 = graph5_21.add_labels()
        self.add(labels5_21)
        # self.play(FadeIn(labels5_21), run_time=0.05)

        vertex5_22 = [2]
        graph5_22 = CustomGraph(vertex5_22, [])
        relative_positionen5_22 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_22:
            graph5_22.vertices[node].move_to(graph4_11.vertices[4].get_center() + relative_positionen5_22[node])

        # for vertex in graph5_22.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_22:
            kante_von_4_zu_node = Line(graph4_11.vertices[4].get_center(), graph5_22.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)
            # self.play(Create(kante_von_4_zu_node), run_time=0.1)

        labels5_22 = graph5_22.add_labels()
        self.add(labels5_22)
        # self.play(FadeIn(labels5_22), run_time=0.05)

        vertex5_23 = [3]
        graph5_23 = CustomGraph(vertex5_23, [])
        relative_positionen5_23 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_23:
            graph5_23.vertices[node].move_to(graph4_12.vertices[2].get_center() + relative_positionen5_23[node])

        # for vertex in graph5_23.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex5_23:
            kante_von_2_zu_node = Line(graph4_12.vertices[2].get_center(), graph5_23.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)
            # self.play(Create(kante_von_2_zu_node), run_time=0.1)

        labels5_23 = graph5_23.add_labels()
        self.add(labels5_23)
        # self.play(FadeIn(labels5_23), run_time=0.05)

        vertex5_24 = [2]
        graph5_24 = CustomGraph(vertex5_24, [])
        relative_positionen5_24 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_24:
            graph5_24.vertices[node].move_to(graph4_12.vertices[3].get_center() + relative_positionen5_24[node])

        # for vertex in graph5_24.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)
        
        for node in vertex5_24:
            kante_von_3_zu_node = Line(graph4_12.vertices[3].get_center(), graph5_24.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)
            # self.play(Create(kante_von_3_zu_node), run_time=0.1)

        labels5_24 = graph5_24.add_labels()
        self.add(labels5_24)
        # self.play(FadeIn(labels5_24), run_time=0.05)

        # node one as last node

        vertex6_1 = [1]
        graph6_1 = CustomGraph(vertex6_1, [])
        relative_positionen6_1 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_1:
            graph6_1.vertices[node].move_to(graph5_1.vertices[5].get_center() + relative_positionen6_1[node])

        # for vertex in graph6_1.vertices.values():
            # self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_1:
            kante_von_5_zu_node = Line(graph5_1.vertices[5].get_center(), graph6_1.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_1 = graph6_1.add_labels()
        self.add(labels6_1)
        # self.play(FadeIn(labels6_1), run_time=0.05)

        vertex6_2 = [1]
        graph6_2 = CustomGraph(vertex6_2, [])
        relative_positionen6_2 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_2:
            graph6_2.vertices[node].move_to(graph5_2.vertices[4].get_center() + relative_positionen6_2[node])

        # for vertex in graph6_2.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_2:
            kante_von_5_zu_node = Line(graph5_2.vertices[4].get_center(), graph6_2.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_2 = graph6_2.add_labels()
        self.add(labels6_2)
        # self.play(FadeIn(labels6_2), run_time=0.05)

        vertex6_3 = [1]
        graph6_3 = CustomGraph(vertex6_3, [])
        relative_positionen6_3 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_3:
            graph6_3.vertices[node].move_to(graph5_3.vertices[5].get_center() + relative_positionen6_3[node])

        # for vertex in graph6_3.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_3:
            kante_von_5_zu_node = Line(graph5_3.vertices[5].get_center(), graph6_3.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_3 = graph6_3.add_labels()
        self.add(labels6_3)
        # self.play(FadeIn(labels6_3), run_time=0.05)

        vertex6_4 = [1]
        graph6_4 = CustomGraph(vertex6_4, [])
        relative_positionen6_4 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_4:
            graph6_4.vertices[node].move_to(graph5_4.vertices[3].get_center() + relative_positionen6_4[node])

        # for vertex in graph6_4.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_4:
            kante_von_5_zu_node = Line(graph5_4.vertices[3].get_center(), graph6_4.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_4 = graph6_4.add_labels()
        self.add(labels6_4)
        # self.play(FadeIn(labels6_4), run_time=0.05)

        vertex6_5 = [1]
        graph6_5 = CustomGraph(vertex6_5, [])
        relative_positionen6_5 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_5:
            graph6_5.vertices[node].move_to(graph5_5.vertices[4].get_center() + relative_positionen6_5[node])

        # for vertex in graph6_5.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_5:
            kante_von_5_zu_node = Line(graph5_5.vertices[4].get_center(), graph6_5.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_5 = graph6_5.add_labels()
        self.add(labels6_5)
        # self.play(FadeIn(labels6_5), run_time=0.05)

        vertex6_6 = [1]
        graph6_6 = CustomGraph(vertex6_6, [])
        relative_positionen6_6 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_6:
            graph6_6.vertices[node].move_to(graph5_6.vertices[3].get_center() + relative_positionen6_6[node])

        # for vertex in graph6_6.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_6:
            kante_von_5_zu_node = Line(graph5_6.vertices[3].get_center(), graph6_6.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_6 = graph6_6.add_labels()
        self.add(labels6_6)
        # self.play(FadeIn(labels6_6), run_time=0.05)

        vertex6_7 = [1]
        graph6_7 = CustomGraph(vertex6_7, [])
        relative_positionen6_7 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_7:
            graph6_7.vertices[node].move_to(graph5_7.vertices[5].get_center() + relative_positionen6_7[node])

        # for vertex in graph6_7.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_7:
            kante_von_5_zu_node = Line(graph5_7.vertices[5].get_center(), graph6_7.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_7 = graph6_7.add_labels()
        self.add(labels6_7)
        # self.play(FadeIn(labels6_7), run_time=0.05)

        vertex6_8 = [1]
        graph6_8 = CustomGraph(vertex6_8, [])
        relative_positionen6_8 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_8:
            graph6_8.vertices[node].move_to(graph5_8.vertices[4].get_center() + relative_positionen6_8[node])

        # for vertex in graph6_8.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_8:
            kante_von_5_zu_node = Line(graph5_8.vertices[4].get_center(), graph6_8.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_8 = graph6_8.add_labels()
        self.add(labels6_8)
        # self.play(FadeIn(labels6_8), run_time=0.05)

        vertex6_9 = [1]
        graph6_9 = CustomGraph(vertex6_9, [])
        relative_positionen6_9 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_9:
            graph6_9.vertices[node].move_to(graph5_9.vertices[5].get_center() + relative_positionen6_9[node])
        
        # for vertex in graph6_9.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_9:
            kante_von_5_zu_node = Line(graph5_9.vertices[5].get_center(), graph6_9.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_9 = graph6_9.add_labels()
        self.add(labels6_9)
        # self.play(FadeIn(labels6_9), run_time=0.05)

        vertex6_10 = [1]
        graph6_10 = CustomGraph(vertex6_10, [])
        relative_positionen6_10 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_10:
            graph6_10.vertices[node].move_to(graph5_10.vertices[2].get_center() + relative_positionen6_10[node])

        # for vertex in graph6_10.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_10:
            kante_von_5_zu_node = Line(graph5_10.vertices[2].get_center(), graph6_10.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_10 = graph6_10.add_labels()
        self.add(labels6_10)
        # self.play(FadeIn(labels6_10), run_time=0.05)

        vertex6_11 = [1]
        graph6_11 = CustomGraph(vertex6_11, [])
        relative_positionen6_11 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_11:
            graph6_11.vertices[node].move_to(graph5_11.vertices[4].get_center() + relative_positionen6_11[node])

        # for vertex in graph6_11.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_11:
            kante_von_5_zu_node = Line(graph5_11.vertices[4].get_center(), graph6_11.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_11 = graph6_11.add_labels()
        self.add(labels6_11)
        # self.play(FadeIn(labels6_11), run_time=0.05)

        vertex6_12 = [1]
        graph6_12 = CustomGraph(vertex6_12, [])
        relative_positionen6_12 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_12:
            graph6_12.vertices[node].move_to(graph5_12.vertices[2].get_center() + relative_positionen6_12[node])

        # for vertex in graph6_12.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_12:
            kante_von_5_zu_node = Line(graph5_12.vertices[2].get_center(), graph6_12.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_12 = graph6_12.add_labels()
        self.add(labels6_12)
        # self.play(FadeIn(labels6_12), run_time=0.05)

        vertex6_13 = [1]
        graph6_13 = CustomGraph(vertex6_13, [])
        relative_positionen6_13 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_13:
            graph6_13.vertices[node].move_to(graph5_13.vertices[5].get_center() + relative_positionen6_13[node])

        # for vertex in graph6_13.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_13:
            kante_von_5_zu_node = Line(graph5_13.vertices[5].get_center(), graph6_13.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_13 = graph6_13.add_labels()
        self.add(labels6_13)
        # self.play(FadeIn(labels6_13), run_time=0.05)

        vertex6_14 = [1]
        graph6_14 = CustomGraph(vertex6_14, [])
        relative_positionen6_14 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_14:
            graph6_14.vertices[node].move_to(graph5_14.vertices[3].get_center() + relative_positionen6_14[node])

        # for vertex in graph6_14.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_14:
            kante_von_5_zu_node = Line(graph5_14.vertices[3].get_center(), graph6_14.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_14 = graph6_14.add_labels()
        self.add(labels6_14)
        # self.play(FadeIn(labels6_14), run_time=0.05)

        vertex6_15 = [1]
        graph6_15 = CustomGraph(vertex6_15, [])
        relative_positionen6_15 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_15:
            graph6_15.vertices[node].move_to(graph5_15.vertices[5].get_center() + relative_positionen6_15[node])

        # for vertex in graph6_15.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_15:
            kante_von_5_zu_node = Line(graph5_15.vertices[5].get_center(), graph6_15.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_15 = graph6_15.add_labels()
        self.add(labels6_15)
        # self.play(FadeIn(labels6_15), run_time=0.05)

        vertex6_16 = [1]
        graph6_16 = CustomGraph(vertex6_16, [])
        relative_positionen6_16 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_16:
            graph6_16.vertices[node].move_to(graph5_16.vertices[2].get_center() + relative_positionen6_16[node])

        # for vertex in graph6_16.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_16:
            kante_von_5_zu_node = Line(graph5_16.vertices[2].get_center(), graph6_16.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_16 = graph6_16.add_labels()
        self.add(labels6_16)
        # self.play(FadeIn(labels6_16), run_time=0.05)

        vertex6_17 = [1]
        graph6_17 = CustomGraph(vertex6_17, [])
        relative_positionen6_17 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_17:
            graph6_17.vertices[node].move_to(graph5_17.vertices[3].get_center() + relative_positionen6_17[node])

        # for vertex in graph6_17.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_17:
            kante_von_5_zu_node = Line(graph5_17.vertices[3].get_center(), graph6_17.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_17 = graph6_17.add_labels()
        self.add(labels6_17)
        # self.play(FadeIn(labels6_17), run_time=0.05)

        vertex6_18 = [1]
        graph6_18 = CustomGraph(vertex6_18, [])
        relative_positionen6_18 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_18:
            graph6_18.vertices[node].move_to(graph5_18.vertices[2].get_center() + relative_positionen6_18[node])

        # for vertex in graph6_18.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_18:
            kante_von_5_zu_node = Line(graph5_18.vertices[2].get_center(), graph6_18.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_18 = graph6_18.add_labels()
        self.add(labels6_18)
        # self.play(FadeIn(labels6_18), run_time=0.05)

        vertex6_19 = [1]
        graph6_19 = CustomGraph(vertex6_19, [])
        relative_positionen6_19 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_19:
            graph6_19.vertices[node].move_to(graph5_19.vertices[4].get_center() + relative_positionen6_19[node])

        # for vertex in graph6_19.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_19:
            kante_von_5_zu_node = Line(graph5_19.vertices[4].get_center(), graph6_19.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_19 = graph6_19.add_labels()
        self.add(labels6_19)
        # self.play(FadeIn(labels6_19), run_time=0.05)

        vertex6_20 = [1]
        graph6_20 = CustomGraph(vertex6_20, [])
        relative_positionen6_20 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_20:
            graph6_20.vertices[node].move_to(graph5_20.vertices[3].get_center() + relative_positionen6_20[node])

        # for vertex in graph6_20.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_20:
            kante_von_5_zu_node = Line(graph5_20.vertices[3].get_center(), graph6_20.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_20 = graph6_20.add_labels()
        self.add(labels6_20)
        # self.play(FadeIn(labels6_20), run_time=0.05)

        vertex6_21 = [1]
        graph6_21 = CustomGraph(vertex6_21, [])
        relative_positionen6_21 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_21:
            graph6_21.vertices[node].move_to(graph5_21.vertices[4].get_center() + relative_positionen6_21[node])

        # for vertex in graph6_21.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)
        
        for node in vertex6_21:
            kante_von_5_zu_node = Line(graph5_21.vertices[4].get_center(), graph6_21.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_21 = graph6_21.add_labels()
        self.add(labels6_21)
        # self.play(FadeIn(labels6_21), run_time=0.05)

        vertex6_22 = [1]
        graph6_22 = CustomGraph(vertex6_22, [])
        relative_positionen6_22 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_22:
            graph6_22.vertices[node].move_to(graph5_22.vertices[2].get_center() + relative_positionen6_22[node])

        # for vertex in graph6_22.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_22:
            kante_von_5_zu_node = Line(graph5_22.vertices[2].get_center(), graph6_22.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_22 = graph6_22.add_labels()
        self.add(labels6_22)
        # self.play(FadeIn(labels6_22), run_time=0.05)

        vertex6_23 = [1]
        graph6_23 = CustomGraph(vertex6_23, [])
        relative_positionen6_23 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_23:
            graph6_23.vertices[node].move_to(graph5_23.vertices[3].get_center() + relative_positionen6_23[node])

        # for vertex in graph6_23.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_23:
            kante_von_5_zu_node = Line(graph5_23.vertices[3].get_center(), graph6_23.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_23 = graph6_23.add_labels()
        self.add(labels6_23)
        # self.play(FadeIn(labels6_23), run_time=0.05)

        vertex6_24 = [1]
        graph6_24 = CustomGraph(vertex6_24, [])
        relative_positionen6_24 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_24:
            graph6_24.vertices[node].move_to(graph5_24.vertices[2].get_center() + relative_positionen6_24[node])

        # for vertex in graph6_24.vertices.values():
        #     self.play(GrowFromCenter(vertex), run_time=0.05)

        for node in vertex6_24:
            kante_von_5_zu_node = Line(graph5_24.vertices[2].get_center(), graph6_24.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)
            # self.play(Create(kante_von_5_zu_node), run_time=0.1)

        labels6_24 = graph6_24.add_labels()
        self.add(labels6_24)
        # self.play(FadeIn(labels6_24), run_time=0.05)

        # group whole graph with all nodes, labels and edges

        gesamter_baum.add(graph1_1, graph2_1, graph3_1, graph3_2, graph3_3, graph3_4, graph4_1, graph4_2, graph4_3, graph4_4, graph4_5, graph4_6, graph4_7, graph4_8, graph4_9, graph4_10, graph4_11, graph4_12, graph5_1, graph5_2, graph5_3, graph5_4, graph5_5, graph5_6, graph5_7, graph5_8, graph5_9, graph5_10, graph5_11, graph5_12, graph5_13, graph5_14, graph5_15, graph5_16, graph5_17, graph5_18, graph5_19, graph5_20, graph5_21, graph5_22, graph5_23, graph5_24, graph6_1, graph6_2, graph6_3, graph6_4, graph6_5, graph6_6, graph6_7, graph6_8, graph6_9, graph6_10, graph6_11, graph6_12, graph6_13, graph6_14, graph6_15, graph6_16, graph6_17, graph6_18, graph6_19, graph6_20, graph6_21, graph6_22, graph6_23, graph6_24, labels1_1, labels2_1, labels3_1, labels3_2, labels3_3, labels3_4, labels4_1, labels4_2, labels4_3, labels4_4, labels4_5, labels4_6, labels4_7, labels4_8, labels4_9, labels4_10, labels4_11, labels4_12, labels5_1, labels5_2, labels5_3, labels5_4, labels5_5, labels5_6, labels5_7, labels5_8, labels5_9, labels5_10, labels5_11, labels5_12, labels5_13, labels5_14, labels5_15, labels5_16, labels5_17, labels5_18, labels5_19, labels5_20, labels5_21, labels5_22, labels5_23, labels5_24, labels6_1, labels6_2, labels6_3, labels6_4, labels6_5, labels6_6, labels6_7, labels6_8, labels6_9, labels6_10, labels6_11, labels6_12, labels6_13, labels6_14, labels6_15, labels6_16, labels6_17, labels6_18, labels6_19, labels6_20, labels6_21, labels6_22, labels6_23, labels6_24)

        # self.play(gesamter_baum.animate.scale(0.5).to_edge(LEFT), run_time=2)

        # self.play(FadeOut(gesamter_baum), run_time=0.5)

        self.play(FadeIn(gesamter_baum), run_time=1)


        with self.voiceover(text="This tree shows every possible route, if you start from node one. Here we can now see that there are 24 possible routes to get to the last node. But is you take a closer look at the first and last route, you can see that the routes are identical, if we have a symmetrical TSP. That means if we have a symmetrical TSP, as in our example, we can ignore half of the routes."):
            
            self.wait(10)

            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph3_1.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph4_1.vertices[4])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph5_1.vertices[5])
            
            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_1.vertices[1])

            # rote Linien zw Kreisen für Route
            linie_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2.set_stroke(RED)

            linie_zw_2_3 = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_2_3.set_stroke(RED)

            linie_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4.set_stroke(RED)

            linie_zw_4_5 = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_4_5.set_stroke(RED)

            linie_zw_5_1 = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_5_1.set_stroke(RED)

            kreis2_um_5 = Circle(color=RED)
            kreis2_um_5.surround(graph2_1.vertices[5]) 

            kreis2_um_4 = Circle(color=RED)
            kreis2_um_4.surround(graph3_4.vertices[4])

            kreis2_um_3 = Circle(color=RED)
            kreis2_um_3.surround(graph4_12.vertices[3])

            kreis2_um_2 = Circle(color=RED)
            kreis2_um_2.surround(graph5_24.vertices[2])

            kreis2_um_1 = Circle(color=RED)
            kreis2_um_1.surround(graph6_24.vertices[1])

            linie2_zw_1_5 = Line(kreis2_um_5.get_center(), kreis_um_1.get_center(), buff=0.3)
            linie2_zw_1_5.set_stroke(RED)

            linie2_zw_5_4 = Line(kreis2_um_4.get_center(), kreis2_um_5.get_center(), buff=0.3)
            linie2_zw_5_4.set_stroke(RED)

            linie2_zw_4_3 = Line(kreis2_um_3.get_center(), kreis2_um_4.get_center(), buff=0.3)
            linie2_zw_4_3.set_stroke(RED)

            linie2_zw_3_2 = Line(kreis2_um_2.get_center(), kreis2_um_3.get_center(), buff=0.3)
            linie2_zw_3_2.set_stroke(RED)

            linie2_zw_2_1 = Line(kreis2_um_1.get_center(), kreis2_um_2.get_center(), buff=0.3)
            linie2_zw_2_1.set_stroke(RED)


            self.play(Create(linie_zw_1_2), run_time=0.5)
            self.play(Create(linie_zw_2_3), run_time=0.5)
            self.play(Create(linie_zw_3_4), run_time=0.5)
            self.play(Create(linie_zw_4_5), run_time=0.5)
            self.play(Create(linie_zw_5_1), run_time=0.5)

            self.play(Create(linie2_zw_2_1), run_time=0.5)
            self.play(Create(linie2_zw_3_2), run_time=0.5)
            self.play(Create(linie2_zw_4_3), run_time=0.5)
            self.play(Create(linie2_zw_5_4), run_time=0.5)
            self.play(Create(linie2_zw_1_5), run_time=0.5)
            
            self.wait(5)

            # self.play(FadeOut(linie_zw_1_2), run_time=0.5)
            # self.play(FadeOut(linie_zw_2_3), run_time=0.5)
            # self.play(FadeOut(linie_zw_3_4), run_time=0.5)
            # self.play(FadeOut(linie_zw_4_5), run_time=0.5)
            # self.play(FadeOut(linie_zw_5_1), run_time=0.5)

            self.play(FadeOut(linie_zw_1_2, linie_zw_2_3, linie_zw_3_4, linie_zw_4_5, linie_zw_5_1), run_time=1)
            self.play(FadeOut(linie2_zw_1_5, linie2_zw_5_4, linie2_zw_4_3, linie2_zw_3_2, linie2_zw_2_1), run_time=1)

        kreis1 = Circle(color=RED, radius=0.5)
        kreis1.set_fill(RED, opacity=1.0)
        kreis1.surround(graph6_10.vertices[1])

        kreis2 = Circle(color=RED, radius=0.5)
        kreis2.set_fill(RED, opacity=1.0)
        kreis2.surround(graph6_12.vertices[1])

        kreis3 = Circle(color=RED, radius=0.5)
        kreis3.set_fill(RED, opacity=1.0)
        kreis3.surround(graph6_14.vertices[1])

        kreis4 = Circle(color=RED, radius=0.5)
        kreis4.set_fill(RED, opacity=1.0)
        kreis4.surround(graph6_16.vertices[1])

        kreis5 = Circle(color=RED, radius=0.5)
        kreis5.set_fill(RED, opacity=1.0)
        kreis5.surround(graph6_17.vertices[1])

        kreis6 = Circle(color=RED, radius=0.5)
        kreis6.set_fill(RED, opacity=1.0)
        kreis6.surround(graph6_18.vertices[1])

        kreis7 = Circle(color=RED, radius=0.5)
        kreis7.set_fill(RED, opacity=1.0)
        kreis7.surround(graph6_19.vertices[1])

        kreis8 = Circle(color=RED, radius=0.5)
        kreis8.set_fill(RED, opacity=1.0)
        kreis8.surround(graph6_20.vertices[1])

        kreis9 = Circle(color=RED, radius=0.5)
        kreis9.set_fill(RED, opacity=1.0)
        kreis9.surround(graph6_21.vertices[1])

        kreis10 = Circle(color=RED, radius=0.5)
        kreis10.set_fill(RED, opacity=1.0)
        kreis10.surround(graph6_22.vertices[1])

        kreis11 = Circle(color=RED, radius=0.5)
        kreis11.set_fill(RED, opacity=1.0)
        kreis11.surround(graph6_23.vertices[1])

        kreis12 = Circle(color=RED, radius=0.5)
        kreis12.set_fill(RED, opacity=1.0)
        kreis12.surround(graph6_24.vertices[1])

        with self.voiceover(text="Let's blur out the routes that we can ignore."):

            self.wait(2)
            self.play(Create(kreis1), Create(kreis2),Create(kreis3),Create(kreis4), Create(kreis5),  Create(kreis6), Create(kreis7), Create(kreis8), Create(kreis9), Create(kreis10), Create(kreis11), Create(kreis12), run_time=0.5)
  

        self.wait(2)



        with self.voiceover(text="Here we can also visualize which route we took in the first example."):

            self.wait(2)

            # red line from node one to node two, then node two to node 5, then node 5 to node 3, then to node 4, then to node 1
            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph3_1.vertices[5])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph4_3.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph5_5.vertices[4])

            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_5.vertices[1])

            # rote Linien zw Kreisen für Route
            linie_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2.set_stroke(RED)

            linie_zw_2_5 = Line(kreis_um_2.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_2_5.set_stroke(RED)

            linie_zw_5_3 = Line(kreis_um_5.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_5_3.set_stroke(RED)

            linie_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4.set_stroke(RED)

            linie_zw_4_1 = Line(kreis_um_4.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_4_1.set_stroke(RED)

            self.play(Create(linie_zw_1_2), run_time=0.5)
            self.play(Create(linie_zw_2_5), run_time=0.5)
            self.play(Create(linie_zw_5_3), run_time=0.5)
            self.play(Create(linie_zw_3_4), run_time=0.5)
            self.play(Create(linie_zw_4_1), run_time=0.5)



        with self.voiceover(text="After having created a tree for every possible route, the branch and bound method calculates the cost for every route and compares it to the best route so far. If the cost of the current route is higher than the cost of the best route so far, the current route will be discarded."):
            self.wait(6)

        with self.voiceover(text="Let's take a look at an example. Lets say the algorithm calculated our route first with the cost of 15. As it is the first route, it is also the best route so far."):
            self.wait(6)

            number15 = Text("15", font_size=30)
            number15.next_to(graph6_5.vertices[1], DOWN, buff=1)
            self.play(FadeIn(number15), run_time=0.5)

            self.wait(4)

            linie_zw_1_2_o = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2_o.set_stroke(YELLOW)

            linie_zw_2_5_o = Line(kreis_um_2.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_2_5_o.set_stroke(YELLOW)

            linie_zw_5_3_o = Line(kreis_um_5.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_5_3_o.set_stroke(YELLOW)

            linie_zw_3_4_o = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4_o.set_stroke(YELLOW)

            linie_zw_4_1_o = Line(kreis_um_4.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_4_1_o.set_stroke(YELLOW)

            self.play(Create(linie_zw_1_2_o), run_time=0.5)
            self.play(Create(linie_zw_2_5_o), run_time=0.5)
            self.play(Create(linie_zw_5_3_o), run_time=0.5)
            self.play(Create(linie_zw_3_4_o), run_time=0.5)
            self.play(Create(linie_zw_4_1_o), run_time=0.5)

            self.play(FadeOut(linie_zw_1_2, linie_zw_2_5,linie_zw_5_3, linie_zw_3_4, linie_zw_4_1), run_time=0)

        with self.voiceover(text="Next, the algorithm calculates the route on the left. The cost of this route is 12. As this route is better than the best route so far, it becomes the new best route."):


            self.wait(2)
            
            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph3_1.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph4_1.vertices[4])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph5_1.vertices[5])
            
            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_1.vertices[1])

            # rote Linien zw Kreisen für Route
            linie2_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie2_zw_1_2.set_stroke(RED)

            linie2_zw_2_3 = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie2_zw_2_3.set_stroke(RED)

            linie2_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie2_zw_3_4.set_stroke(RED)

            linie2_zw_4_5 = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie2_zw_4_5.set_stroke(RED)

            linie2_zw_5_1 = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie2_zw_5_1.set_stroke(RED)

            self.play(Create(linie2_zw_1_2), run_time=0.5)
            self.play(Create(linie2_zw_2_3), run_time=0.5)
            self.play(Create(linie2_zw_3_4), run_time=0.5)
            self.play(Create(linie2_zw_4_5), run_time=0.5)
            self.play(Create(linie2_zw_5_1), run_time=0.5)

            number12 = Text("12", font_size=30)
            number12.next_to(graph6_1.vertices[1], DOWN, buff=1)
            self.play(FadeIn(number12), run_time=0.5)





            linie2_zw_1_2_o = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie2_zw_1_2_o.set_stroke(YELLOW)

            linie2_zw_2_3_o = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie2_zw_2_3_o.set_stroke(YELLOW)

            linie2_zw_3_4_o = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie2_zw_3_4_o.set_stroke(YELLOW)

            linie2_zw_4_5_o = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie2_zw_4_5_o.set_stroke(YELLOW)

            linie2_zw_5_1_o = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie2_zw_5_1_o.set_stroke(YELLOW)

            self.wait(1)

            self.play(FadeOut(linie_zw_1_2_o, linie_zw_2_5_o, linie_zw_5_3_o, linie_zw_3_4_o, linie_zw_4_1_o), run_time=0.5)
            self.play(FadeOut(linie2_zw_1_2, linie2_zw_2_3, linie2_zw_3_4, linie2_zw_4_5, linie2_zw_5_1), run_time=0.05)
            self.play(FadeOut(number15), run_time=0.5)

            self.wait(2)

            self.play(Create(linie2_zw_1_2_o), run_time=0.5)
            self.play(Create(linie2_zw_2_3_o), run_time=0.5)
            self.play(Create(linie2_zw_3_4_o), run_time=0.5)
            self.play(Create(linie2_zw_4_5_o), run_time=0.5)
            self.play(Create(linie2_zw_5_1_o), run_time=0.5)

        with self.voiceover(text="Now the algorithm calculates the next route. In our example it will be the seventh possible route."):
            self.wait(2)



            kreis2_um_1 = Circle(color=RED, radius=0.5)
            kreis2_um_1.surround(graph1_1.vertices[1])

            kreis2_um_2 = Circle(color=RED, radius=0.6)
            kreis2_um_2.surround(graph2_1.vertices[3])

            kreis2_um_3 = Circle(color=RED)
            kreis2_um_3.surround(graph3_2.vertices[2])

            kreis2_um_4 = Circle(color=RED)
            kreis2_um_4.surround(graph4_4.vertices[4])

            kreis2_um_5 = Circle(color=RED, radius=0.7)
            kreis2_um_5.surround(graph5_7.vertices[5])

            kreis2_um_1_2 = Circle(color=RED)
            kreis2_um_1_2.surround(graph6_7.vertices[1])

            # rote Linien zw Kreisen für Route
            linie3_zw_1_2 = Line(kreis2_um_1.get_center(), kreis2_um_2.get_center(), buff=0.3)
            linie3_zw_1_2.set_stroke(RED)

            linie3_zw_2_3 = Line(kreis2_um_2.get_center(), kreis2_um_3.get_center(), buff=0.3)
            linie3_zw_2_3.set_stroke(RED)

            linie3_zw_3_4 = Line(kreis2_um_3.get_center(), kreis2_um_4.get_center(), buff=0.3)
            linie3_zw_3_4.set_stroke(RED)

            linie3_zw_4_5 = Line(kreis2_um_4.get_center(), kreis2_um_5.get_center(), buff=0.3)
            linie3_zw_4_5.set_stroke(RED)

            linie3_zw_5_1 = Line(kreis2_um_5.get_center(), kreis2_um_1_2.get_center(), buff=0.3)
            linie3_zw_5_1.set_stroke(RED)

            # self.play(Create(linie3_zw_1_2), run_time=0.5)
            # self.play(Create(linie3_zw_2_3), run_time=0.5)
            # self.play(Create(linie3_zw_3_4), run_time=0.5)
            # self.play(Create(linie3_zw_4_5), run_time=0.5)
            # self.play(Create(linie3_zw_5_1), run_time=0.5)

        with self.voiceover(text="In this route the algorithm realizes at the third node that the added costs are at 14. Since the cost of the route till the third node is already higher than the cost of the best route, the algorithm can discard this route without calculating it untill the end."):
            
            self.play(Create(linie3_zw_1_2), run_time=0.5)
            self.play(Create(linie3_zw_2_3), run_time=0.5)
            
            number14 = Text("14", font_size=30)
            number14.next_to(graph3_2.vertices[2], LEFT*0.5, buff=1)
            self.play(FadeIn(number14), run_time=0.5)

            self.wait(4)

            self.play(FadeOut(linie3_zw_1_2, linie3_zw_2_3, linie3_zw_3_4), run_time=0.5)

        
        with self.voiceover(text="This way of calculating the best route is applied to every route. At the end the algorithm will have found the best route. In this example it is the first route."):
            self.play(FadeOut(number14, number12, linie2_zw_1_2_o, linie2_zw_2_3_o, linie2_zw_3_4_o, linie2_zw_4_5_o, linie2_zw_5_1_o), run_time=0.5)
            # draw_line(graph1_1.vertices[1], graph2_1.vertices[2], graph3_1.vertices[3], graph4_1.vertices[4], graph5_1.vertices[5], graph6_1.vertices[1], RED)
            # draw_line(graph1_1.vertices[1], graph2_1.vertices[3], graph3_2.vertices[2], graph4_4.vertices[4], graph5_7.vertices[5], graph6_7.vertices[1], RED)
            self.wait(4)
            self.play(Create(linie2_zw_1_2_o), run_time=0.5)
            self.play(Create(linie2_zw_2_3_o), run_time=0.5)
            self.play(Create(linie2_zw_3_4_o), run_time=0.5)
            self.play(Create(linie2_zw_4_5_o), run_time=0.5)
            self.play(Create(linie2_zw_5_1_o), run_time=0.5)
            # self.play(FadeOut(linie1, linie2, linie3, linie4, linie5))


        with self.voiceover(text="Let's take a look now at the time complexity of the branch and bound method. As you can see, the algorithm calculates every possible route. But as we have seen before, the algorithm can discard routes that are worse than the best route so far. "):
            self.wait(4)

        with self.voiceover(text="That means the algorithm does not have to calculate every route untill the end. Still having to calculate every possible route makes the branch and bound method very time consuming. In the worst case the algorithm has to calculate every possible route and the time complexity is the same as the brute force method."):
            self.wait(4)

        with self.voiceover(text="However the algorithm performs very well in practice and it is mostly better than the brute force method."):
            self.wait(4)

        












            



if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} GraphBaB")