import "./App.css";
import DashboardPage from "./DashboardPage";
import DataUploadPage from "./DataUploadPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Box, Typography } from "@mui/material";

function App() {
  return (
    <div className="App">
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          pt: 2,
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            fontWeight: "bold",
            color: "#333",
            textTransform: "uppercase",
            letterSpacing: "2px",
            textShadow: "1px 1px 3px rgba(0,0,0,0.1)",
          }}
        >
          Data Cleanser
        </Typography>
      </Box>

      <Router>
        <Routes>
          <Route path="/" element={<DataUploadPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
