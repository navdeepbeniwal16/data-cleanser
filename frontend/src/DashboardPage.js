import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Link from "@mui/material/Link";
import DataTable from "./DataTable";
import DTypesConfigurationPane from "./DTypesConfigurationPane";

const defaultTheme = createTheme();

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [receivedData, setReceivedData] = useState(location.state?.data);

  useEffect(() => {
    if (!receivedData) {
      // If there's no data, redirect to the upload page
      navigate("/");
    }
  }, [receivedData, navigate]);

  const onApplyDtypesConfigs = (newDtypesConfigsArr) => {
    const requestData = {
      dtypes: newDtypesConfigsArr,
      invalid_values: "coerce",
      original_data_key: receivedData["original_data_key"],
      cleaned_data_key: receivedData["cleaned_data_key"],
    };

    fetch("http://localhost:8000/data_cleanser/update-columns-dtypes/", {
      method: "POST",
      body: JSON.stringify(requestData),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Network response was not ok.");
      })
      .then((data) => {
        console.log("Dtypes updated successfully:", data);
        // Perform any additional actions with the response data

        // Navigate to Dashboard
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      })
      .finally(() => {
        // TODO: Set received data to updated one
        // setReceivedData()
      });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      {receivedData ? (
        <Box sx={{ display: "flex", width: "100%", height: "100vh" }}>
          <Container
            maxWidth={false}
            sx={{ mt: 4, mb: 4, height: "calc(100% - 32px)" }}
          >
            <Grid container spacing={3} sx={{ height: "100%" }}>
              {/* Chart */}
              <Grid
                item
                xs={12}
                md={8}
                lg={9}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: "100%",
                  }}
                >
                  <DataTable
                    data={receivedData["data"]}
                    dtypes={receivedData["dtypes"]}
                  />
                </Paper>
              </Grid>

              {/* Data types configuration pane */}
              <Grid
                item
                xs={12}
                md={4}
                lg={3}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: "100%",
                    overflow: "auto",
                  }}
                >
                  <DTypesConfigurationPane
                    dtypes={receivedData["dtypes"]}
                    onApply={onApplyDtypesConfigs}
                  />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      ) : (
        <Box />
      )}
    </ThemeProvider>
  );
}
