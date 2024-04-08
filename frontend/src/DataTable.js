import * as React from "react";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Typography } from "@mui/material";
import dataTypeMappings from "./dataTypes";
import Box from "@mui/material/Box";

function getDatasetColumnNames(data) {
  console.log("getDatasetColumnNames: Data:", data);
  return Object.keys(data);
}

export default function DataTable({ data, dtypes }) {
  return (
    <React.Fragment>
      <Typography
        component="h2"
        variant="h6"
        color="primary"
        gutterBottom
        align="left"
        sx={{ pl: 2 }}
      >
        Cleaned Data
      </Typography>
      <Box sx={{ overflowX: "auto" }}>
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
