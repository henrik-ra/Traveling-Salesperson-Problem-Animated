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

# class GraphkNN(VoiceoverScene):
#     def construct(self):
#         self.set_speech_service(
#             AzureService(
#                 voice="en-US-GuyNeural ",
#                 style="newscast-casual",
#             )
#         )
#         # the graph class expects a list of vertices and edges
#         vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#         edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
#                  (1, 7), (5, 7), (2, 8), (1, 9)]

#         h = CustomGraph(vertices, edges).shift(RIGHT * 0)

#         # Verschieben des gesamten Graphen
#         self.play(Create(h))

#         self.wait(4)
#         h.scale(0.5)

#         # Animation für das Hervorheben von bestimmten Kanten
#         for edge in h.edges:
#             self.play(h.edges[edge].animate.set_color(RED), run_time=0.5)
#             self.wait(0.1)
#             self.play(h.edges[edge].animate.set_color(GREEN), run_time=0.5)

#         self.wait(1)


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
    os.system(f"manim -pqh --disable_caching {__file__} AzureExample")