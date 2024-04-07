import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Typography,
  Container,
  Paper,
  LinearProgress,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

const Input = styled("input")({
  display: "none",
});

export default function DataUploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (file) {
      setIsUploading(true);

      // Create a FormData instance to build the form request
      const formData = new FormData();
      formData.append("file", file);
      // Append the 'uploaded_on' field with the current datetime in ISO format
      formData.append("uploaded_on", new Date().toISOString());

      // Use the fetch API to POST the form data
      fetch("http://localhost:8000/data_cleanser/upload-file/", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            return response.json(); // or response.text() if the response is not in JSON format
          }
          throw new Error("Network response was not ok.");
        })
        .then((data) => {
          console.log("File uploaded successfully:", data);
          // Perform any additional actions with the response data

          // Navigate to Dashboard
          navigate("/dashboard", { state: { data: data } });
        })
        .catch((error) => {
          console.error(
            "There has been a problem with your fetch operation:",
            error
          );
        })
        .finally(() => {
          setIsUploading(false);
          setFile(null);
        });
    } else {
      alert("Please select a file to upload.");
    }
  };

  return (
    <Container component="main" width="100%">
      <Paper
        elevation={6}
        sx={{
          my: 8,
          p: 2,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="h6" gutterBottom>
          Upload Your Data File
        </Typography>
        <Typography variant="body2" sx={{ mb: 3 }}>
          Please select a CSV or Excel file to upload. The file should contain
          your dataset for processing.
        </Typography>
        <label htmlFor="contained-button-file">
          <Input
            accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
            id="contained-button-file"
            multiple
            type="file"
            onChange={handleFileChange}
          />
          <Button
            variant="contained"
            component="span"
            startIcon={<CloudUploadIcon />}
            sx={{ mb: 2 }}
          >
            Select File
          </Button>
        </label>
        {file && (
          <Box sx={{ width: "100%", mb: 2 }}>
            <Typography variant="body2" gutterBottom>
              Selected file: {file.name}
            </Typography>
            {isUploading && <LinearProgress />}
          </Box>
        )}
        <Button
          variant="outlined"
          onClick={handleFileUpload}
          disabled={!file || isUploading}
        >
          Upload File
        </Button>
      </Paper>
    </Container>
  );
}
