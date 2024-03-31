import { SQUARE_COLOR } from "../constants/constants";
import coordsToAlgebraic from "./coordsToAlgebraic";

const squareIsWhite = (s) => s.charCodeAt(0) % 2 !== s.charCodeAt(1) % 2;

export function getSquareColor(rank, file) {
  const position = coordsToAlgebraic(rank, file);
  if (squareIsWhite(position)) return SQUARE_COLOR.WHITE;
  else return SQUARE_COLOR.BLACK;
}
