import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Typography,
  Container,
  Paper,
  LinearProgress,
  Snackbar,
} from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

const Input = styled("input")({
  display: "none",
});

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export default function DataUploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [snackbarState, setSnackbarState] = useState({
    open: false,
    message: "",
    severity: "error",
    vertical: "bottom",
    horizontal: "center",
  });

  const { vertical, horizontal } = snackbarState;

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (file) {
      setIsUploading(true);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("uploaded_on", new Date().toISOString());

      fetch("http://localhost:8000/data_cleanser/upload-file/", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("File upload failed.");
        })
        .then((data) => {
          navigate("/dashboard", { state: { data: data } });
        })
        .catch((error) => {
          setSnackbarState({
            ...snackbarState,
            open: true,
            message: "Error occured while processing. Please check the format",
            severity: "error",
          });
        })
        .finally(() => {
          setIsUploading(false);
          setFile(null);
        });
    } else {
      alert("Please select a file to upload.");
    }
  };

  const closeSnackbar = () => {
    setSnackbarState({ ...snackbarState, open: false });
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
        <img
          src="data_cleaning_illus.svg"
          alt="Illustration representing data files"
          style={{ width: "40%", height: "auto", padding: "15px" }}
        />
        <Typography variant="h6" gutterBottom>
          Upload Your Data File
        </Typography>
        <Typography variant="body2" sx={{ mb: 3 }}>
          Please select a CSV or Excel file to upload. The file should contain
          your dataset for processing.
        </Typography>
        {/* File input for selecting a file */}
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
        {/* Displaying the selected file name and a loading indicator when uploading */}
        {file && (
          <Box sx={{ width: "100%", mb: 2 }}>
            <Typography variant="body2" gutterBottom>
              Selected file: {file.name}
            </Typography>
            {isUploading && <LinearProgress />}
          </Box>
        )}
        {/* Button to initiate file upload */}
        <Button
          variant="outlined"
          onClick={handleFileUpload}
          disabled={!file || isUploading}
        >
          Upload File
        </Button>
        {/* Snackbar for displaying messages */}
        <Snackbar
          anchorOrigin={{ vertical, horizontal }}
          open={snackbarState.open}
          autoHideDuration={3000}
          onClose={closeSnackbar}
          key={vertical + horizontal}
        >
          <Alert onClose={closeSnackbar} severity={snackbarState.severity}>
            {snackbarState.message}
          </Alert>
        </Snackbar>
      </Paper>
    </Container>
  );
}
