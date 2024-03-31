import React from "react";
import Square from "./Square/Square";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";
import { FILE, RANK } from "@/app/constants/constants";

const squares = [1, 2, 3, 4, 5, 6, 7, 8];

const Row = ({ index }) => {
  return (
    <div className="flex flex-row">
      {squares.map((square) => (
        <Square
          key={coordsToAlgebraic(index, square)}
          rank={index}
          file={square}
          showRank={square == FILE.MIN}
          showFile={index == RANK.MIN}
          position={coordsToAlgebraic(index, square)}
        ></Square>
      ))}
    </div>
  );
};

export default Row;
