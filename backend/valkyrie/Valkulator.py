import engine.MoveGen.setup as setup

class Valkulator:
  MODES = [LAZY, NORMAL, EAGER] = range(3)

  def __init__(self):

    self.pieceSquareTables = setup.PieceSquareTables
    self.masks = setup.load_evaluation_masks()

    self.pieceValues = (
      1,  # PAWN
      3,  # BISHOP
      3,  # KNIGHT
      5,  # ROOK
      9,  # QUEEN
      0   # KING
    )

    self.weights = (
      1.5,    # Material
      0.001,   # Piece Square Table Values
      1,      # development
      0.3,      # Center Control
      0.02,   # tempo bonus
      5,      # Connectivity
      3,      # Mobility
      0.2,   # Bishop Pair bonus
      2,     # Pawn structure score
      1,      #pressure
    )

    self.memo = [{} for _ in range(len(Valkulator.MODES))]

  def __call__(self, board, *args, mode=NORMAL):
    scores = [score(board,*args) for score in self.get_scores(mode)]
    dot_product = lambda l1,l2: sum(v1*v2 for v1,v2 in zip(l1,l2))
    valuation = dot_product(scores, self.weights)

    return valuation

  def score(func):
    def decorator(self, *args):
      whiteScore = func(self, 0, *args)
      blackScore = func(self, 1, *args)
      return round(whiteScore - blackScore, 4)
    return decorator

  @score
  def material(self, color, board, *args):
    pieces = board.pieces.get_color(color)
    pieceValues = map(lambda p: self.pieceValues[p[1]], pieces)
    return sum(pieceValues)

  @score
  def piece_square_value(self, color, board, *args):
    
    # For each piece, a piece square table contains a score for every
    # square indicating the strength of a square for that piece.
    pieces =  board.pieces.get_color(color)
    tables = self.pieceSquareTables[color]
    pst_values = map(lambda piece: tables[piece[1]][piece[0]], pieces)
    return sum(pst_values) / board.pieces.size(color)

  @score
  def development(self, color, board, *args):
    isPieceDeveloped = lambda mask: mask & board.colors[color] == 0
    developmentMap = map(isPieceDeveloped, self.masks.minorPieceSquares[color])
    return sum(developmentMap) / 4 # 4 minor pieces per color


  @score
  def center_control(self, color, board, attacks):
    def countCenterSquares(attack):
      isAttackingSquare = lambda square: attack & square != 0
      return sum(map(isAttackingSquare, self.masks.centerSquares))
    return sum(map(countCenterSquares, attacks[color]))

  @score
  def connectivity(self, color, board, attacks):
    def countDefences(attack):
      isDefendingPiece = lambda p: p[0] & attack != 0
      return sum(map(isDefendingPiece, board.pieces.get_color(color)))
    defenceBoolMap = map(countDefences, attacks[color])
    return sum(defenceBoolMap) / board.pieces.size(color)

  @score
  def mobility(self, color, board, attacks):
    pass

  @score
  def king_safety(self, board, attacks, color):
    # TODO
    pass

  @score
  def pawn_structure(self, board, attacks, color):
    # TODO
    pass

  @score
  def pressure(self, board, attacks, color):
    # TODO
    pass

  @score
  def tempo(self, color, board, *args):
    # The purpose of a tempo bonus is to discourage cyclical repetitions.
    return int(board.active == color)

  def get_scores(self, mode):
    # Lazy Evaluation
    yield from (self.material, self.piece_square_value)
    if mode == 0: return

    # Normal Evaluation
    yield from (self.development, self.center_control, self.connectivity)
    if mode == 1: return

    # Eager Evaluation
    yield from (self.mobility, self.king_safety, self.connectivity, self.king_safety, self.pawn_structure, self.pressure)