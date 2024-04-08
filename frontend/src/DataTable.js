import * as React from "react";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Typography, IconButton } from "@mui/material";
import { ArrowBackIos, ArrowForwardIos } from "@mui/icons-material";
import dataTypeMappings from "./dataTypes";
import Box from "@mui/material/Box";

function getDatasetColumnNames(data) {
  console.log("getDatasetColumnNames: Data:", data);
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
              {Object.entries(dtypes).map(([columnName, type]) => (
                <TableCell key={columnName}>
                  <strong>{columnName}</strong> <br></br>
                  {dataTypeMappings[type]}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
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
