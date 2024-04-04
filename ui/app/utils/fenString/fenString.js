import { PIECE_COLOR } from "@/app/constants/constants";
import { algebraicToCoords } from "../algebraicToCoords";
import coordsToAlgebraic from "../coordsToAlgebraic";
export const getRow = (fen, row) => {
  if (!fen) return "8";
  const splitString = fen.split(" ");
  const rows = splitString[0].split("/");

  return rows[8 - row];
};

export const makeComplete = (fenRow) => {
  if (!fenRow) return "";
  const possibleNumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8];

  possibleNumbers.forEach((num) => {
    const regex = new RegExp(num, "g");
    fenRow = fenRow.replace(regex, "X".repeat(num));
  });

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

  if (!piece) return;
  return pieces[piece.toLowerCase()];
};

export const getSquarePieceColor = (fen, rank, file) => {
  const [placement, turn, ...a] = fen.split(" ");
  let rows = placement.split("/");
  rows = rows.map((row) => makeComplete(row));
  if (rows[8 - rank][file - 1].toLowerCase() == rows[8 - rank][file - 1])
    return PIECE_COLOR.BLACK;
  else return PIECE_COLOR.WHITE;
};

export const getPieceColor = (piece) =>
  piece && piece.toLowerCase() === piece
    ? PIECE_COLOR.BLACK
    : PIECE_COLOR.WHITE;

export const getCurrentPlayer = (fen) => {
  if (fen == "") return PIECE_COLOR.WHITE;
  const [placement, turn, ...a] = fen.split(" ");
  if (turn === "w") return PIECE_COLOR.WHITE;
  else return PIECE_COLOR.BLACK;
};

export const getOppositePlayer = (fen) => {
  if (fen == "") return PIECE_COLOR.WHITE;
  const [placement, turn, ...a] = fen.split(" ");
  if (turn === "b") return PIECE_COLOR.WHITE;
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

export const getKingLocationFromFen = (fen, color) => {
  const piecePlacement = fen.split(" ")[0];
  const king = color === PIECE_COLOR.BLACK ? "k" : "K";

  const ranks = piecePlacement.split("/");

  let rankIndex = 8;
  let fileIndex,
    foundKing = false,
    algebraicPosition = "";

  for (const rank of ranks) {
    fileIndex = 0;
    for (const char of rank) {
      if (isNaN(char)) {
        if (char === king) {
          algebraicPosition =
            String.fromCharCode(97 + fileIndex) + rankIndex.toString();
          foundKing = true;
          break;
        }
        fileIndex++;
      } else {
        fileIndex += parseInt(char);
      }
    }
    if (foundKing) break;
    rankIndex--;
  }

  return algebraicPosition;
};

export const getPieceAt = (currentFen, piece_coords) => {
  const boardLayout = currentFen.split(" ")[0];

  const coords = algebraicToCoords(piece_coords);
  const file = coords[1];
  const rank = 9 - coords[0];

  const ranks = boardLayout.split("/");

  const fenRow = ranks[rank - 1];
  console.log(fenRow);

  const expandedRow = fenRow.replace(/\d/g, (match) => ".".repeat(match));
  return expandedRow[file - 1] === "." ? null : expandedRow[file - 1];
};
