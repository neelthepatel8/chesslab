import React from "react";
import Row from "./Row";
import * as fen from "@/app/utils/fenString/fenString";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

// const currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
const currentFen =
  "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2";
const Board = () => {
  return (
    <div className="flex flex-col">
      {rows.map((row) => (
        <Row
          rowFenString={fen.getRow(currentFen, row)}
          key={`row${row}`}
          index={row}
        />
      ))}
    </div>
  );
};

export default Board;
