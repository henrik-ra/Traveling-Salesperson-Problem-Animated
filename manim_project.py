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

# voices: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts

class Intro(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        ) 
        # self.camera.background_color = BLACK

        with self.voiceover(text="The Traveling Salesman Problem (TSP) is a classic problem in computer science and operations research. It involves finding the shortest possible route that visits a list of cities and returns to the origin point.") as tracker:
            # Introduction Text
            intro_text = Text("Traveling Salesman Problem").to_edge(UP)
            explanation1 = Text("The challenge: Find the shortest path visiting all cities.", font_size=24).next_to(intro_text, DOWN)
            self.play(Write(intro_text), FadeIn(explanation1))
            self.wait(2)
            self.play(FadeOut(explanation1))

        with self.voiceover(text="Let's assume we are an international salesman and need to visiting clients all over the world. Our time is very expensive so we need to find the most feasible and shortest way.") as tracker:
            
            # Load the image
            image = ImageMobject("Salesman_stolen.png")
            image.scale(0.3)  # Skalieren Sie das Bild nach Bedarf

            # Start position
            start_pos = image.get_center()

            # Move up and to the right
            move_up_right = start_pos + 1.5*UP + 3*RIGHT
            # Move down and to the left
            move_down_left = start_pos + 3*DOWN + 3*LEFT

            # Add image to the scene
            self.add(image)
            self.wait(3)

            # Move image up and to the right, then back
            self.play(image.animate.move_to(move_up_right))
            self.play(image.animate.move_to(start_pos))

            # Move image down and to the left, then back
            self.play(image.animate.move_to(move_down_left))
            self.play(image.animate.move_to(start_pos))

            self.wait(4)
            self.remove(image)

            # fade out header
            self.play(FadeOut(intro_text))

            # intro_text = Text("Traveling Salesman Problem").to_edge(UP)
            # explanation1 = Text("The challenge: Find the shortest path visiting all cities.", font_size=24).next_to(intro_text, DOWN)
            # self.play(Write(intro_text), FadeIn(explanation1))
            # self.wait(2)
            # self.play(FadeOut(explanation1))

            # # City Nodes
            # cities = ["A", "B", "C", "D", "E", "F"]
            # city_locations = [LEFT, UP, RIGHT, DOWN, LEFT + DOWN, RIGHT + DOWN]
            # city_dots = [Dot(location, color=BLUE).add(Text(city).next_to(location, DOWN)) for city, location in zip(cities, city_locations)]
            # for dot in city_dots:
            #     self.play(FadeIn(dot), run_time=0.5)
            # self.wait(2)
            # for dot in city_dots:
            #     self.play(FadeOut(dot), run_time=0.5)

            # for dot in city_dots:
            #     self.play(FadeIn(dot), run_time=0.5)

            # # Distance Connections
            # # self.play(ReplacementTransform(explanation2, explanation3))
            # for i in range(len(city_dots)):
            #     for j in range(i + 1, len(city_dots)):
            #         line = Line(city_dots[i].get_center(), city_dots[j].get_center(), color=GREEN)
            #         self.play(Create(line), run_time=0.5)
            # self.wait(2)

            # # Highlighting a Route
            # route = [0, 3, 4, 1, 2, 5, 0]  # A -> D -> E -> B -> C -> F -> A
            # explanation4 = Text("Example route: A -> D -> E -> B -> C -> F -> A", font_size=24).to_edge(DOWN)
            # self.play(ReplacementTransform(explanation1, explanation4))
            # for i in range(len(route) - 1):
            #     self.play(Indicate(city_dots[route[i]]), Indicate(city_dots[route[i + 1]]), run_time=1)
            # self.wait(2)

            # # Calculating the Distance
            # distance_text = Text("Total Distance: 290 km", color=RED).to_edge(DOWN)
            # self.play(Transform(explanation4, distance_text))
            # self.wait(2)

            # # Conclusion Text
            # conclusion_text = Text("Finding the shortest route is a complex challenge.", font_size=24).to_edge(DOWN)
            # self.play(Transform(distance_text, conclusion_text))
            # self.wait(2)

            # # End Scene
            # self.wait()

        with self.voiceover(text="There are several ways to calculate or find the shortest way between different point, cities in this case. This visualization is based on the k nearest neighbors method. This algorithm  involves the salesman starting at a city and, for each step, visiting the nearest unvisited city until all cities are visited. Essentially, the salesman looks at the 'k' closest cities and selects the nearest one as the next stop. While this is simple and intuitive, this heuristic does not guarantee the shortest overall route, especially as 'k' is typically set to 1 for TSP, hence it's often used for initial approximations.") as tracker:

            # World Map
            svg_object = SVGMobject("world.svg").scale(3).set_color(WHITE)
            self.play(FadeIn(svg_object))
            self.wait(5)
            
            # Definieren Sie die Punkte (Städte)
            points = [
                Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # DE
                Dot(np.array([-0.28, -0.16, 0]), color=DARK_GREY), # Spain

                Dot(np.array([2.5, -0.5, 0]), color=DARK_GREY), # Asia
                Dot(np.array([2.5, 0.3, 0]), color=DARK_GREY), # Asia

                Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Afrika
                Dot(np.array([0.5, -1, 0]), color=DARK_GREY), # Afrika

                Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia

                # Dot(np.array([-1.7, -2, 0]), color=DARK_GREY), # Südamerika
                Dot(np.array([-1.5, -1.6, 0]), color=DARK_GREY), # Südamerika

                Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
                Dot(np.array([-3.2, -0.2, 0]), color=DARK_GREY), # USA
                Dot(np.array([-3, 0.5, 0]), color=DARK_GREY), # Canada
                # Fügen Sie hier mehr Punkte hinzu
            ]

            # Stellen Sie die Punkte auf der Szene dar
            for point in points:
                self.add(point)

            # TSP Algorithmus: Nearest-Neighbor
            route = self.nearest_neighbor(points, 0)

            # Zeichnen Sie die Linien zwischen den Punkten basierend auf der Route
            # for i in range(len(route) - 1):
            #     start_point = points[route[i]].get_center()
            #     end_point = points[route[i + 1]].get_center()
            #     line = Line(start_point, end_point, color=DARK_BLUE, stroke_width=2)
            #     self.play(Create(line), run_time=0.5)


            self.wait(14)

            # Delete World Map
            self.play(FadeOut(svg_object))

    def nearest_neighbor(self, points, start_index):
        num_points = len(points)
        visited = [False] * num_points
        visited[start_index] = True
        route = [start_index]

        current_index = start_index
        while len(route) < num_points:
            nearest_index = None
            nearest_distance = float('inf')

            # Zeichnen und Löschen der Pfeile zu allen unbesuchten Punkten
            temp_arrows = []
            for i in range(num_points):
                if not visited[i]:
                    arrow = Arrow(points[current_index].get_center(), points[i].get_center(), buff=0, color=DARK_BLUE)
                    temp_arrows.append(arrow)
                    self.play(Create(arrow), run_time=0.1)

            # Finden der kürzesten Verbindung
            for i in range(num_points):
                if not visited[i]:
                    distance = np.linalg.norm(points[current_index].get_center() - points[i].get_center())
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_index = i

            # Löschen Sie alle Pfeile außer dem zur kürzesten Verbindung
            for arrow in temp_arrows:
                if np.all(arrow.get_end() == points[nearest_index].get_center()):
                    self.play(Transform(arrow, Line(arrow.get_start(), arrow.get_end(), color=ORANGE)))
                else:
                    self.play(FadeOut(arrow), run_time=0.1)

            visited[nearest_index] = True
            route.append(nearest_index)
            current_index = nearest_index

        # Zeichnen der letzten Linie zurück zum Startpunkt
        last_line = Line(points[current_index].get_center(), points[start_index].get_center(), color=ORANGE)
        self.add(last_line)

        route.append(start_index)  # Rückkehr zum Startpunkt

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

        

