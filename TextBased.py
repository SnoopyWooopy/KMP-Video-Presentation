from manim import *
# all the text based scenes (somehow blender video editor is more anoying to use than this, is that what they call poor computers?)
from pygments.lexer import words
from rich.markdown import Heading


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
class Question1(Scene):
    def construct(self):
        heading = Text("1) What Problem Does the Algorithm Solve?", font_size=40)
        knp = Text("Knuth-Morris-Pratt Algorithm (KNP)", font_size=38)
        name = Tex ("Donald Knuth and James Morris and Vaughan Pratt",
                    tex_to_color_map={"Knuth": RED,"Morris": RED,"Pratt" :RED})
        purpose = Text("Sub-string problem that finds exact mach for...", font_size=35)
        latex = Tex(r"for each $p$ of length $m$")
        latex1 = Tex(r"within")
        latext2 = Tex(r"word $w$ of length $n$")
        latex3 = Tex("Returns: starting index position of $i$ of word")
        # $\Theta(mn) \ \Theta(m + n)$

        fancy = VGroup(latex,latex1,latext2,latex3)
        fancy.arrange(DOWN, buff=0.2)

        textGroup = VGroup(heading,knp, name, purpose, fancy)
        textGroup.scale(0.75)
        textGroup.arrange(DOWN, buff=0.2)
        heading.shift(UP * 0.3)
        self.play(Write(textGroup))

class References(Scene):
    def construct(self):
        Heading = Text("References", font_size=40)
        entires_raw = """        
        Kartik. (10 October, 2025). KMP Algorithm for Pattern Searching. GeeksforGeeks.
        https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/
        
        Logic First. (2020). Knuth-Morris-Pratt (KMP) algorithm | String Matching Algorithm | Substring Search.
        https://www.youtube.com/watch?v=4jY57Ehc14Y
        
        Wikimedia Foundation Inc. (10 October, 2025). Knuth–Morris–Pratt algorithm. Wikipedia.
        https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
        
        P3G. (11 December, 2011). Knuth–Morris–Pratt algorithm. Wcipeg.
        https://wcipeg.com/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
        
        Nayuki. (20 June, 2018). Knuth-Morris-Pratt-String-Matching. Project Nayuki.
        https://www.nayuki.io/page/knuth-morris-pratt-string-matching
        
        InsideCode. (24 October, 2022). Knuth-Morris-Pratt algorithm (KMP) - Inside code. YouTube.
        https://www.youtube.com/watch?v=M9azY7YyMqI&t=379s
        
        Junaid, A. W. (24 July, 2023). KMP algorithm and working of this algorithm. AWJUNAID.
        https://awjunaid.com/algorithm/kmp-algorithm-and-working-of-this-algorithm/
        """
        entries = Text(entires_raw, font_size=12, line_spacing=1.0)
        allText = VGroup(Heading, entries)
        allText.to_edge(LEFT, buff=0.5)
        allText.arrange(DOWN, buff=0.5)
        self.play(Write(allText))

