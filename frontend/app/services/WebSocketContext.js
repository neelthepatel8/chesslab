"use client";
import React, {
  createContext,
  useState,
  useEffect,
  useContext,
  useCallback,
} from "react";
import log from "../utils/log";
const WebSocketContext = createContext(null);

export const useWebSocket = () => useContext(WebSocketContext);

export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(
      process.env.NODE_ENV === "development"
        ? "wss://localhost/ws"
        : "wss://backend-chess-7vc9h.ondigitalocean.app/chesslab-backend2/ws",
    );

    ws.onopen = () => {
      log("Connected to Websocket");
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = useCallback(
    (message) => {
      if (socket) {
        socket.send(JSON.stringify(message));
      }
    },
    [socket],
  );

  const contextValue = {
    sendMessage,
    messages,
    isConnected,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};
