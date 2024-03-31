import numToLetter from "@/app/utils/numToletter";
import React from "react";

const Square = ({ rank, file, position, showFile, showRank }) => {
  return (
    <div className="relative h-24  w-24 border-2 border-solid">
      {showFile && (
        <div className="absolute bottom-1 right-2">{numToLetter(file)}</div>
      )}
      {showRank && <div className="absolute left-2 top-1">{rank}</div>}
      <div className="flex h-full w-full items-center justify-center"></div>
    </div>
  );
};

export default Square;
