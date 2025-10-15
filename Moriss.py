from manim import *
from pyglm.glm import column
from pygments.lexer import words

# EXORT SETTINGS
# config.pixel_width = 1920
## config.pixel_height = 1080

# Lsb construction
class lps(Scene):
    ## Creating floating labels for patternTable
    def floatingLabel(self, table, data):
        colLabels = [Text(str(i)) for i in range(len(data[0]))]  # index count label creation
        #assignation
        for i, label in enumerate(colLabels):
            # Get the center of the cell in row 1, column i+1
            cell = table.get_cell((1, i + 1))
            label.next_to(cell.get_top(), UP, buff=0.3)  # Slightly above the cell array
            self.play(Write(label,run_time=0.2))
    # Lsp Construction steps highlighted (technically not correctly implemented but good enough for animation)
    def populating (self, patternTable, lpsAnswers, lspTable, index, foundAt = -1):
        highlightedList = [] # Stores all highlighted cells for later removal

        #Select Current index
        highlight = patternTable.get_highlighted_cell((1, index + 1), color=RED)
        patternTable.add_to_back(highlight)
        self.wait(1)

        # Prefix Match found
        if (foundAt != -1):
            for i in range (0, int(lpsAnswers[0][index])):
                prefix = patternTable.get_highlighted_cell((1, foundAt + i), color=BLUE)
                patternTable.add_to_back(prefix)
                highlightedList.append(prefix)

        # lps update
        targetCell = lspTable.get_entries_without_labels((1, index + 1))  # wtf is get_entries_without_labels
        self.play(targetCell.animate.become(Text(lpsAnswers[0][index])).move_to(targetCell))

        #Removal of highlights
        highlight.set_opacity(0)
        if (foundAt != -1):
            for cell in highlightedList:
                cell.set_opacity(0)
        self.wait(1)

    def construct(self):
        #Based on Example of Construction of LPS Array: https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/
        # [1:30] https://www.youtube.com/watch?v=ynv7bbcSLKE

        # Table data initlisation
        pattern = [
            ['a','b','a','b','a','a']
        ]
        lsbValues = [["." for _ in range(6)]]
        lpsAnswers = [['0', '0', '1', '2', '3', '1']]

        phrasePattern = ''.join(pattern[0]) # Pattern that needs to be found LOL UNUSED
        ##self.play(Write(Text(wordPattern))) # need to be monim compatible text type

        patternTable = Table(pattern,include_outer_lines=True)
        lspTable = Table(lsbValues,include_outer_lines=True)

        allTables = VGroup(patternTable,lspTable)

        ## Arrangement
        allTables.arrange(DOWN, buff=0.5)
        allTables.add(Text("LSP"))
        allTables.submobjects.insert(1, allTables.submobjects.pop(-1))  # Move label to position 1

        # Rearrange the group again to shift tables and label without overlap
        allTables.arrange(DOWN, buff=0.5)
        self.floatingLabel(patternTable,pattern)
        self.play(Write(allTables))

        ## Ugly transformation
        # self.play(targetCell.animate.become(Text("5").move_to(targetCell)),run_time=2)  ## WORKS with sil animation ,run_time=secs

        #Populating lps Table (sorry hardcoded)
        self.populating(patternTable,lpsAnswers, lspTable,0) #at index 0 (no match)
        self.populating(patternTable, lpsAnswers, lspTable, 1)
        self.populating(patternTable, lpsAnswers, lspTable, 2,1) #found at position
        self.populating(patternTable, lpsAnswers, lspTable, 3,1)
        self.populating(patternTable, lpsAnswers, lspTable, 4, 1)
        self.populating(patternTable, lpsAnswers, lspTable, 5, 1)

