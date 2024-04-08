import pandas as pd

# Original data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hannah', 'Ian', 'Jill'],
    'Birthdate': ['1/01/1990', '2/02/1991', '3/03/1992', '4/04/1993', '5/05/1994', '6/06/1995', '7/07/1996', '8/08/1997', '9/09/1998', '10/10/1999'],
    'Score': [90, 75, 85, 70, 65, 80, 95, 60, 85, 70],
    'Grade': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
    'Height': [165.5, 170.2, 180.1, 175.3, 160.4, 182.5, 167.6, 172.7, 185.8, 178.9],
    'Weight': [55.2, 60.3, 70.4, 65.5, 50.6, 72.7, 57.8, 62.9, 75.0, 67.1],
    'Is Student': [True, False, True, False, True, False, True, False, True, False],
    'Stream': ['Science', 'Arts', 'Engineering', 'Mathematics', 'History', 'Literature', 'Physics', 'Chemistry', 'Biology', 'Geography'],
    'Complex Number': ['3+4j', '5+6j', '7+8j', '9+10j', '11+12j', '13+14j', '15+16j', '17+18j', '19+20j', '21+22j'],
    'Time Since Exam': ['5 days', '10 days', '15 days', '20 days', '25 days', '30 days', '35 days', '40 days', '45 days', '50 days']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Duplicate the data to reach 1 million rows
df_large = pd.concat([df] * 100000, ignore_index=True)

# Save to CSV
df_large.to_csv('sample_data_large.csv', index=False)

print("CSV file with 1 million rows created successfully.")
