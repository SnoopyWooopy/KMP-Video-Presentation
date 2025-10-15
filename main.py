from manim import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class TitleCard(Scene):
    def construct(self):
        algorithmTopic = Text("Knuth-Morris-Pratt",font="Liberation Serif", font_size=80)
        videoTitle = Text("41052 Advanced Algorithms: \n Assignment 2 Research Presentation", font_size=40)
        subTitle = Text("By Melisa Erica Soria 14482905",font_size=35)

        # Center title card
        algorithmTopic.move_to(UP * 1.5)
        videoTitle.next_to(algorithmTopic, DOWN, buff=0.5)
        subTitle.next_to(videoTitle, DOWN, buff=0.5)

        self.play(Write(algorithmTopic))
        self.play(Write(videoTitle))
        self.play(Write(subTitle))
