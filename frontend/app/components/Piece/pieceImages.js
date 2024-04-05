const pieceNameMap = {
  black_bishop: "bB",
  black_king: "bK",
  black_knight: "bN",
  black_pawn: "bP",
  black_queen: "bQ",
  black_rook: "bR",
  white_bishop: "wB",
  white_king: "wK",
  white_knight: "wN",
  white_pawn: "wP",
  white_queen: "wQ",
  white_rook: "wR",
};

const pieceImages = Object.fromEntries(
  Object.entries(pieceNameMap).map(([key, value]) => [
    key,
    `/pieces/${value}.svg`,
  ]),
);

export default pieceImages;