# Comparison
class compare(Scene):
    def floatingLabel(self, table, data, direction):
        colLabels = [Text(str(i),font_size=30) for i in range(len(data[0]))]  # index count label creation
        labelComplete = VGroup();
        #assignation
        for i, label in enumerate(colLabels):
            # Get the center of the cell in row 1, column i+1
            cell = table.get_cell((1, i + 1))
            if direction == "UP":
                label.next_to(cell.get_top(), UP, buff=0.3)  # Slightly above the cell array
                self.play(Write(label,run_time=0.2))
            else:
                # I had to change position approach cause ^ relative position was messing up grouplabeling
                label.move_to(cell.get_bottom())
                label.shift(DOWN * 0.3)
                labelComplete.add(label)
                ##self.play(Write(label,run_time=0.2))
        return labelComplete # Hopefully I can slide this with pattern table

    # aligns movingtable below staticTable by index/cell
    def alignmentArray (self, wordTable, patternTable, wordCell, patternCell ):
            # Composition - Aligns the cell of word and pattern array
            # REMEMBER MELISA TABLES ARE INDEXED 1 in Manim
            # maybe I should rename to moving and unmoving static tables
            wCell = wordTable.get_cell(wordCell)
            pCell = patternTable.get_cell(patternCell)
            shiftDistance = wCell.get_center() - pCell.get_center()

            patternTable.next_to(wordTable, DOWN, buff=1.5)
            patternTable.shift(RIGHT * shiftDistance)

    def horizontalSlide(self,staticTable,movingTableGroup, wPoint, pPoint) :
        patternTable = movingTableGroup[0]

        targetWord = staticTable.get_cell((1, wPoint))  # Location of next WordTable index
        # slilly fix when lps returns 0, table gets misaligned since manim tables are index 1 (yet works just fine at index 0 for all other j?)
        if (pPoint == 0):
            currentLetter = patternTable.get_cell((1,1))
        else:
            currentLetter = patternTable.get_cell((1, pPoint))  # Location of current LetterTable

        ## Only calculates shift distance by x coordinate dist/pos
        shiftDistance = targetWord.get_center()[0] - currentLetter.get_center()[0]
        self.play(movingTableGroup.animate.shift(RIGHT * shiftDistance), run_time=0.5)

    #  updates label to hold current index of pointer i and j
    def updatePointer(self, i, j, wLabel, pLabel):
        new_wLabel = f"i = {i}"
        new_pLabel = f"j = {j}"
        #text changed
        self.play(Transform(wLabel, Tex(new_wLabel, font_size=25).move_to(wLabel.get_center())),
                  Transform(pLabel, Tex(new_pLabel, font_size=25).move_to(pLabel.get_center()))
                  )

    # Helper function: Removeal of highlights from a table
    def removeHighlight (self, table, highlights, instant : bool):
        if instant == True:
            for cell in highlights:
                table.remove(cell)
                #cell.set_opacity(0)  #highlights.set_opacity(0) NOT WORK
                #there is no such thing as remove_cell
        else:
            for cell in highlights:
                table.remove(cell)
                #cell.set_opacity(0)
                #there is no such thing as remove_cell
                self.wait(1)
        highlights.clear() # empty tracking
    # not being used
    def OLDcolour(self, wordTable, patternTableGroup, wPoint, pPoint, isMatch : bool):


        patternTable = patternTableGroup[0]
        colour = GREEN if isMatch else RED # colour cell is to be highlighted

        ## for r in (range(len(pattern[0]))):        self.play(movingTable[r].animate.set_opacity(0), run_time=0.3)


        # Highlighting relevant(cur) index
        highlightTop = wordTable.get_highlighted_cell((1, wPoint + 1), color=colour).scale(0.45)
        wordTable.add_to_back(highlightTop)

        highlightDown = patternTable.get_highlighted_cell((1, pPoint + 1), color=colour).scale(0.45)
        patternTable.add_to_back(highlightDown)

        self.play(Create(highlightTop), Create(highlightDown), run_time=0.5)

    def colour(self, wordTable, patternTableGroup, wPoint, pPoint, isMatch : bool, Slide=False):

        patternTable = patternTableGroup[0]
        colour = GREEN if isMatch else RED # colour cell is to be highlighted
        # clear previous
        #self.removeHighlight(wordTable, self.wordHighlights)
        #self.removeHighlight(patternTable, self.patternHighlights)
        #if Slide == True:


        ## for r in (range(len(pattern[0]))):        self.play(movingTable[r].animate.set_opacity(0), run_time=0.3)
        if isMatch:
            highlightTop = wordTable.get_highlighted_cell((1, wPoint + 1), color=colour).scale(0.45)
            wordTable.add_to_back(highlightTop)
            # acesses kmp highlight list
            self.wordHighlights.append(highlightTop)

            highlightDown = patternTable.get_highlighted_cell((1,pPoint + 1), color=colour).scale(0.45)
            patternTable.add_to_back(highlightDown)
            self.patternHighlights.append(highlightDown)

        else: # 1=0 excludes i=0 (...why did I do elif pPoint != 0)
            #Mismatch mark as red
            highlightTop = wordTable.get_highlighted_cell((1, wPoint + 1), color=colour).scale(0.45)
            wordTable.add_to_back(highlightTop)
            self.wordHighlights.append(highlightTop)

            highlightDown = patternTable.get_highlighted_cell((1, pPoint + 1), color=colour).scale(0.45)
            patternTable.add_to_back(highlightDown)
            self.patternHighlights.append(highlightDown)
            self.wait(1)

            # REMOVE coloured in time for slide reset
            self.removeHighlight(wordTable, self.wordHighlights, True)
            self.removeHighlight(patternTable, self.patternHighlights, True)


        #self.play(Create(highlightTop), Create(highlightDown), run_time=0.5)

    # Implemenation of KMP (REAL OMG)
    def kmp(self, wordTable, patternTableGroup, wordData, patternData, lps, lspTableGroup):
        patternTable = patternTableGroup[0]
        lspTable = lspTableGroup[1]
        lastMatched = lspTableGroup[2] # Used for location to print match results

        wordLength = len(wordData[0]) # length n
        patternLength = len(patternData[0]) # length m

        i = j = 0  # index pointers (i = current word index, j = current pattern index)
        match = 0

        #Highlight tracking initalisation
        self.wordHighlights = []
        self.patternHighlights = []

        # introducing arrow animation
        wLabel = Tex(r"i = " + str(i), font_size=25)
        pLabel = Tex(r"j = " + str(j), font_size=25)

        initalW = wordTable.get_cell((1,1))
        initalP = patternTable.get_cell((1, 1))

        wLabel.move_to(initalW.get_bottom())
        wLabel.shift(DOWN * 0.25)
        pLabel.move_to(initalP.get_top())
        pLabel.shift(UP * 0.25)

        wArrow = Arrow(start=wLabel.get_top(),end=initalW.get_bottom())
        pArrow = Arrow(start=pLabel.get_bottom(),end=initalP.get_top())

        # Grouped for easy sliding
        wPointer = VGroup(wLabel,wArrow)
        pPointer = VGroup(pLabel,pArrow)

        self.play(Write(wLabel),Write(pLabel))
        self.play(Write(wArrow),Write(pArrow))

        ## self.play(wPointer.animate.shift(RIGHT * 3), run_time=0.5)

        # kMP Algorithm
        while i < wordLength:
            #Prevent restarting loop & highlight allready covered in green
            if (i != 0):
                self.horizontalSlide(wordTable, patternTableGroup, i, j)
                #self.colour(wordTable, patternTableGroup, i, j, True, True)
            #current char match between i & j
            if wordData[0][i] == patternData[0][j]:
                #Pointers moving
                self.colour(wordTable, patternTableGroup, i, j, True)
                i += 1
                j += 1
                # updating pointer label
                self.updatePointer(i,j,wLabel,pLabel)
                # word found completely j =
                if j == patternLength:
                    ##Print answer:
                    match += 1

                    # answer written down
                    answer = Tex(rf"\# {match}~index:~{i - j}", font_size=25)
                    answer.next_to(lastMatched, DOWN, buff=0.2)
                    lastMatched = answer # update newest answer location
                    self.play(Write(answer))
                    # Look up LPS
                    highlightedLPS = lspTable.get_highlighted_cell((1, j)).scale(0.75)
                    lspTable.add_to_back(highlightedLPS)

                    # Continue search comparison * No need to remove colour at it's found
                    j = lps [0][j-1]
                    self.updatePointer(i, j, wLabel, pLabel)
                    self.removeHighlight(patternTable,self.patternHighlights,True) # clear to reset pattern
                    self.horizontalSlide(wordTable, patternTableGroup, i, j)
                    self.wait(1)
                    highlightedLPS.set_opacity(0) # remove highlihgted lps
            # failure function (not matched)
            else:
                #refer to previous entry in lps for new pointer location
                if j != 0:
                    #  Word table should be highlighted in red (incorrect match
                    self.colour(wordTable, patternTableGroup, i, j, False)
                    highlightedLPS = lspTable.get_highlighted_cell((1, j)).scale(0.75)
                    lspTable.add_to_back(highlightedLPS)

                    j = lps[0][j - 1]
                    # update pointer label
                    self.updatePointer(i, j, wLabel, pLabel)
                        # self.removeHighlight(self.colour(wordTable, patternTableGroup, i, j, False)); # not functioning
                        # self.colour(wordTable, patternTableGroup, i, j, True) # do the i - j range

                    self.horizontalSlide(wordTable, patternTableGroup, i, j)
                    self.wait(1)
                    highlightedLPS.set_opacity(0)
                    ## How to remove lps highlight??
                else:
                    self.colour(wordTable, patternTableGroup, i, j, False)
                    i += 1 #Do not update
                    # pointer label
                    ## wLabel, pLabel = self.updatePointer(i, j, wLabel, pLabel, wPointer, pPointer)
                    self.updatePointer(i, j, wLabel, pLabel)
                    self.horizontalSlide(wordTable, patternTableGroup, i, j)



    def construct(self):
        # full word: abababbababaababaa 18 n
        word = [
            ['a','b','a','b','a','b','b','a','b','a','b','a','a','b','a','b','a','a']
        ]
        pattern = [
                ['a','b','a','b','a','a'] # pattern: ababaa 6 m
        ]
        lpsAnswers = [[0, 0, 1, 2, 3,1]]
        #'0', '0', '1', '2', '3', '1'

        phrasePattern = ''.join(pattern[0]) # Pattern that needs to be found LOL UNUSED
        ##self.play(Write(Text(wordPattern))) # need to be monim compatible text type

        #Word Table Assembly
        wordTable = Table(word, include_outer_lines=True)

        # Pattern Table Assembly
        patternTable = Table(pattern,include_outer_lines=True)

        # lspTable Assembly
        lspTable = IntegerTable(lpsAnswers,include_outer_lines=True)
        lpsLabel = Text("LPS = ")
        patPosition = Tex(r" $p$ found at ...", font_size=50)

        # General Arrangement

        allTables = VGroup(wordTable,patternTable).scale(0.45)
        # alignment
        allTables.to_edge(LEFT, buff=0.5)
        allTables.to_edge(UP, buff=2)
        self.alignmentArray(wordTable,patternTable,(1,1),(1,1))

        #Label Pattern Grouping
        patternLabel = self.floatingLabel(patternTable, pattern, "DOWN")
        patGroup = VGroup(patternTable, patternLabel)

        #Lps answer,label table Grouping
        lps = VGroup(lpsLabel,lspTable, patPosition).scale(0.75)
        lps.arrange(RIGHT, buff=0.2)
        lps.next_to(allTables, DOWN, buff=1.5)
        patPosition.shift(UP * 0.3)


        # Writing VIsually
        self.floatingLabel(wordTable,word,"UP")
        self.play(Write(wordTable))
        self.play(Write(patternLabel,run_time=1))
        self.play(Write(patternTable))

        self.play(Write(lps))

        ## self.slidingAnimation(patGroup,pattern,wordTable,word,16)

        # Updator for labels i = word index and j = pattern index (maybe not, out of scope from my skills)
        # COMPARISON STEP - Poorly ANimated
        ## KMP implementation
        self.kmp(wordTable,patGroup,word,pattern,lpsAnswers, lps)


