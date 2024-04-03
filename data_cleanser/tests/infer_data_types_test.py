import pandas as pd
import numpy as np
from data_cleanser.inference import infer_data_types, InferedDataType

def test_infer_data_types():
    # Sample DataFrame using data from sample_data.csv
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Birthdate': ['1/01/1990', '2/02/1991', '3/03/1992', '4/04/1993', '5/05/1994'],
        'Score': [90, 75, 85, 70, 'Not Available'],
        'Grade': ['A', 'B', 'A', 'B', 'A']
    }
    data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Birthdate': ['1/01/1990', '2/02/1991', '3/03/1992', '4/04/1993', '5/05/1994'],
    'Score': [90, 75, 85, 70, 'Not Available'],
    'Grade': ['A', 'B', 'A', 'B', 'A'],
    'Is_Citizen': [True, False, True, False, True],
    'Blood_Group': ['A', 'B', 'B', 'B', 'A'],
    'Complex': ['1 + 2j', '3 + 4j', '5 + 6j', '7 + 8j', '9 + 10j'],
    'Object': [object(), object(), object(), object(), object()],
}
    df = pd.DataFrame(data)

    # Call infer_data_types on the sample DataFrame
    inferred_types = infer_data_types(df)

    # Assert the inferred types for each column
    assert inferred_types['Name'] == InferedDataType.OBJECT
    assert inferred_types['Birthdate'] == InferedDataType.DATETIME64
    assert inferred_types['Score'] == InferedDataType.INT8
    assert inferred_types['Grade'] == InferedDataType.CATEGORY
    assert inferred_types['Is_Citizen'] == InferedDataType.BOOLEAN
    assert inferred_types['Blood_Group'] == InferedDataType.CATEGORY
    assert inferred_types['Complex'] == InferedDataType.COMPLEX
    assert inferred_types['Object'] == InferedDataType.OBJECT