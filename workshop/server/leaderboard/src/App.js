import { QueryClient, QueryClientProvider } from "react-query";

import "./App.css";

import Leaderboard from "./Leaderboard";

const queryClient = new QueryClient();

function App() {

  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <header className="App-header">
          <p>PyCon SK 2022 - MicroPython Racetrack</p>
        </header>
        <div className="container mx-auto">
          <Leaderboard />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
