"use client";
import React, { useEffect, useState } from "react";
import Row from "./Row";
import * as fen from "@/app/utils/fenString/fenString";
import { PIECE_COLOR } from "@/app/constants/constants";
import { useWebSocket } from "@/app/services/WebSocketContext";
import { WEBSOCKET } from "@/app/services/constants";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

const currentFen =
  "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2";

const Board = ({ playerColor = PIECE_COLOR.WHITE }) => {
  const [currentFen, setCurrentFen] = useState(
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  );
  const [selectedSquare, setSelectedSquare] = useState([]);

  const { sendMessage, messages, isConnected } = useWebSocket();

  const [currentPlayer, setCurrentPlayer] = useState(
    fen.getCurrentPlayer(currentFen),
  );

  useEffect(() => {
    if (isConnected) {
      const init_message = {
        type: WEBSOCKET.TYPES.INIT,
      };
      sendMessage(init_message);
    }
  }, [isConnected]);

  useEffect(() => {
    const latestMessage = messages[messages.length - 1];
    if (latestMessage) {
      if (
        latestMessage.type === WEBSOCKET.TYPES.UPDATE ||
        latestMessage.type === WEBSOCKET.TYPES.INIT
      ) {
        const newFen = latestMessage.data?.fen;
        setCurrentFen(newFen);
        setCurrentPlayer(fen.getCurrentPlayer(newFen));
      }
    }
  }, [messages]);

  const handleSquareClick = (rank, file, hasPiece, pieceColor) => {
    sendMessage({ data: "hello world!" });
    // if (currentPlayer !== playerColor) return;
    if (selectedSquare.length === 0) {
      if (hasPiece && pieceColor == currentPlayer)
        setSelectedSquare([rank, file]);
    } else {
      if (selectedSquare[0] === rank && selectedSquare[1] === file) {
        setSelectedSquare([]);
      } else {
        if (!hasPiece) {
          const newFen = fen.movePiece(currentFen, selectedSquare, [
            rank,
            file,
          ]);

          setCurrentFen(newFen);
          setCurrentPlayer((old) =>
            old == PIECE_COLOR.WHITE ? PIECE_COLOR.BLACK : PIECE_COLOR.WHITE,
          );
          setSelectedSquare([]);
        }
      }
    }
  };

  return (
    <div className="flex flex-col">
      {rows.map((row) => (
        <Row
          selectedSquare={selectedSquare}
          handleSquareClick={handleSquareClick}
          rowFenString={fen.getRow(currentFen, row)}
          key={`row${row}`}
          index={row}
        />
      ))}
    </div>
  );
};

export default Board;