# The first time I was experimenting with tables
class TableHigh(Scene):
    # aligns movingtable below staticTable by index/cell
    def alignmentArray (self, wordTable, patternTable, wordCell, patternCell ):
            # Composition - Aligns the cell of word and pattern array
            # REMEMBER MELISA TABLES ARE INDEXED 1 in Manim
            # maybe I should rename to moving and unmoving static tables
            wCell = wordTable.get_cell(wordCell)
            pCell = patternTable.get_cell(patternCell)
            shiftDistance = wCell.get_center() - pCell.get_center()

            patternTable.next_to(wordTable, DOWN, buff=0.5)
            patternTable.shift(RIGHT * shiftDistance)

    # Slides patternTable table by cell/index per word range
    def slidingAnimation (self, movingTable, pattern, staticTable, data, startStatic):
        #Slidy animation - going through each index pattern per Word Range
        for i in range (startStatic, len(data[0]) + 1):
            wordCell = i
            ## Remove highlight
            if wordCell != startStatic:
                ## Removes older - newest highlighed cells
                for r in reversed(range(len(pattern[0]))):
                    self.play(movingTable[r].animate.set_opacity(0), run_time=0.3)
            for j in range(1, len(pattern[0]) + 1):
                targetWord = staticTable.get_cell((1, wordCell))  # WordTable
                currentLetter = movingTable.get_cell((1, j))
                # LetterTable
                ## Only calculates shift distance by x coordinate dist/pos
                shiftDistance = targetWord.get_center()[0] - currentLetter.get_center()[0]

                ## Highlighting current letter cell
                highlight = movingTable.get_highlighted_cell((1, j), color=RED)
                movingTable.add_to_back(highlight)

                self.play(movingTable.animate.shift(RIGHT * shiftDistance), run_time=0.5)
                self.wait(1)

    def construct(self):
        data = [
            ['a','b','c','d','c','e'],
        ]
        pattern = [
            ['a','b','c']
        ]
        wordPattern = ''.join(pattern[0]) # Pattern that needs to be found
        ##self.play(Write(Text(wordPattern)))

        wordTable = Table(data,
                          include_outer_lines=True,)
        patternTable = Table(pattern,include_outer_lines=True)

        tableGroup = Group(wordTable,patternTable)
        tableGroup.scale(0.75)
        self.wait(2)

        ## Creating floating labels
        w_colLabels = [Text(str(i)) for i in range(len(data[0]))]  # WordTable data count
        for i, label in enumerate(w_colLabels):
            # Get the center of the cell in row 1, column i+1
            cell = wordTable.get_cell((1, i + 1))
            label.next_to(cell.get_top(), UP, buff=0.3)  # Slightly above the cell array
            self.play(Write(label,run_time=0.2))

        ##Inital Position / Composition
        self.alignmentArray(wordTable,patternTable,(1,1),(1,3))
        self.play(Write(wordTable))
        self.play(Write(patternTable))
        self.wait(3)

        ## Sliding + get_highlighted_cell
        self.slidingAnimation(patternTable,pattern,wordTable,data,5)

        ## checked = patternTable.get_highlighted_cell((1,1),color = RED)


        ## These two over write each other
        ## patternTable.shift()
        ## patternTable.shift(wCell.get_center() - pCell.get_center())

