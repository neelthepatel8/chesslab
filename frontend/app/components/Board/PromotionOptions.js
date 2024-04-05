import React from "react";
import Piece from "../Piece/Piece";
import { PIECE_COLOR } from "@/app/constants/constants";

const PromotionOptions = ({ allowedOptions, setSelectedPromotion }) => {
  const locationClass =
    allowedOptions[0].color == PIECE_COLOR.BLACK ? "bottom-0" : "top-0";
  return (
    <div
      className={`absolute ${locationClass} left-0 z-[2000] rounded-xl bg-white px-1 pb-10 pt-4 drop-shadow-2xl`}
    >
      {allowedOptions &&
        allowedOptions.map((option) => (
          <Piece
            onClick={() => setSelectedPromotion(option)}
            key={option.type}
            className="drop-shadow-2xl"
            type={option.type}
            color={option.color}
          />
        ))}
    </div>
  );
};

export default PromotionOptions;
