"use client";
import React, { useEffect, useState } from "react";
import Row from "./Row";
import * as fen from "@/app/utils/fenString/fenString";
import { PIECE_COLOR } from "@/app/constants/constants";
import { useWebSocket } from "@/app/services/WebSocketContext";
import { WEBSOCKET } from "@/app/services/constants";
import coordsToAlgebraic from "@/app/utils/coordsToAlgebraic";
import log from "@/app/utils/log";
import useSound from "use-sound";
import { algebraicToCoords } from "@/app/utils/algebraicToCoords";

const rows = [1, 2, 3, 4, 5, 6, 7, 8].reverse();

const Board = () => {
  const [config, setConfig] = useState({});
  const [currentFen, setCurrentFen] = useState("");
  const [selectedSquare, setSelectedSquare] = useState([]);

  const { sendMessage, messages, isConnected } = useWebSocket();

  const [messageQueue, setMessageQueue] = useState([]);

  const [currentPlayer, setCurrentPlayer] = useState(
    fen.getCurrentPlayer(currentFen),
  );

  const [possibleMoves, setPossibleMoves] = useState([]);

  const [currentMoving, setCurrentMoving] = useState([[], []]);
  const [rookMoving, setRookMoving] = useState([]);

  const [showPromotionOptions, setShowPromotionOptions] = useState([
    [],
    PIECE_COLOR.BLACK,
  ]);
  const [selectedPromotion, setSelectedPromotion] = useState({});

  // Sound Effects:
  const [playMove] = useSound("sfx/move.mp3", { volume: 1 });
  const [playMoveCheck] = useSound("sfx/move.mp3", { volume: 5 });
  const [playCapture] = useSound("sfx/capture.mp3", { volume: 1 });
  const [playCaptureCheck] = useSound("sfx/capture.mp3", { volume: 5 });
  const [playCheck] = useSound("sfx/check.mp3", { volume: 1 });
  const [playCheckmate] = useSound("sfx/checkmate.mp3", { volume: 1 });
  const [playStalemate] = useSound("sfx/stalemate.mp3", { volume: 1 });
  const [playPromotion] = useSound("sfx/promotion.mp3", { volume: 1 });

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
  }, [isConnected, sendMessage]);

  useEffect(() => {
    if (messages.length > 0) {
      const latestMessage = messages[messages.length - 1];
      setMessageQueue((prevQueue) => [...prevQueue, latestMessage]);
    }
  }, [messages]);

  useEffect(() => {
    if (messageQueue.length > 0) {
      const processMessage = async (message) => {
        handleWebSockMessaging(message);

        await new Promise((resolve) => setTimeout(resolve, 200));

        setMessageQueue((prevQueue) => prevQueue.slice(1));
      };

      processMessage(messageQueue[0]);
    }
  }, [messageQueue]);

  const handleInitMessage = (message) => {
    const newFen = message.data?.fen;
    setCurrentFen(newFen);
    setCurrentPlayer(fen.getCurrentPlayer(newFen));
    setPossibleMoves([]);
    setSelectedSquare([]);
  };

  const handleConfigMessage = (message) => {
    setConfig(message.data?.constants);
  };

  const handleMakeMoveMessage = async (message) => {
    if (message.data?.move_success) {
      const special = message.data?.special;
      await animateMove(
        message.data?.from_pos,
        message.data?.to_pos,
        message.data?.fen,
        message.data?.is_kill === config.KILL,
        special === config.CHECK || special === config.CASTLED_CHECK,
        special === config.PROMOTE_POSSIBLE,
        special === config.CASTLED_CHECK || special === config.CASTLED_NO_CHECK,
      ).then(() => {
        if (special === config.CHECKMATE) {
          handleCheckmate();
        } else if (special === config.STALEMATE) {
          handleStalemate(message.data?.fen);
        }
      });

      if (
        currentPlayer == PIECE_COLOR.WHITE &&
        special !== config.PROMOTE_POSSIBLE
      ) {
        await setTimeout(wsRequestEngineMove, 500);
      }
    }
    setPossibleMoves([]);
    setSelectedSquare([]);
  };

  const handlePossibleMovesMessage = (message) => {
    const possibleMoves = message.data?.possible_moves;
    setPossibleMoves(possibleMoves);
  };

  const handlePromotePawnMessage = async (message) => {
    const updatedFen = message.data?.fen;
    setCurrentFen(updatedFen);
    setCurrentPlayer(fen.getCurrentPlayer(updatedFen));
    setPossibleMoves([]);
    setSelectedSquare([]);
    setShowPromotionOptions([[], PIECE_COLOR.BLACK]);
    setSelectedPromotion([]);
    setCurrentMoving([[], []]);

    if (message.data?.special === config.CHECKMATE) {
      handleCheckmate();
    } else if (message.data?.special === config.STALEMATE) {
      handleStalemate(updatedFen);
    } else if (message.data?.special === config.CHECK) {
      handleCheck();
    }

    if (currentPlayer == PIECE_COLOR.BLACK) {
      await setTimeout(wsRequestEngineMove, 500);
    }
  };

  const handleWebSockMessaging = async (latestMessage) => {
    if (!latestMessage) {
      log("No Message to process..");
      return;
    }

    console.log("Processing message ", latestMessage);
    if (latestMessage.error < 0) {
      log("Received error from backend: ", latestMessage);
      return;
    }

    switch (latestMessage.type) {
      case WEBSOCKET.TYPES.INIT:
        handleInitMessage(latestMessage);
        break;
      case WEBSOCKET.TYPES.CONFIG:
        handleConfigMessage(latestMessage);
        break;
      case WEBSOCKET.TYPES.MAKE_MOVE:
        await handleMakeMoveMessage(latestMessage);
        break;
      case WEBSOCKET.TYPES.POSSIBLE_MOVES:
        handlePossibleMovesMessage(latestMessage);
        break;
      case WEBSOCKET.TYPES.PROMOTE_PAWN:
        await handlePromotePawnMessage(latestMessage);
        break;
      default:
        break;
    }
  };

  useEffect(() => {
    if (showPromotionOptions[0].length > 0) playPromotion();
  }, [showPromotionOptions]);

  useEffect(() => {
    if (selectedPromotion?.type) {
      wsPromotePawn(showPromotionOptions[0]);
    }
  }, [selectedPromotion]);

  const handleCheckmate = async () => {
    const king = document.querySelector(
      `.king-${fen.getCurrentPlayer(currentFen) == PIECE_COLOR.BLACK ? "white" : "black"}`,
    );

    setTimeout(() => {
      playCheckmate();
      const kingSquare = king.parentElement;
      flickerSquare(
        kingSquare,
        8,
        300,
        kingSquare.classList.contains("bg-squarewhite"),
      );
    }, 200);
  };
  const handleStalemate = async (fenStr = currentFen) => {
    const blackKingLocation = fen.getKingLocationFromFen(
      fenStr,
      PIECE_COLOR.BLACK,
    );
    const whiteKingLocation = fen.getKingLocationFromFen(
      fenStr,
      PIECE_COLOR.WHITE,
    );
    const blackKingSquare = document.getElementById(
      `square-${blackKingLocation}`,
    );
    const whiteKingSquare = document.getElementById(
      `square-${whiteKingLocation}`,
    );

    setTimeout(() => {
      playStalemate();
      flickerSquare(
        blackKingSquare,
        8,
        300,
        blackKingSquare.classList.contains("bg-squarewhite"),
        true,
      );
      flickerSquare(
        whiteKingSquare,
        8,
        300,
        whiteKingSquare.classList.contains("bg-squarewhite"),
        true,
      );
    }, 300);
  };

  const handleCheck = () => {
    const king = document.querySelector(
      `.king-${fen.getCurrentPlayer(currentFen) == PIECE_COLOR.WHITE ? "white" : "black"}`,
    );
    setTimeout(() => {
      playCheck();
      const kingSquare = king.parentElement;

      flickerSquare(
        kingSquare,
        2,
        300,
        kingSquare.classList.contains("bg-squarewhite"),
      );
    }, 200);
  };

  const animateMove = async (
    fromPos,
    toPos,
    newFen,
    isKill = false,
    isCheck = false,
    isPromote = false,
    isCastle = false,
    movingRook = false,
  ) => {
    const [from_rank, from_file] = movingRook
      ? rookMoving[0]
      : algebraicToCoords(fromPos);
    const [to_rank, to_file] = movingRook
      ? rookMoving[1]
      : algebraicToCoords(toPos);

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
        `.king-${fen.getCurrentPlayer(currentFen) == PIECE_COLOR.BLACK ? "white" : "black"}`,
      );

      piece.style.position = "relative";
      piece.style.zIndex = 1000;
      piece.style.transform = `translate3d(${transformX}px, ${transformY}px, 0)`;

      function handleMoveOutcome() {
        const executeMoveLogic = () => {
          if (isPromote) {
            setShowPromotionOptions([currentMoving[1], currentPlayer]);
            return;
          }

          if (isCheck) {
            playMoveCheck();
            if (king) {
              setTimeout(playCheck, 200);
              const kingSquare = king.parentElement;
              flickerSquare(
                kingSquare,
                2,
                300,
                kingSquare.classList.contains("bg-squarewhite"),
              );
            }
          }

          if (isKill) {
            isCheck ? playCaptureCheck() : playCapture();
          } else {
            playMove();
          }
        };

        if (!movingRook) {
          setTimeout(executeMoveLogic, 200);
        }
      }

      handleMoveOutcome();

      if (movingRook) {
        setTimeout(() => {
          playMove();
        }, 400);
      }

      setTimeout(async () => {
        if (isCastle) {
          await animateMove(newFen, false, false, false, false, true);
        } else {
          setCurrentFen(newFen);
          setCurrentPlayer(fen.getCurrentPlayer(newFen));
          setCurrentMoving([[], []]);
          setRookMoving([[], []]);
          piece.style.transform = "";
          piece.style.zIndex = "";
        }
      }, 500);

      return true;
    }

    return false;
  };

  const flickerSquare = (
    element,
    times,
    interval,
    white = true,
    stalemate = false,
  ) => {
    const classOn = stalemate ? "#89CFF0" : white ? "#EB896F" : "#E2553E";
    const classOff = stalemate ? "#D3D3D3" : white ? "#eeeed2" : "#769656";

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

  const wsMovePiece = async (from_pos, to_pos) => {
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

  const wsPromotePawn = (at_pos) => {
    const message = {
      type: WEBSOCKET.TYPES.PROMOTE_PAWN,
      data: {
        position: coordsToAlgebraic(at_pos[0], at_pos[1]),
        promote_to: selectedPromotion?.type,
      },
    };

    sendMessage(message);
  };

  const wsRequestEngineMove = () => {
    const message = {
      type: WEBSOCKET.TYPES.NEXT_MOVE,
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
      if (selectedSquare.length > 0) {
        const moving_from = coordsToAlgebraic(
          selectedSquare[0],
          selectedSquare[1],
        );

        const piece_name = fen.getPieceAt(currentFen, moving_from);
        if (piece_name?.toLowerCase() === "k") {
          if (Math.abs(file - selectedSquare[1]) > 1) {
            if (moving_from == "e1") {
              setRookMoving([
                algebraicToCoords(file > selectedSquare[1] ? "h1" : "a1"),
                algebraicToCoords(file > selectedSquare[1] ? "f1" : "d1"),
              ]);
            } else if (moving_from == "e8") {
              setRookMoving([
                algebraicToCoords(file > selectedSquare[1] ? "h8" : "a8"),
                algebraicToCoords(file > selectedSquare[1] ? "f8" : "d8"),
              ]);
            }
          }
        }
        wsMovePiece(selectedSquare, [rank, file]);
      }
    }
  };

  const generatePromotionOptions = () => {
    const options = [];
    const allowedPieceNames = ["queen", "rook", "knight", "bishop"];
    allowedPieceNames.forEach((piece) => {
      options.push({
        type: piece,
        color: showPromotionOptions[1],
      });
    });
    return options;
  };

  return (
    <div className="flex flex-col overflow-hidden  drop-shadow-2xl">
      {rows.map((row) => (
        <Row
          possibleMoves={possibleMoves}
          selectedSquare={selectedSquare}
          handleSquareClick={handleSquareClick}
          rowFenString={fen.getRow(currentFen, row)}
          key={`row${row}`}
          index={row}
          showPromotionOptions={showPromotionOptions}
          promotionOptions={generatePromotionOptions()}
          setSelectedPromotion={setSelectedPromotion}
        />
      ))}
    </div>
  );
};

export default Board;
