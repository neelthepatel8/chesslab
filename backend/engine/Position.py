class Position():
    def __init__(self, rank=None, file=None, algebraic=None, coords=None):
        if algebraic:
            self.rank = rank 
            self.file = file
            self.algebraic = self.coords_to_algebraic(self.rank, self.file)
            
        elif rank and file:
            self.algebraic = algebraic
            self.rank, self.file = self.algeraic_to_coords(algebraic)
            
        elif coords:
            self.coords = coords
            self.rank, self.file = coords
            self.algebraic = self.coords_to_algebraic(self.rank, self.file) 
            
        else:
            raise TypeError("Incorrect values provided to Position class.")
        
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
    
    def __str__(self):
        return f"{self.algebraic}"
            
            