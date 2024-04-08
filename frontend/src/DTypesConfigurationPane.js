import React, { useState } from "react";
import {
  Box,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import dataTypeMappings from "./dataTypes";

const dataTypes = [
  "object",
  "int64",
  "int32",
  "int16",
  "int8",
  "float64",
  "float32",
  "datetime64[ns]",
  "timedelta64[ns]",
  "bool",
  "category",
  "complex",
];

const missingValueOptions = ["ignore", "default", "delete"];

export default function DTypesConfigurationPane({ dtypes, onApply }) {
  const [selectedTypes, setSelectedTypes] = useState(dtypes);
  const [missingValues, setMissingValues] = useState(() =>
    Object.keys(dtypes).reduce((acc, key) => ({ ...acc, [key]: "ignore" }), {})
  );
  const [defaultValues, setDefaultValues] = useState({});

  const handleTypeChange = (column, type) => {
    setSelectedTypes({ ...selectedTypes, [column]: type });
  };

  const handleMissingValueChange = (column, option) => {
    setMissingValues({ ...missingValues, [column]: option });
  };

  const handleDefaultValueChange = (column, value) => {
    setDefaultValues({ ...defaultValues, [column]: value });
  };

  const handleSubmit = () => {
    // Construct the payload with the changes
    const changes = Object.keys(dtypes).reduce((acc, column) => {
      if (dtypes[column] !== selectedTypes[column]) {
        acc.push({
          col_name: column,
          dtype: selectedTypes[column],
          missing_values: missingValues[column],
          default:
            missingValues[column] === "default" ? defaultValues[column] : null,
        });
      }
      return acc;
    }, []);

    onApply(changes);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Typography
        component="h2"
        variant="h6"
        color="primary"
        gutterBottom
        align="left"
        sx={{ pl: 2 }}
      >
        Column Type Configuration
      </Typography>

      {Object.entries(dtypes).map(([column, type]) => (
        <Accordion key={column}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>{column}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>Current type: {dataTypeMappings[type]}</Typography>
            <FormControl fullWidth margin="normal">
              <InputLabel>New type</InputLabel>
              <Select
                value={selectedTypes[column]}
                label="New type"
                onChange={(e) => handleTypeChange(column, e.target.value)}
              >
                {dataTypes.map((dataType) => (
                  <MenuItem key={dataType} value={dataType}>
                    {dataTypeMappings[dataType]}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>Missing values</InputLabel>
              <Select
                value={missingValues[column] || "ignore"}
                label="Missing values"
                onChange={(e) =>
                  handleMissingValueChange(column, e.target.value)
                }
              >
                {missingValueOptions.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              margin="normal"
              label="Default value"
              disabled={missingValues[column] !== "default"}
              value={defaultValues[column] || ""}
              onChange={(e) => handleDefaultValueChange(column, e.target.value)}
            />
          </AccordionDetails>
        </Accordion>
      ))}
      <Button variant="contained" onClick={handleSubmit} sx={{ mt: 2 }}>
        Apply
      </Button>
    </Box>
  );
}
