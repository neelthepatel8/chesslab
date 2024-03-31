const { SQUARE_COLOR } = require("../constants/constants");

export default function getTextColor(squareColor) {
  return squareColor.includes(SQUARE_COLOR.WHITE)
    ? SQUARE_COLOR.BLACK
    : SQUARE_COLOR.WHITE;
}
