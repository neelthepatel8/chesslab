import React from "react";

const PossibleMoveDot = ({ color, size, className }) => {
  return (
    <svg
      className={`lg:responsive-svg-dot ${className}`}
      stroke={color}
      fill={color}
      strokeWidth="0"
      viewBox="0 0 24 24"
      height={size}
      width={size}
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z"></path>
    </svg>
  );
};

export default PossibleMoveDot;
