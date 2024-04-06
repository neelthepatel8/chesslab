import React from "react";
import Image from "next/image";

import pieceImages from "./pieceImages";
const Piece = ({ type, color, ...props }) => {
  const pieceImage = pieceImages[`${color}_${type}`];
  const kingClass = `${type}-${color}`;
  return (
    <div
      className={`chess-piece z-50 transition-transform duration-500 ease-in-out ${kingClass}`}
    >
      {pieceImage && (
        <Image
          {...props}
          priority
          width={100}
          height={100}
          src={pieceImage}
          alt={`${color}-${type}`}
          layout="responsive"
        />
      )}
    </div>
  );
};

export default Piece;