# class TravelingSalesman2(Scene):
#     def construct(self):
#         # Definieren Sie die Punkte (Städte)
#         points = [
#             Dot(np.array([2, 1, 0])),
#             Dot(np.array([4, 3, 0])),
#             Dot(np.array([1, -2, 0])),
#             Dot(np.array([-3, 2, 0])),
#             # Fügen Sie hier mehr Punkte hinzu
#         ]

#         # Stellen Sie die Punkte auf der Szene dar
#         for point in points:
#             self.add(point)

#         # TSP Algorithmus: Nearest-Neighbor
#         route = self.nearest_neighbor(points, 0)

#         # Zeichnen Sie die Linien zwischen den Punkten basierend auf der Route
#         for i in range(len(route) - 1):
#             start_point = points[route[i]].get_center()
#             end_point = points[route[i + 1]].get_center()
#             line = Line(start_point, end_point, color=BLUE, stroke_width=2)
#             self.play(Create(line), run_time=0.5)

#         self.wait(2)

#     def nearest_neighbor(self, points, start_index):
#         num_points = len(points)
#         visited = [False] * num_points
#         visited[start_index] = True
#         route = [start_index]

#         current_index = start_index
#         while len(route) < num_points:
#             nearest_index = None
#             nearest_distance = float('inf')

