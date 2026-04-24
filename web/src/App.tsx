import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

// Rutas stub — se implementan en Sprint 2+ (RP7, RP9)
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<div>Login — pendiente RP7</div>} />
          <Route
            path="/admin"
            element={<div>Panel Admin — pendiente RP7</div>}
          />
          <Route
            path="/portal/:token"
            element={<div>Portal Cliente — pendiente RP9</div>}
          />
          <Route path="*" element={<div>Wireless HeatMapper</div>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
