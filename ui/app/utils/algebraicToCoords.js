export const algebraicToCoords = (algebraic) => {
  const fileToNum = { a: 1, b: 2, c: 3, d: 4, e: 5, f: 6, g: 7, h: 8 };
  const fileLetter = algebraic[0];

  const rankNumber = parseInt(algebraic[1], 10);
  const fileNumber = fileToNum[fileLetter];

  return [rankNumber, fileNumber];
};
