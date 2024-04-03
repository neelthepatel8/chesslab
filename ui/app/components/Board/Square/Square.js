import React from "react";
import { getSquareColor } from "@/app/utils/getSquareColor";
import getTextColor from "@/app/utils/getTextColor";
import numToLetter from "@/app/utils/numToletter";
import PossibleMoveDot from "../../Dot/PossibleMoveDot";
import PossibleKillRing from "../../Dot/PossibleKillRing";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";

const Square = ({
  children,
  rank,
  file,
  position,
  showFile,
  showRank,
  isSelected,
  isPossibleMove,
  handleSquareClick,
  pieceColor,
}) => {
  const squareColor = `bg-${getSquareColor(rank, file, isSelected)}`;
  const textColor = `text-${getTextColor(squareColor)}`;
  const pointerStyle = children || isPossibleMove ? "cursor-pointer" : "";

  return (
    <div
      id={`square-${coordsToAlgebraic(rank, file)}`}
      onClick={() => handleSquareClick(rank, file, children, pieceColor)}
      className={`relative h-[6.2rem] w-[6.2rem]  pt-1 text-lg font-bold ${pointerStyle} ${squareColor}`}
    >
      {isPossibleMove && !children && (
        <div className="flex h-full w-full items-center justify-center">
          <PossibleMoveDot
            size={"65px"}
            color={"black"}
            className="opacity-10"
          />
        </div>
      )}
      {showFile && (
        <div className={`absolute bottom-0 right-2 ${textColor}`}>
          {numToLetter(file)}
        </div>
      )}
      {showRank && (
        <div className={`absolute left-2 top-1 ${textColor}`}>{rank}</div>
      )}
      {isPossibleMove && children ? (
        <div className="relative">
          <div className="absolute z-20">{children}</div>
          <PossibleKillRing
            size={"100px"}
            className="absolute z-10  opacity-20 "
          />
        </div>
      ) : (
        <>{children}</>
      )}
    </div>
  );
};

export default Square;
