class Position():
    def __init__(self, rank=None, file=None, algebraic=None, coords=None, lsrcoords=None):
        
        self.rank = self.file = -1
        self.coords = (-1, -1)
        self.lsrcoords = (-1, -1)
        self.algebraic = ""
        
        try:
            if algebraic:
                self.rank, self.file = self.algebraic_to_coords(algebraic)
                self.algebraic = algebraic
                self.coords = (self.rank, self.file)
                self.lsrcoords = (8 - self.rank, self.file - 1)
                
            elif rank and file:
                if not (1 <= rank <= 8 and 1 <= file <= 8):
                    raise ValueError("Rank and file must be within 1 to 8.")
                self.algebraic = self.coords_to_algebraic(rank, file)
                self.rank, self.file = rank, file
                self.coords = (self.rank, self.file)
                self.lsrcoords = (8 - self.rank, self.file - 1)
                
            elif coords:
                if len(coords) == 2 and all(1 <= x <= 8 for x in coords):
                    self.coords = coords
                    self.rank, self.file = coords
                    self.algebraic = self.coords_to_algebraic(self.rank, self.file) 
                    self.lsrcoords = (8 - self.rank, self.file - 1)

            elif lsrcoords:
                if len(lsrcoords) == 2 and all(0 <= x <= 7 for x in lsrcoords):
                    self.lsrcoords = lsrcoords
                    self.rank, self.file = 8 - lsrcoords[0] , lsrcoords[1] + 1
                    self.coords = (self.rank, self.file)
                    self.algebraic = self.coords_to_algebraic(self.rank, self.file)
                
            elif isinstance(rank, str):
                self.rank, self.file = self.algebraic_to_coords(rank)
                self.algebraic = rank
                self.coords = (self.rank, self.file)
                self.lsrcoords = (8 - rank, file - 1)
                

        except:
            pass
        
    def algebraic_to_coords(self, algebraic):
        file_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

        file_letter = algebraic[0]
        rank_number = 9 - int(algebraic[1])

        file_number = file_to_num[file_letter]

        return rank_number, file_number

    def coords_to_algebraic(self, rank, file):
        num2letter = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }
        new_file = num2letter[file]
        return f"{new_file}{8 + 1 - rank}"
    
    def is_on_board(self):
        return 1 <= self.rank <= 8 and 1 <= self.file <= 8
    
    def __str__(self):
        return f"{self.algebraic}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        return type(self) == type(other) and self.file == other.file and self.rank == other.rank
    
    def __hash__(self) -> int:
        return hash(self.algebraic)
    
    def __lt__(self, other):
        return (self.rank, self.file) < (other.rank, other.file)

    def __le__(self, other):
        return (self.rank, self.file) <= (other.rank, other.file)

    def __gt__(self, other):
        return (self.rank, self.file) > (other.rank, other.file)

    def __ge__(self, other):
        return (self.rank, self.file) >= (other.rank, other.file)
            
    def deep_copy(self):
        return Position(self.rank, self.file)
            