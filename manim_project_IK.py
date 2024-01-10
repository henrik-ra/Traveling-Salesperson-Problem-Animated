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
            self.wait(2)

            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(edge.animate.set_opacity(1), run_time=0.5)

            self.wait(3)

            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(FadeOut(edge), run_time=0.5)
            

            # Group the graph and labels together
            graph_with_labels = VGroup(graph, labels) 

            self.play(graph_with_labels.animate.shift(LEFT*5).scale(0.5), run_time=1)

            
        with self.voiceover(text="The Branch-and-Bound method begins by constructing a tree of all possibilities. First we need a Graph. Let's use the same graph and start at node one. ") as tracker:
            
            self.wait(1.5)
            self.play(FadeOut(bab_text))
            self.wait(3)

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
            self.play(vertex_groups[1].animate.move_to(UP * 2 + RIGHT * 2))

            # Bewegung der restlichen Knoten unterhalb von Knoten 1
            positions = [
                    LEFT  + UP * 0.5,  # Knoten 2
                    RIGHT + UP * 0.5,  # Knoten 3
                    RIGHT * 3 + UP * 0.5,  # Knoten 4
                    RIGHT * 5 + UP * 0.5  # Knoten 5
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
                self.camera.frame.animate.move_to(LEFT * 0.5 + DOWN * 0.5).scale(0.7)
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
            


        with self.voiceover(text="Let's go back to the tree. The next nodes that we can travel to are node 3 and node 4.") as tracker:

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


        with self.voiceover(text="As you can see the last city, that we have not visited is city 4. Let's finish our route by traveling to city 4.") as tracker:

            self.wait(4)
            linie_zwischen_kreis3_und_4_weiß = Line(kreis_um_knoten3.get_center(), kreis_um_knoten4.get_center(), buff=0.2)

            self.play(Create(linie_zwischen_kreis3_und_4_weiß))


        with self.voiceover(text="Now we can also finish our route on the tree by adding node 4 as our last node.") as tracker:


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

            



            
            


# class AzureExample(VoiceoverScene):
#     def construct(self):
#         self.set_speech_service(
#             AzureService(
#                 voice="en-US-GuyNeural ",
#                 style="newscast-casual",
#             )
#         )

#         circle = Circle()
#         square = Square().shift(2 * RIGHT)

#         with self.voiceover(text="This circle is drawn as I speak.") as tracker:
#             self.play(Create(circle), run_time=tracker.duration)

#         with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
#             self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

#         with self.voiceover(text="Now, let's transform it into a square.") as tracker:
#             self.play(Transform(circle, square), run_time=tracker.duration)

#         with self.voiceover(
#             text="You can also change the pitch of my voice like this.",
#             prosody={"pitch": "+40Hz"},
#         ) as tracker:
#             pass

#         with self.voiceover(text="Thank you for watching."):
#             self.play(Uncreate(circle))

#         self.wait(5)


if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} GraphBaB")