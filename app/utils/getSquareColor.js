import { SQUARE_COLOR } from "../constants/constants";
import coordsToAlgebraic from "./coordsToAlgebraic";

const squareIsWhite = (s) => s.charCodeAt(0) % 2 !== s.charCodeAt(1) % 2;

export function getSquareColor(rank, file, isSelected) {
  const position = coordsToAlgebraic(rank, file);
  if (squareIsWhite(position))
    return isSelected ? SQUARE_COLOR.SELECTED_WHITE : SQUARE_COLOR.WHITE;
  else return isSelected ? SQUARE_COLOR.SELECTED_BLACK : SQUARE_COLOR.BLACK;
}
