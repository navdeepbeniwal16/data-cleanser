import * as React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  IconButton,
} from "@mui/material";
import { ArrowBackIos, ArrowForwardIos } from "@mui/icons-material";
import dataTypeMappings from "./dataTypes";
import Box from "@mui/material/Box";

function getDatasetColumnNames(data) {
  return Object.keys(data);
}

export default function DataTable({
  data,
  dtypes,
  currentPage,
  onPrevPage,
  onNextPage,
}) {
  return (
    <React.Fragment>
      <Box sx={{ display: "flex", justifyContent: "space-between", pl: 2 }}>
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
          Cleaned Data
        </Typography>
        <Box
          sx={{
            justifyContent: "space-between",
            pl: 2,
            verticalAlign: "center",
          }}
        >
          <IconButton aria-label="previous page" onClick={onPrevPage}>
            <ArrowBackIos />
          </IconButton>
          {/* Displaying the current page number */}
          {}
          {currentPage}
          {}
          <IconButton aria-label="next page" onClick={onNextPage}>
            <ArrowForwardIos />
          </IconButton>
        </Box>
      </Box>

      <Box sx={{ overflowX: "auto", height: "100%" }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {/* Displaying the columns with their corresponding data types */}
              {Object.entries(dtypes).map(([columnName, type]) => (
                <TableCell key={columnName} sx={{ verticalAlign: "top" }}>
                  <strong>{String(columnName).toUpperCase()}</strong> <br></br>
                  {dataTypeMappings[type]}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {/* Iterating over each row in the dataset */}
            {data.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {getDatasetColumnNames(row).map((colName, colIndex) => (
                  <TableCell key={colIndex}>{String(row[colName])}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
    </React.Fragment>
  );
}
