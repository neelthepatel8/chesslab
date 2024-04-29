class PieceList(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        
        self.colorCounts = [16, 16]
        self.colorRanges = [(0, 16), (16, 32)]
        self.colorLookup = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.typeLookup =  [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5]
        #                   wp wp wp wp wp wp wp wp wn wn wb wb wr wr wq wk bp bp bp bp bp bp bp bp bn bn bb bb br br bq bk
        self.numPieces = 32
        
    def __iter__(self):
        for index in range(self.numPieces):
            piece = self[index]
            if piece == 0: continue
            pieceType = self.typeLookup[index]
            pieceColor = self.colorLookup[index]
            yield piece, pieceType, pieceColor

    def get_color(self, color):
        start,stop = self.colorRanges[color]
        for index in range(start,stop):
            piece = self[index]
            if piece == 0: continue
            yield piece, self.typeLookup[index]
            
            
    def update(self, p0, p1, color):
        start, end = self.colorRanges[color]
        for index in range(start,end):
            piece = self[index]
            if piece == p0:
                self[index] = p1
                return self.typeLookup[index]
        raise RuntimeError("Cannot update piece")
    
    def remove(self, piece, color):
        self.colorCounts[color] -= 1
        start,end = self.colorRanges[color]
        for index in range(start,end):
            if self[index] == piece:
                self[index] = 0
                return self.typeLookup[index]
        raise RuntimeError(f'Cannot remove piece')
    
    def insert(self, piece, pieceType, color):
        self.colorCounts[color] += 1
        start,end = self.colorRanges[color]
        for index in range(start,end):
            indexCanStorePiece = self[index] == 0 \
                            and self.typeLookup[index]  == pieceType \
                            and self.colorLookup[index] == color

            if indexCanStorePiece:
                self[index] = piece
                return
        raise RuntimeError(f'Cannot insert piece')

    def size(self, color):
        return self.colorCounts[color]