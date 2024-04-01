import React, { createContext, useState, useEffect, useContext } from "react";

const WebSocketContext = createContext(null);

export const useWebSocket = () => useContext(WebSocketContext);

export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://your-backend-server.com");

    ws.onopen = () => {
      console.log("WebSocket Connected");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    ws.onclose = () => {
      console.log("WebSocket Disconnected");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = (message) => {
    if (socket) {
      socket.send(JSON.stringify(message));
    }
  };

  const contextValue = {
    sendMessage,
    messages,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};
