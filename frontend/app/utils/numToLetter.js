const numToLetter = (num) => {
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

  if (num > 8 || num < 1) return "x";
  return num2letter[num];
};

export default numToLetter;
