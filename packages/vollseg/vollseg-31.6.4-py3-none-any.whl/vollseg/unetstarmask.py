class UnetStarMask:
    def __init__(self, boxA, cordB):

        self.boxA = boxA
        self.cordB = cordB

    def semi_masking(self):

        self.masksemiD()
        return self.semiinclude

    def masking(self):

        self.masknD()

        return self.include

    def masknD(self):

        self.ndim = len(self.cordB)

        self.include = False
        includelist = [self.Conditioncheck(p) for p in range(0, self.ndim)]
        if True in includelist:
            self.include = True

    def Conditioncheck(self, p):

        include = True

        if self.cordB[p] >= self.boxA[p] and self.cordB[p] <= self.boxA[p + self.ndim]:

            include = False

        return include

    def masksemiD(self):

        self.ndim = len(self.cordB)

        self.semiinclude = False
        includelist = [self.Conditioncheck(p) for p in range(1, self.ndim)]
        if True in includelist:
            self.semiinclude = True
