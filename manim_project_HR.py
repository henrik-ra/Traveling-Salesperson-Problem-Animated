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

DARK_BLUE_COLOR = "#00008b"


class BruteForce(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
                 (1, 7), (5, 7), (2, 8), (1, 9)]

        h = CustomGraph(vertices, edges).shift(RIGHT * 0)

        # Verschieben des gesamten Graphen
        self.play(Create(h))

        self.wait(4)
        h.scale(0.5)

        # Animation für das Hervorheben von bestimmten Kanten
        for edge in h.edges:
            self.play(h.edges[edge].animate.set_color(RED), run_time=0.5)
            self.wait(0.1)
            self.play(h.edges[edge].animate.set_color(GREEN), run_time=0.5)

        self.wait(1)


class GraphkNN(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
                 (1, 7), (5, 7), (2, 8), (1, 9)]

        h = CustomGraph(vertices, edges).shift(RIGHT * 0)

        # Verschieben des gesamten Graphen
        self.play(Create(h))

        self.wait(4)
        h.scale(0.5)

        # Animation für das Hervorheben von bestimmten Kanten
        for edge in h.edges:
            self.play(h.edges[edge].animate.set_color(RED), run_time=0.5)
            self.wait(0.1)
            self.play(h.edges[edge].animate.set_color(GREEN), run_time=0.5)

        self.wait(1)


# class Intro(VoiceoverScene):
#     def construct(self):
#         self.set_speech_service(
#             AzureService(
#                 voice="en-US-GuyNeural ",
#                 style="newscast-casual",
#             )
#         ) 
#         # self.camera.background_color = BLACK

#         with self.voiceover(text="The Traveling Salesman Problem (TSP) is a classic problem in computer science and operations research.") as tracker:
#             # Introduction Text
#             intro_text = Text("Traveling Salesman Problem").to_edge(UP)
#             explanation1 = Text("The challenge: Find the shortest path visiting all cities.", font_size=24).next_to(intro_text, DOWN)
#             self.play(Write(intro_text), FadeIn(explanation1))
#             self.wait(2)
#             self.play(FadeOut(explanation1))

#         with self.voiceover(text="Let's assume we are an international salesman and need to visit clients all over the world. Our time is very expensive so we need to find the most feasible and shortest way.") as tracker:
            
#             # Load the image
#             image = ImageMobject("Salesman.png")
#             image.scale(0.3)  # Skalieren Sie das Bild nach Bedarf

#             # Start position
#             start_pos = image.get_center()

#             # Move up and to the right
#             move_up_right = start_pos + 1.5*UP + 3*RIGHT
#             # Move down and to the left
#             move_down_left = start_pos + 3*DOWN + 3*LEFT

#             # Add image to the scene
#             self.add(image)
#             self.wait(3)

#             # Move image up and to the right, then back
#             self.play(image.animate.move_to(move_up_right))
#             self.play(image.animate.move_to(start_pos))

#             # Move image down and to the left, then back
#             self.play(image.animate.move_to(move_down_left))
#             self.play(image.animate.move_to(start_pos))

#             self.wait(4)
#             self.remove(image)

#             # fade out header
#             self.play(FadeOut(intro_text))


#         with self.voiceover(text="There are several ways to calculate or find the shortest way between different point, cities in this case. This visualization is based on the k nearest neighbors method. This algorithm  involves the salesman starting at a city and, for each step, visiting the nearest unvisited city until all cities are visited. Essentially, the salesman looks at the 'k' closest cities and selects the nearest one as the next stop. While this is simple and intuitive, this heuristic does not guarantee the shortest overall route, especially as 'k' is typically set to 1 for TSP, hence it's often used for initial approximations.") as tracker:

#             # World Map
#             svg_object = SVGMobject("world.svg").scale(3).set_color(WHITE)
#             self.play(FadeIn(svg_object))
#             self.wait(5)
            
#             # Definieren Sie die Punkte (Städte)
#             points = [
#                 Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # DE
#                 Dot(np.array([-0.28, -0.16, 0]), color=DARK_GREY), # Spain

#                 Dot(np.array([2.5, -0.5, 0]), color=DARK_GREY), # Asia
#                 Dot(np.array([2.5, 0.3, 0]), color=DARK_GREY), # Asia

#                 Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Afrika
#                 Dot(np.array([0.5, -1, 0]), color=DARK_GREY), # Afrika

#                 Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia

#                 # Dot(np.array([-1.7, -2, 0]), color=DARK_GREY), # Südamerika
#                 Dot(np.array([-1.5, -1.6, 0]), color=DARK_GREY), # Südamerika

#                 Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
#                 Dot(np.array([-3.2, -0.2, 0]), color=DARK_GREY), # USA
#                 Dot(np.array([-3, 0.5, 0]), color=DARK_GREY), # Canada
#                 # Fügen Sie hier mehr Punkte hinzu
#             ]

#             # Stellen Sie die Punkte auf der Szene dar
#             for point in points:
#                 self.add(point)

#             # TSP Algorithmus: Nearest-Neighbor
#             route = self.nearest_neighbor(points, 0)

#             # Zeichnen Sie die Linien zwischen den Punkten basierend auf der Route
#             # for i in range(len(route) - 1):
#             #     start_point = points[route[i]].get_center()
#             #     end_point = points[route[i + 1]].get_center()
#             #     line = Line(start_point, end_point, color=DARK_BLUE, stroke_width=2)
#             #     self.play(Create(line), run_time=0.5)


#             self.wait(14)

#             # Delete World Map
#             self.play(FadeOut(svg_object))

#     def nearest_neighbor(self, points, start_index):
#         num_points = len(points)
#         visited = [False] * num_points
#         visited[start_index] = True
#         route = [start_index]

#         current_index = start_index
#         while len(route) < num_points:
#             nearest_index = None
#             nearest_distance = float('inf')

#             # Zeichnen und Löschen der Pfeile zu allen unbesuchten Punkten
#             temp_arrows = []
#             for i in range(num_points):
#                 if not visited[i]:
#                     arrow = Arrow(points[current_index].get_center(), points[i].get_center(), buff=0, color=DARK_BLUE)
#                     temp_arrows.append(arrow)
#                     self.play(Create(arrow), run_time=0.1)

#             # Finden der kürzesten Verbindung
#             for i in range(num_points):
#                 if not visited[i]:
#                     distance = np.linalg.norm(points[current_index].get_center() - points[i].get_center())
#                     if distance < nearest_distance:
#                         nearest_distance = distance
#                         nearest_index = i

#             # Löschen Sie alle Pfeile außer dem zur kürzesten Verbindung
#             for arrow in temp_arrows:
#                 if np.all(arrow.get_end() == points[nearest_index].get_center()):
#                     self.play(Transform(arrow, Line(arrow.get_start(), arrow.get_end(), color=ORANGE)))
#                 else:
#                     self.play(FadeOut(arrow), run_time=0.1)

#             visited[nearest_index] = True
#             route.append(nearest_index)
#             current_index = nearest_index

#         # Zeichnen der letzten Linie zurück zum Startpunkt
#         last_line = Line(points[current_index].get_center(), points[start_index].get_center(), color=ORANGE)
#         self.add(last_line)

#         route.append(start_index)  # Rückkehr zum Startpunkt




# USE TRACKER_DURATION
class AzureExample(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text="Now, let's transform it into a square.") as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(
            text="You can also change the pitch of my voice like this.",
            prosody={"pitch": "+40Hz"},
        ) as tracker:
            pass

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait(5)


if __name__ == "__main__":
    os.system(f"manim -pql --disable_caching {__file__} Intro")