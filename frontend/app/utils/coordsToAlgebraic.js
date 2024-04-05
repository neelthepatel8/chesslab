import numToLetter from "./numToletter";

export default function coordsToAlgebraic(i, j) {
  const row = i;
  const col = numToLetter(j);

  return `${col}${row}`;
}
