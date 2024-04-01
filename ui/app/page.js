import Board from "./components/Board/Board";
import { WebSocketProvider } from "./contexts/WebSocketContext";

export default function Home() {
  return (
    <WebSocketProvider>
      <main className="flex h-screen w-screen items-center justify-center">
        <Board />
      </main>
    </WebSocketProvider>
  );
}
