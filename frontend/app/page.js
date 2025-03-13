import Board from "./components/Board/Board";
import { WebSocketProvider } from "./services/WebSocketContext";

export default function Home() {
  return (
    <WebSocketProvider>
      <main className="flex h-screen w-screen items-center justify-center">
        // <Board />
          <h1>Currently Down due to an issue, work in progress. Expect updates soon.</h1>
      </main>
    </WebSocketProvider>
  );
}
