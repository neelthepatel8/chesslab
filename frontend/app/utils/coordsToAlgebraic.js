export default function coordsToAlgebraic(i, j) {
  const row = i;
  const num2letter = {
    1: "a",
    2: "b",
    3: "c",
    4: "d",
    5: "e",
    6: "f",
    7: "g",
    8: "h",
  };

  if (j > 8 || j < 1) return "x";
  const col = num2letter[j];

  return `${col}${row}`;
}
