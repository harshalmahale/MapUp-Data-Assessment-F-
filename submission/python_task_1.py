import pandas as pd

def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    car_matrix = car_matrix.fillna(0)

    car_matrix.values[[range(len(car_matrix))]*2] = 0

    # Convert the resulting matrix to a DataFrame
    result_df = pd.DataFrame(car_matrix, index=car_matrix.index, columns=car_matrix.columns)

    return result_df

# Example usage
df = pd.read_csv("dataset-1.csv")
result_df = generate_car_matrix(df)
print(result_df)



import pandas as pd

def get_type_count(df):
    """
    Categorizes 'car' values into types, creates a 'car_type' column, 
    and returns a dictionary of counts. Also, returns a DataFrame with a one-hot vector for car_type.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
        pandas.DataFrame: DataFrame with a one-hot vector for car_type.
    """
    # Create a new column 'car_type' based on the given rules
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Calculate counts for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

    # Create a one-hot vector for the 'car_type' column
    one_hot_df = pd.get_dummies(df['car_type'], prefix='car_type')

    return one_hot_df

# Example usage
df = pd.read_csv("dataset-1.csv")
result_one_hot_df = get_type_count(df)

print("\nDataFrame with one-hot vector for car_type:")
print(result_one_hot_df)


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    sorted_bus_indexes = sorted(bus_indexes)

    return sorted_bus_indexes


df = pd.read_csv("dataset-1.csv")

result_i = get_bus_indexes(df)
print(result_i)


import pandas as pd

def filter_routes(df):
    """
    Returns the sorted list of values in the 'route' column 
    for which the average of 'truck' column values is greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: Sorted list of 'route' column values that meet the condition.
    """
    # Calculate the average of 'truck' column values for each 'route'
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column values is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Example usage
df = pd.read_csv("dataset-1.csv")
result_routes = filter_routes(df)

print("Sorted list of 'route' values with average 'truck' values greater than 7:", result_routes)



def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


result_matrix = generate_car_matrix(df)

modified_result_matrix = multiply_matrix(result_matrix)
print(modified_result_matrix)



def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

   
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    
    completeness_check = (
        (df['end_timestamp'] - df['start_timestamp'] == pd.Timedelta(days=1)) &  # Full 24-hour period
        (df['start_timestamp'].dt.dayofweek == 0) &  # Monday
        (df['end_timestamp'].dt.dayofweek == 6)      # Sunday
    )

    
    result_series = completeness_check.groupby(['id', 'id_2']).all()

    return result_series


df = pd.read_csv("dataset-2.csv")


result_series = time_check(df)

print(result_series)