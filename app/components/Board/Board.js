import React from "react";
import Row from "./Row";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

const Board = () => {
  return (
    <div className="flex flex-col">
      {rows.map((row) => (
        <Row key={`row${row}`} index={row} />
      ))}
    </div>
  );
};

export default Board;
