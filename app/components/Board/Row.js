import React from "react";
import Square from "./Square/Square";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";
import { FILE, RANK } from "@/app/constants/constants";
import * as fen from "@/app/utils/fenString/fenString";
import Piece from "../Piece/Piece";

const squares = [1, 2, 3, 4, 5, 6, 7, 8];
const Row = ({ index, rowFenString, selectedSquare, handleSquareClick }) => {
  const completeRowFen = fen.makeComplete(rowFenString);
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
          isSelected={selectedSquare[0] == index && selectedSquare[1] == square}
          handleSquareClick={handleSquareClick}
          pieceColor={fen.getPieceColor(completeRowFen[square - 1])}
        >
          {completeRowFen[square - 1] !== "X" &&
            fen.getPieceType(completeRowFen[square - 1]) && (
              <Piece
                type={fen.getPieceType(completeRowFen[square - 1])}
                color={fen.getPieceColor(completeRowFen[square - 1])}
              />
            )}
        </Square>
      ))}
    </div>
  );
};

export default Row;
