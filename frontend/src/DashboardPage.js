import React, { useEffect, useState } from "react";
import { useNavigate, useLocation, Link as RouterLink } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import {
  CssBaseline,
  Box,
  Container,
  Grid,
  Paper,
  Link,
  Breadcrumbs,
  Snackbar,
  Alert,
} from "@mui/material";
import DataTable from "./DataTable";
import DTypesConfigurationPane from "./DTypesConfigurationPane";

const defaultTheme = createTheme();
let currentPageNumber = 1;

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [snackbarState, setSnackbarState] = React.useState({
    open: false,
    vertical: "top",
    horizontal: "center",
    requestSuccess: "success",
    message: "",
  });
  const { vertical, horizontal, open, requestSuccess, message } = snackbarState;

  const openSnackbar = (newState) => () => {
    setSnackbarState({ ...newState, open: true });
  };

  const closeSnackbar = () => {
    setSnackbarState({ ...snackbarState, open: false });
  };
  const [receivedData, setReceivedData] = useState(location.state?.data);

  useEffect(() => {
    if (!receivedData) {
      // Redirect to the upload page if no receivedData is found
      navigate("/");
    }
  }, [receivedData, navigate]);

  const getPreviousPage = () => {
    if (currentPageNumber > 1) {
      getPage(currentPageNumber - 1);
    }
  };

  const getNextPage = () => {
    getPage(currentPageNumber + 1);
  };

  const getPage = (pageNumber) => {
    fetch(
      "http://localhost:8000/data_cleanser/data/" +
        receivedData["cleaned_data_key"] +
        "?page=" +
        pageNumber,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Error occured while serving the request.");
      })
      .then((data) => {
        currentPageNumber = pageNumber;
        const dataToReplaceWith = { ...receivedData, data: data["data"] };
        setReceivedData(dataToReplaceWith);
      })
      .catch((error) => {
        console.error("Error occured while fetching data from backend:", error);
        // Showing an error alert/snackbar
        openSnackbar({
          vertical: "bottom",
          horizontal: "center",
          requestSuccess: "error",
          message: "Reached the end of the dataset.",
        })();
      });
  };

  const onApplyDtypesConfigs = (newDtypesConfigsArr) => {
    const requestData = {
      dtypes: newDtypesConfigsArr,
      invalid_values: "coerce",
      original_data_key: receivedData["original_data_key"],
      cleaned_data_key: receivedData["cleaned_data_key"],
    };

    fetch(
      "http://localhost:8000/data_cleanser/update-columns-dtypes/?page=" +
        currentPageNumber,
      {
        method: "POST",
        body: JSON.stringify(requestData),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Error occured while serving the request.");
      })
      .then((data) => {
        // Showing a success alert/snackbar
        openSnackbar({
          vertical: "bottom",
          horizontal: "center",
          requestSuccess: "success",
          message: "Data types have been successfully updated.",
        })();
        setReceivedData(data);
      })
      .catch((error) => {
        console.error("Error occured while fetching data from backend:", error);
        openSnackbar({
          vertical: "bottom",
          horizontal: "center",
          requestSuccess: "error",
          message:
            "Sorry, we were unable to update the data types. Please try again.",
        })();
      });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      {receivedData ? (
        <Box
          sx={{
            display: "flex",
            width: "100%",
            height: "100vh",
          }}
        >
          <Container
            maxWidth={false}
            sx={{ mt: 4, mb: 4, height: "calc(100% - 32px)" }}
          >
            <Breadcrumbs
              aria-label="breadcrumb"
              sx={{ mt: 2, mb: 2, ml: 2, mr: 2 }}
            >
              <Link
                component={RouterLink}
                underline="hover"
                color="inherit"
                to="/"
              >
                Home
              </Link>
              <Link
                component={RouterLink}
                underline="hover"
                color="inherit"
                to="/dashboard"
              >
                Dashboard
              </Link>
            </Breadcrumbs>
            <br></br>

            <Grid container spacing={3} sx={{ height: "80%" }}>
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
                    currentPage={currentPageNumber}
                    onPrevPage={getPreviousPage}
                    onNextPage={getNextPage}
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
              <Box sx={{ width: 500 }}>
                <Snackbar
                  anchorOrigin={{ vertical, horizontal }}
                  open={open}
                  onClose={closeSnackbar}
                  key={vertical + horizontal}
                  autoHideDuration={3000}
                >
                  <Alert
                    onClose={closeSnackbar}
                    severity={requestSuccess}
                    variant="filled"
                    sx={{ width: "100%" }}
                  >
                    {message}
                  </Alert>
                </Snackbar>
              </Box>
            </Grid>
          </Container>
        </Box>
      ) : (
        <Box />
      )}
    </ThemeProvider>
  );
}
