import React from "react";
import { getSquareColor } from "@/app/utils/getSquareColor";
import getTextColor from "@/app/utils/getTextColor";
import numToLetter from "@/app/utils/numToletter";
import Piece from "../../Piece/Piece";

const Square = ({ children, rank, file, position, showFile, showRank }) => {
  const squareColor = `bg-${getSquareColor(rank, file)}`;
  const textColor = `text-${getTextColor(squareColor)}`;
  return (
    <div
      className={`relative h-[6.5rem] w-[6.5rem] text-lg font-bold ${squareColor}`}
    >
      {showFile && (
        <div className={`absolute bottom-0 right-2 ${textColor}`}>
          {numToLetter(file)}
        </div>
      )}
      {showRank && (
        <div className={`absolute left-2 top-1 ${textColor}`}>{rank}</div>
      )}
      {children}
    </div>
  );
};

export default Square;
