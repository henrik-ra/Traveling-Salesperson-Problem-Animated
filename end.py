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

class End(VoiceoverScene):
    def construct(self):

        # Initalisierung des Voiceovers
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        ) 

        bf = ImageMobject("./pics/brute_force.png").scale(0.3).move_to(LEFT * 3 + UP * 2)
        bab = ImageMobject("./pics/bab.png").scale(0.3).move_to(RIGHT * 3 + UP * 2)
        ch = ImageMobject("./pics/christofides.png").scale(0.3).move_to(LEFT * 3 + DOWN * 2)
        knn = ImageMobject("./pics/knn.png").scale(0.3).move_to(RIGHT * 3 + DOWN * 2)
        
        with self.voiceover(text="In this video, we showed you different methods to solve the traveling salesperson problem. Every method has its own advantages and disadvantages. The brute force algorithm is the most accurate, but it is also the slowest."):

            self.wait(4)


            self.play(FadeIn(bab, bf, ch, knn))

            self.wait(5)
            self.play(bf.animate.scale(1.5))
            self.wait(3)
            self.play(bf.animate.scale(1/1.5))

        with self.voiceover(text="The branch and bound method is faster, but it is still not efficient for large graphs."):

            self.wait(1)
            self.play(bab.animate.scale(1.5))
            self.wait(2)
            self.play(bab.animate.scale(1/1.5))

        with self.voiceover(text="The Christofides algorithm is a heuristic algorithm, which means it is not guaranteed to find the optimal solution, but it is much faster than the previous algorithms."):


            self.play(ch.animate.scale(1.5))
            self.wait(7)
            self.play(ch.animate.scale(1/1.5))

        with self.voiceover(text="The k-nearest neighbor algorithm is also a heuristic algorithm, but it is even faster than the Christofides algorithm. At the end depending on the size of the graph, you have to decide which algorithm is best suited for your problem."):

            self.play(knn.animate.scale(1.5))
            self.wait(5)
            self.play(knn.animate.scale(1/1.5))

            self.wait(5)


            



    if __name__ == "__main__":
        os.system(f"manim -pqh --disable_caching {__file__} End")