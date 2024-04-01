"use client";
import React, { useEffect, useState } from "react";
import Row from "./Row";
import * as fen from "@/app/utils/fenString/fenString";
import { PIECE_COLOR } from "@/app/constants/constants";
import { useWebSocket } from "@/app/services/WebSocketContext";
import { WEBSOCKET } from "@/app/services/constants";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

const Board = ({ playerColor = PIECE_COLOR.WHITE }) => {
  const [currentFen, setCurrentFen] = useState("");
  const [selectedSquare, setSelectedSquare] = useState([]);

  const { sendMessage, messages, isConnected } = useWebSocket();

  const [currentPlayer, setCurrentPlayer] = useState(
    fen.getCurrentPlayer(currentFen),
  );

  const [possibleMoves, setPossibleMoves] = useState([]);

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
        latestMessage.type === WEBSOCKET.TYPES.INIT ||
        latestMessage.type === WEBSOCKET.TYPES.MAKE_MOVE
      ) {
        console.log("recieved message: ", latestMessage);
        if (latestMessage.error) return;
        const newFen = latestMessage.data?.fen;
        setCurrentFen(newFen);
        setCurrentPlayer(fen.getCurrentPlayer(newFen));
        setPossibleMoves([]);
        setSelectedSquare([]);
      } else if (latestMessage.type === WEBSOCKET.TYPES.POSSIBLE_MOVES) {
        const possibleMoves = latestMessage.data?.possible_moves;
        setPossibleMoves(possibleMoves);
        console.log("Recieved Possible Moves: ", possibleMoves);
      }
    }
  }, [messages]);

  const wsShowPossibleMoves = (rank, file) => {
    const message = {
      type: WEBSOCKET.TYPES.POSSIBLE_MOVES,
      data: {
        position: coordsToAlgebraic(rank, file),
      },
    };
    console.log("Sending message", message);
    sendMessage(message);
  };

  const wsMovePiece = (from_pos, to_pos) => {
    const message = {
      type: WEBSOCKET.TYPES.MAKE_MOVE,
      data: {
        from_position: coordsToAlgebraic(from_pos[0], from_pos[1]),
        to_position: coordsToAlgebraic(to_pos[0], to_pos[1]),
      },
    };
    console.log("Sending message", message);
    sendMessage(message);
  };

  const handleSquareClick = (rank, file, hasPiece, pieceColor) => {
    if (hasPiece) {
      if (
        selectedSquare[0] === rank &&
        selectedSquare[1] === file &&
        pieceColor == currentPlayer
      ) {
        setSelectedSquare([]);
        setPossibleMoves([]);
      } else if (
        selectedSquare.length > 0 &&
        fen.getSquarePieceColor(
          currentFen,
          selectedSquare[0],
          selectedSquare[1],
        ) != pieceColor
      ) {
        wsMovePiece(selectedSquare, [rank, file]);
      } else {
        if (pieceColor == currentPlayer) {
          setSelectedSquare([rank, file]);
          wsShowPossibleMoves(rank, file);
        }
      }
    } else {
      if (selectedSquare.length > 0) wsMovePiece(selectedSquare, [rank, file]);
    }
  };

  return (
    <div className="flex flex-col">
      {rows.map((row) => (
        <Row
          possibleMoves={possibleMoves}
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
