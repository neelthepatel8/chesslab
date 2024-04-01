import { PIECE_COLOR } from "@/app/constants/constants";

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

  if (!piece) return console.log(piece);
  return pieces[piece.toLowerCase()];
};

export const getPieceColor = (piece) =>
  piece.toLowerCase() === piece ? PIECE_COLOR.BLACK : PIECE_COLOR.WHITE;

export const getCurrentPlayer = (fen) => {
  const [placement, turn, ...a] = fen.split(" ");
  if (turn === "w") return PIECE_COLOR.WHITE;
  else return PIECE_COLOR.BLACK;
};

export const movePiece = (fen, from, to) => {
  const [placement, turn, castling, enPassant, halfMove, fullMove] =
    fen.split(" ");

  const rows = placement.split("/").map((row) => {
    let expandedRow = [];
    for (const char of row) {
      if (isNaN(parseInt(char))) {
        expandedRow.push(char);
      } else {
        expandedRow.push(...Array(parseInt(char)).fill("1"));
      }
    }
    return expandedRow;
  });

  const fromRankIndex = from[0] - 1;
  const fromFileIndex = from[1] - 1;
  const toRankIndex = to[0] - 1;
  const toFileIndex = to[1] - 1;

  const piece = rows[fromRankIndex][fromFileIndex];
  rows[fromRankIndex][fromFileIndex] = "1";
  rows[toRankIndex][toFileIndex] = piece;

  const newPlacement = rows
    .map((row) => {
      let result = "";
      let emptyCount = 0;
      for (const square of row) {
        if (square === "1") {
          emptyCount++;
        } else {
          if (emptyCount > 0) {
            result += emptyCount.toString();
            emptyCount = 0;
          }
          result += square;
        }
      }
      if (emptyCount > 0) {
        result += emptyCount.toString();
      }
      return result;
    })
    .join("/");

  const newTurn = turn === "w" ? "b" : "w";

  const newFullMove = turn === "b" ? parseInt(fullMove) + 1 : fullMove;

  return `${newPlacement} ${newTurn} ${castling} ${enPassant} ${halfMove} ${newFullMove}`;
};
