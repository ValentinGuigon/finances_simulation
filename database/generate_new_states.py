import pandas as pd
from database.get_parameters import get_new_parameters

def create_updated_states_df(starting_parameters, new_states_list):
    # Make a copy of starting parameters to avoid modifying the original
    new_states_parameters = starting_parameters.copy()

    # Iterate over the new states list and update the parameters
    for new_states_dict in new_states_list:
        start_date = pd.to_datetime(new_states_dict['variables_start_date'], format='%m/%d/%Y')
        print(f"Processing new states for start date: {start_date}")

        # Find the index corresponding to the start date
        start_index = (start_date - pd.to_datetime(new_states_parameters['variables_start_date'][0], format='%m/%d/%Y')).days // 30 + 1

        # Extend DataFrame if needed
        if start_index > len(new_states_parameters):
            new_rows = start_index - len(new_states_parameters)
            new_states_parameters = pd.concat([new_states_parameters, pd.DataFrame([{}]*new_rows)], ignore_index=True)

        # Get the existing row
        existing_row = new_states_parameters.iloc[start_index-1]

        # Update specified columns
        for param, value in new_states_dict.items():
            print(f"Checking param: {param}")
            if param in new_states_parameters.columns:
                # Update the existing row with new values
                existing_row[param] = value
            else:
                print(f"{param} not found in columns.")

        # Update the row in the DataFrame
        new_states_parameters.iloc[start_index-1] = existing_row

    return new_states_parameters


def main():
    # Get the starting parameters for the model into a DataFrame
    starting_parameters = pd.read_csv('./database/init_states.csv')

    # Get the new parameters
    new_parameters = get_new_parameters()

    # Generate new states DataFrame from the starting and the new parameters
    new_states_df = create_updated_states_df(starting_parameters, new_parameters_list)

    # Ensure the DataFrame is filled with blank rows up to variables['years']*12
    total_rows_needed = starting_parameters['variables_years'][0] * 12
    if len(new_states_df) < total_rows_needed:
        blank_rows = total_rows_needed - len(new_states_df)
        new_states_df = pd.concat([new_states_df, pd.DataFrame([{}]*blank_rows)], ignore_index=True)

    # Print the DataFrame to check if it contains the expected data
    print(new_states_df)

    # Save the DataFrame to a CSV file
    new_states_df.to_csv('./database/updated_states.csv', index=False)

if __name__ == "__main__":
    main()