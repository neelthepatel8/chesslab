import React from "react";
import Image from "next/image";

import pieceImages from "./pieceImages";
const Piece = ({ type, color, position }) => {
  const pieceImage = pieceImages[`${color}_${type}`];

  return (
    <>
      {pieceImage && (
        <Image
          priority
          width={100}
          height={100}
          src={pieceImage}
          alt={`${color}-${type}`}
        />
      )}
    </>
  );
};

export default Piece;
