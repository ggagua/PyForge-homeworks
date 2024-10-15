import pandas as pd

# Sample DataFrames for demonstration (to be replaced by actual data reading)
wells_data = {
    'well_id': [1, 2, 3, 4],
    'well_row': ['A', 'A', 'B', 'B'],
    'well_column': [1, 2, 1, 2],
    'plate_id': [1, 1, 2, 2],
    'concentration': [10, None, 5, 5],
    'concentration_unit': ['uM', 'uM', 'mM', 'mM'],
    'channel': ['R', 'G', None, 'R']
}

plates_data = {
    'plate_id': [1, 2],
    'experiment_id': [1, 1],
    'property_name': ['concentration', 'channel'],
    'property_value': [5, 'R']
}

experiments_data = {
    'experiment_id': [1],
    'property_name': ['concentration_unit'],
    'property_value': ['uM']
}

# Creating DataFrames from the sample data
wells_df = pd.DataFrame(wells_data)
plates_df = pd.DataFrame(plates_data)
experiments_df = pd.DataFrame(experiments_data)

# Merging wells and plates
merged_df = wells_df.merge(plates_df, how='left', on='plate_id', suffixes=('', '_plate'))

# Merging the result with experiments
merged_df = merged_df.merge(experiments_df, how='left', on='experiment_id', suffixes=('', '_experiment'))

# Debugging: Check merged DataFrame columns
print("Merged DataFrame columns:")
print(merged_df.columns)

result_df = merged_df[['well_id', 'well_row', 'well_column']].copy()

for property_name in wells_df.columns[3:]:  # Assuming the first three columns are well_id, well_row, well_column
    result_df[property_name] = merged_df[property_name]

for property_name in wells_df.columns[3:]:
    plate_property = f"{property_name}_plate"
    experiment_property = f"{property_name}_experiment"

    if plate_property in merged_df.columns:
        result_df[property_name] = result_df[property_name].combine_first(merged_df[plate_property])
    if experiment_property in merged_df.columns:
        result_df[property_name] = result_df[property_name].combine_first(merged_df[experiment_property])

result_df.drop(columns=[col for col in merged_df.columns if col not in result_df.columns], inplace=True,
               errors='ignore')

# Save results to an Excel file
# I am not uploading .xlsc as it was not mentioned but I have no problem in doing so
result_df.to_excel('consolidated_properties.xlsx', index=False)

print("Consolidated properties saved to 'consolidated_properties.xlsx'")


### SQL SCRIPT ###

#-- Assuming we have three tables: wells, plates, and experiments
# CREATE TABLE consolidated_properties AS
# SELECT
#     w.well_id,
#     w.well_row,
#     w.well_column,
#     w.plate_id,
#     COALESCE(w.concentration, p.property_value) AS concentration,
#     COALESCE(w.concentration_unit, e.property_value) AS concentration_unit,
#     COALESCE(w.channel, p.property_value) AS channel,
#     p.experiment_id
# FROM
#     wells w
# LEFT JOIN
#     plates p ON w.plate_id = p.plate_id
# LEFT JOIN
#     experiments e ON p.experiment_id = e.experiment_id;

# -- Query to select data from the consolidated_properties view
# SELECT * FROM consolidated_properties;"

###