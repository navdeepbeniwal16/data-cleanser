const dataTypeMappings = {
  object: "Text",
  int64: "Integer (64-bit)",
  int32: "Integer (32-bit)",
  int16: "Integer (16-bit)",
  int8: "Integer (8-bit)",
  float64: "Floating Point (64-bit)",
  float32: "Floating Point (32-bit)",
  "datetime64[ns]": "Date & Time",
  "timedelta64[ns]": "Time Duration",
  bool: "Boolean (True/False)",
  category: "Categorical",
  complex: "Complex Number",
};

export default dataTypeMappings;
