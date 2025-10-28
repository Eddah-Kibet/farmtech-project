import { Routes, Route } from "react-router-dom"; 
import HomePage from "./pages/HomePage";
import SideBar from "./components/SideBar";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/sidebar" element={<SideBar />} />
    </Routes>
  );
}

export default App;