#             for i in range(num_points):
#                 if not visited[i]:
#                     distance = np.linalg.norm(points[current_index].get_center() - points[i].get_center())
#                     if distance < nearest_distance:
#                         nearest_distance = distance
#                         nearest_index = i

#             visited[nearest_index] = True
#             route.append(nearest_index)
#             current_index = nearest_index

#         route.append(start_index)  # Rückkehr zum Startpunkt
#         return route

# class TravelingSalesman(VoiceoverScene):
#     def construct(self):
#         TEXT_SPEED = 0.045

#         self.set_speech_service(GTTSService())

#         background_texture = ImageMobject("USA-MAP4.png")  # Pfad zur Texturdatei
#         background_texture.scale(1)  # Skalieren Sie die Textur nach Bedarf
#         self.add(background_texture)

#         city_coords = [
#             (-6.0, -0.25, 0),  # SF
#             (-5.7, 0.55, 0),  # san jose
#             (-4.899, -1.45, 0),  # LA
#             (0.55, 0.85, 0),  # Atlanta
#             (-0.25, -0.35, 0),  # Miami
#             (-4.25, 1.75, 0),  # Miami
#             (-1.65, 1.35, 0),  # Denver
#             (3.6, -0.5, 0),  # Atlanta
#             (-3.25, -1.0, 0),  # phoenix
#             (0.55, -0.85, 0),  # dallas
#         ]

#         # cities = [
#         #     Dot(np.array([x, y, z]), radius=0.05, color=BLACK)
#         #     for x, y, z in city_coords
#         # ]


#         # connections = []
#         # for i in range(len(city_coords)):
#         #     for j in range(i + 1, len(city_coords)):
#         #         line = Line(city_coords[i], city_coords[j], color=WHITE, stroke_width=2)
#         #         connections.append(line)

#         # with self.voiceover(text="This circle is drawn as I speak.") as tracker:
#         #     self.play(*[Create(city) for city in cities], run_time=tracker.duration)
        

#         # Punkte auf der Szene erstellen
#         points = [Dot(np.array(coord)) for coord in city_coords]
#         for point in points:
#             self.add(point)


#         def calculate_total_distance(path):
#             return sum(np.linalg.norm(np.array(city_coords[path[i]]) - np.array(city_coords[path[i - 1]])) for i in range(1, len(path)))

#         # Berechne den kürzesten Pfad
#         shortest_path = min(itertools.permutations(range(len(city_coords))), key=calculate_total_distance)

#         # Zeichne die Pfade
#         lines = []
#         for i in range(len(shortest_path)):
#             start_point = points[shortest_path[i]]
#             end_point = points[shortest_path[(i + 1) % len(points)]]
#             line = Line(start_point.get_center(), end_point.get_center(), stroke_width=2)
#             lines.append(line)
#             self.play(Create(line), run_time=0.5)

#         # Halte das Endbild
#         self.wait(2)

#         # with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
#         #     pass


#         # with self.voiceover(
#         #     text="This is a very very very very very very very very very very very very very very very very very long sentence."
#         # ):
#         #     pass

#         # with self.voiceover(text="Es kann tausende Verbindungen geben.") as tracker2:
#         #     self.play(*[Create(city) for city in cities], run_time=tracker2.duration)
#             # self.play(*[Create(connection) for connection in connections], run_time=tracker2.duration)

#         # self.wait(5) 



if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} Intro")