# Ignore
class ScrappedSnippets(Scene):
    def hardcodeTableConstruct(self):

        ### LPS TABLE ANIMATION (Forgive me for the hard-code)
        # Index 0
        highlight = patternTable.get_highlighted_cell((1, 1), color=RED)
        patternTable.add_to_back(highlight)
        self.wait(1)
            # lps update
        targetCell = lspTable.get_entries_without_labels((1, 1))  # wtf is get_entries_without_labels
        self.play(targetCell.animate.become(Text(lpsAnswers[0][0])).move_to(targetCell))

        highlight.set_opacity(0)
        #index 2 - end
        highlight = patternTable.get_highlighted_cell((1, 2), color=RED)
        patternTable.add_to_back(highlight)
        self.wait(1)
            # lps update
        targetCell = lspTable.get_entries_without_labels((1, 2))  # wtf is get_entries_without_labels
        self.play(targetCell.animate.become(Text(lpsAnswers[0][1])).move_to(targetCell))
        highlight.set_opacity(0)

        # Index 3
        highlight = patternTable.get_highlighted_cell((1, 3), color=GREEN)
        patternTable.add_to_back(highlight)
        self.wait(1)
        highlight = patternTable.get_highlighted_cell((1, 1), color=BLUE)
        patternTable.add_to_back(highlight)
            # lps update
        targetCell = lspTable.get_entries_without_labels((1, 3))  # wtf is get_entries_without_labels
        self.play(targetCell.animate.become(Text(lpsAnswers[0][2])).move_to(targetCell))
        highlight.set_opacity(0)

        ##self.play(movingTable[r].animate.set_opacity(0), run_time=0.3

        ## Update values
        lpsAnswers = [['0','0','1','2','3','1']]

        for i in range(0, len(lsbValues[0])):
            # Chaning table cell value ()
            targetCell = lspTable.get_entries_without_labels((1, i + 1))  # wtf is get_entries_without_labels
            self.play(targetCell.animate.become(Text(lsbValues[0][i])).move_to(targetCell))  ## WORKS with sil animation
            # ## targetCell.become(Text("4").move_to(targetCell)) ## This also works but you need to manualyl play to see changes

    # OLD METHOD THAT STACKED VISUALLY updates pointerGroup to hold current index of pointer i and j
    def updatePointer(self,i,j, wLabel, pLabel, wPointer, pPointer):
        # Track new i,j values
        new_wLabel = Tex(r"i = " + str(i), font_size=25)
        new_pLabel = Tex(r"j = " + str(j), font_size=25)

        # move to previous label location
        new_wLabel.move_to(wLabel.get_center())
        new_pLabel.move_to(pLabel.get_center())
        self.play(Transform(wLabel, new_wLabel), Transform(pLabel, new_pLabel))

        #new_wPointer = VGroup(new_wLabel, wPointer[1])
        #new_pPointer = VGroup(new_pLabel, pPointer[1])

        #update pointer group reference to new label
        wPointer[0] = new_wLabel #more verbose wPointer.submobject[0]
        pPointer[0] = new_pLabel

        return new_wLabel, new_pLabel

    def construct(self):

        ## I am trying to figure out how to make tables of equal size (width x height)
        pattern = [
            ['a', 'b', 'a', 'b', 'a', 'a']
        ]
        lsbValues = [["." for _ in range(6)]]

        patternTable = Table(pattern,include_outer_lines=True)
        lspTable = Table(lsbValues,include_outer_lines=True)

        allTables = VGroup(patternTable,lspTable)
        allTables.arrange(DOWN, buff=0.5)

        rows = len(pattern)
        cols = len(pattern[0])
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                pattern_cell = patternTable.get_cell((r, c))
                lsp_cell = lspTable.get_cell((r, c))
                # Match width and height
                lsp_cell.stretch_to_fit_width(pattern_cell.width)
                lsp_cell.stretch_to_fit_height(pattern_cell.height)

        self.play(Write(allTables)) # wowie you can print groups

        # atetmpting to make same screen
        # Scales entire table up (not expand each individual cell)
        """" 
        lspTable.match_width(patternTable)
        lspTable.match_height(patternTable)

        """



