"use client";
import React, { useEffect, useState } from "react";
import Row from "./Row";
import * as fen from "@/app/utils/fenString/fenString";
import { PIECE_COLOR } from "@/app/constants/constants";
import { useWebSocket } from "@/app/services/WebSocketContext";
import { WEBSOCKET } from "@/app/services/constants";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";

import useSound from "use-sound";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

const Board = () => {
  const [config, setConfig] = useState({});
  const [currentFen, setCurrentFen] = useState("");
  const [selectedSquare, setSelectedSquare] = useState([]);

  const { sendMessage, messages, isConnected } = useWebSocket();

  const [currentPlayer, setCurrentPlayer] = useState(
    fen.getCurrentPlayer(currentFen),
  );

  const [possibleMoves, setPossibleMoves] = useState([]);

  const [currentMoving, setCurrentMoving] = useState([[], []]);

  // Sound Effects:
  const [playMove] = useSound("sfx/move.mp3");
  const [playMoveCheck] = useSound("sfx/move.mp3", { volume: 5 });
  const [playCapture] = useSound("sfx/capture.mp3");
  const [playCaptureCheck] = useSound("sfx/capture.mp3", { volume: 5 });
  const [playCheck] = useSound("sfx/check.mp3", { volume: 1 });

  useEffect(() => {
    if (isConnected) {
      const initMessage = {
        type: WEBSOCKET.TYPES.INIT,
      };
      sendMessage(initMessage);

      const configurationMessage = {
        type: WEBSOCKET.TYPES.CONFIG,
      };

      sendMessage(configurationMessage);
    }
  }, [isConnected]);

  useEffect(() => {
    const handleWebSockMessaging = async () => {
      const latestMessage = messages[messages.length - 1];
      if (latestMessage) {
        if (latestMessage.error < 0) {
          console.error("Recieved error from backend: ", latestMessage);
          return;
        }

        switch (latestMessage.type) {
          case WEBSOCKET.TYPES.INIT:
            const newFen = latestMessage.data?.fen;
            setCurrentFen(newFen);
            setCurrentPlayer(fen.getCurrentPlayer(newFen));
            setPossibleMoves([]);
            setSelectedSquare([]);
          case WEBSOCKET.TYPES.CONFIG:
            setConfig(latestMessage.data?.constants);
          case WEBSOCKET.TYPES.MAKE_MOVE:
            if (latestMessage.data?.move_success == true) {
              const pieceMoved = await animateMove(
                latestMessage.data?.fen,
                latestMessage.data?.is_kill,
                latestMessage.data?.special == config.CHECK,
              );
              if (!pieceMoved) {
                console.error("Couldnt move piece due to error!");
                return;
              }
            } else {
            }
            setPossibleMoves([]);
            setSelectedSquare([]);
            break;

          case WEBSOCKET.TYPES.POSSIBLE_MOVES:
            const possibleMoves = latestMessage.data?.possible_moves;
            setPossibleMoves(possibleMoves);
            break;

          default:
            break;
        }
      }
    };

    handleWebSockMessaging();
  }, [messages]);

  const animateMove = async (newFen, isKill = false, isCheck = False) => {
    const [from_rank, from_file] = currentMoving[0];
    const [to_rank, to_file] = currentMoving[1];

    const fromSquare = document.getElementById(
      `square-${coordsToAlgebraic(from_rank, from_file)}`,
    );
    const toSquare = document.getElementById(
      `square-${coordsToAlgebraic(to_rank, to_file)}`,
    );
    const piece = fromSquare?.querySelector(".chess-piece");

    if (piece && fromSquare && toSquare) {
      const fromRect = fromSquare.getBoundingClientRect();
      const toRect = toSquare.getBoundingClientRect();
      const transformX = toRect.left - fromRect.left;
      const transformY = toRect.top - fromRect.top;

      const king = document.querySelector(
        `.king-${fen.getCurrentPlayer(currentFen) == "b" ? "white" : "black"}`,
      );

      piece.style.position = "relative";
      piece.style.zIndex = 1000;
      piece.style.transform = `translate3d(${transformX}px, ${transformY}px, 0)`;

      setTimeout(() => {
        if (isKill) {
          if (isCheck) playCaptureCheck();
          else playCapture();
        } else if (isCheck) {
          playMoveCheck();
        } else playMove();

        if (isCheck && king) {
          setTimeout(() => {
            playCheck();
          }, 200);
          const kingSquare = king.parentElement;
          flickerSquare(
            kingSquare,
            2,
            300,
            kingSquare.classList.contains("bg-squarewhite"),
          );
        }
      }, 200);

      setTimeout(() => {
        setCurrentFen(newFen);
        setCurrentPlayer(fen.getCurrentPlayer(newFen));
        piece.style.transform = "";
        piece.style.zIndex = "";
      }, 400);

      return true;
    }

    return false;
  };

  const flickerSquare = (element, times, interval, white = true) => {
    const classOn = white ? "#EB896F" : "#E2553E";
    const classOff = white ? "#eeeed2" : "#769656";

    element.style.background = classOff;
    let isOn = false;

    const flicker = () => {
      isOn = !isOn;
      element.style.background = isOn ? classOn : classOff;

      if (times <= 0) {
        element.style.background = classOff;
        return;
      }

      times -= 1;
      setTimeout(flicker, interval);
    };

    flicker();
  };

  const wsShowPossibleMoves = (rank, file) => {
    const message = {
      type: WEBSOCKET.TYPES.POSSIBLE_MOVES,
      data: {
        position: coordsToAlgebraic(rank, file),
      },
    };
    sendMessage(message);
  };

  const wsMovePiece = (from_pos, to_pos) => {
    setCurrentMoving([from_pos, to_pos]);

    const message = {
      type: WEBSOCKET.TYPES.MAKE_MOVE,
      data: {
        from_position: coordsToAlgebraic(from_pos[0], from_pos[1]),
        to_position: coordsToAlgebraic(to_pos[0], to_pos[1]),
      },
    };
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
