import React from "react";

const PossibleKillRing = ({ color, size, className }) => {
  return (
    <svg
      className={`responsive-svg ${className}`}
      stroke={color}
      fill={color}
      strokeWidth="0"
      viewBox="0 0 512 512"
      height={size}
      width={size}
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200z"></path>
    </svg>
  );
};

export default PossibleKillRing;
