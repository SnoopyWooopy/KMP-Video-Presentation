# Used to test functionality of KMP algorithm (without the hassle of animation)
class KMP:

    def kmp(self, wordData, patternData, lps):
        wordLength = len(wordData[0]) # length n
        patternLength = len(patternData[0]) # length m
        i = j = 0 # index pointers (i = current word index, j = current pattern index)
        while i < wordLength:
            #current char match sucessfully
            if wordData[0][i] == patternData[0][j]:
                i += 1
                j += 1
                print("i =", i, "j =", j)
                #wordData, patternData
                # word found completely
                if j == patternLength:
                    print("Pattern found at", (i-j))
                    j = lps[0][j-1]
                    print("i =", i, "j =", j)
            # failure function (not matched)
            else:
                #refer to previous entry in lps for new pointer location
                if j != 0:
                    j = lps[0][j - 1]
                    print("i =", i, "j =", j)
                else:
                    i += 1 #Do not update
                    print("i =", i, "j =", j)
    def construct(self):
        word = [
            ['a','b','a','b','a','b','b','a','b','a','b','a','a','b','a','b','a','a']
        ]
        pattern = [
            ['a','b','a','b','a','a'] # pattern: ababaa 6 m
        ]
        lpsAnswers = [[0, 0, 1, 2, 3,1]]

        print("Hello!")
        self.kmp(word, pattern, lpsAnswers)

if __name__ == "__main__":
    kmp_instance = KMP()
    kmp_instance.construct()
