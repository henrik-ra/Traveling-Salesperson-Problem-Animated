from manim import *
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

        self.wait()

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
    os.system(f"manim -pqh {__file__} AzureExample")