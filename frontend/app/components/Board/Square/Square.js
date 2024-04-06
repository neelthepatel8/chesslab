import React from "react";
import { getSquareColor } from "@/app/utils/getSquareColor";
import getTextColor from "@/app/utils/getTextColor";
import numToLetter from "@/app/utils/numToLetter";
import PossibleMoveDot from "../../Dot/PossibleMoveDot";
import PossibleKillRing from "../../Dot/PossibleKillRing";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";
import PromotionOptions from "../PromotionOptions";

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
  showPromotionOptions,
  promotionOptions,
  setSelectedPromotion,
}) => {
  const squareColor = `bg-${getSquareColor(rank, file, isSelected)}`;
  const textColor = `text-${getTextColor(squareColor)}`;
  const pointerStyle = children || isPossibleMove ? "cursor-pointer" : "";

  return (
    <div
      id={`square-${coordsToAlgebraic(rank, file)}`}
      onClick={() => handleSquareClick(rank, file, children, pieceColor)}
      className={`relative pt-1 text-lg  font-bold lg:h-20 lg:w-20 xl:h-[6.2rem] xl:w-[6.2rem] ${pointerStyle} ${squareColor}`}
    >
      {showPromotionOptions &&
        showPromotionOptions[0][0] == rank &&
        showPromotionOptions[0][1] == file && (
          <PromotionOptions
            key={`${rank}-${file}`}
            allowedOptions={promotionOptions}
            setSelectedPromotion={setSelectedPromotion}
          />
        )}
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
