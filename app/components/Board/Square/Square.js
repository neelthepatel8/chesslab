import React from "react";
import { getSquareColor } from "@/app/utils/getSquareColor";
import getTextColor from "@/app/utils/getTextColor";
import numToLetter from "@/app/utils/numToletter";

const Square = ({
  children,
  rank,
  file,
  position,
  showFile,
  showRank,
  isSelected,
  handleSquareClick,
  pieceColor,
}) => {
  const squareColor = `bg-${getSquareColor(rank, file, isSelected)}`;
  const textColor = `text-${getTextColor(squareColor)}`;
  const pointerStyle = children ? "cursor-pointer" : "";

  return (
    <div
      onClick={() => handleSquareClick(rank, file, children, pieceColor)}
      className={`relative h-[6.5rem] w-[6.5rem]  pt-1 text-lg font-bold ${pointerStyle} ${squareColor}`}
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
