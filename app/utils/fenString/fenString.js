export const getRow = (fen, row) => {
  const splitString = fen.split(" ");
  const rows = splitString[0].split("/");

  return rows[row - 1];
};

export const makeComplete = (fenRow) => {
  const possibleNumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8];

  for (let num in possibleNumbers) {
    if (fenRow.includes(num)) {
      fenRow = fenRow.replace(num, "X".repeat(num));
    }
  }

  return fenRow;
};

export const getPieceType = (piece) => {
  const pieces = {
    r: "rook",
    p: "pawn",
    k: "king",
    n: "knight",
    q: "queen",
    b: "bishop",
  };

  return pieces[piece.toLowerCase()];
};

export const getPieceColor = (piece) =>
  piece.toLowerCase() === piece ? "black" : "white";
