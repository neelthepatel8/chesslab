import React from "react";
import Square from "./Square/Square";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";
import { FILE, RANK } from "@/app/constants/constants";
import * as fen from "@/app/utils/fenString/fenString";
import Piece from "../Piece/Piece";
import PromotionOptions from "./PromotionOptions";
const squares = [1, 2, 3, 4, 5, 6, 7, 8];
const Row = ({
  index,
  rowFenString,
  selectedSquare,
  handleSquareClick,
  possibleMoves,
  showPromotionOptions,
  promotionOptions,
  setSelectedPromotion,
}) => {
  const completeRowFen = fen.makeComplete(rowFenString);
  return (
    <div className="flex flex-row">
      {squares.map((square) => (
        <div key={`${square}-${index}`}>
          <Square
            key={coordsToAlgebraic(index, square)}
            rank={index}
            file={square}
            showRank={square == FILE.MIN}
            showFile={index == RANK.MIN}
            position={coordsToAlgebraic(index, square)}
            isSelected={
              selectedSquare[0] == index && selectedSquare[1] == square
            }
            isPossibleMove={possibleMoves.includes(
              coordsToAlgebraic(index, square),
            )}
            handleSquareClick={handleSquareClick}
            pieceColor={fen.getPieceColor(completeRowFen[square - 1])}
            showPromotionOptions={showPromotionOptions}
            promotionOptions={promotionOptions}
            setSelectedPromotion={setSelectedPromotion}
          >
            {completeRowFen[square - 1] !== "X" &&
              fen.getPieceType(completeRowFen[square - 1]) &&
              fen.getPieceColor(completeRowFen[square - 1]) && (
                <Piece
                  type={fen.getPieceType(completeRowFen[square - 1])}
                  color={fen.getPieceColor(completeRowFen[square - 1])}
                />
              )}
          </Square>
        </div>
      ))}
    </div>
  );
};

export default Row;
