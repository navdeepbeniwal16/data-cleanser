import * as React from "react";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Typography } from "@mui/material";

let dataRowsCount = 0;

function getDatasetColumnNames(data) {
  console.log("getDatasetColumnNames: Data:", data);
  return Object.keys(data);
}

const getListRowsData = (data) => {
  // Get an array of column names from the data property
  const columns = getDatasetColumnNames(data);

  // Find out the number of rows by checking the length of the array of the first property
  const numRows = data[columns[0]].length;
  const rows = [];

  // Create an array of row objects
  for (let i = 0; i < numRows; i++) {
    let row = {
      id: dataRowsCount,
    };
    columns.forEach((column) => {
      row[column] = data[column][i];
    });
    rows.push(row);
    dataRowsCount++;
  }

  return rows;
};

function preventDefault(event) {
  event.preventDefault();
}

export default function DataTable({ data, dtypes }) {
  return (
    <React.Fragment>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Data
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            {Object.entries(dtypes).map(([columnName, type]) => (
              <TableCell key={columnName}>
                {columnName} ({type})
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {getListRowsData(data).map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {getDatasetColumnNames(data).map((colName, colIndex) => (
                <TableCell key={colIndex}>{String(row[colName])}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
        Load more data
      </Link>
    </React.Fragment>
  );
}
