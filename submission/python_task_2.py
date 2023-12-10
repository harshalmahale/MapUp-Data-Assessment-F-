import pandas as pd


def calculate_distance_matrix(df) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    
    distance_matrix = df.pivot_table(index='start_location', columns='end_location', values='distance', aggfunc='sum', fill_value=0)
    
    distance_matrix = distance_matrix + distance_matrix.T - df['distance'].where(df['start_location'] != df['end_location'], 0)

    return distance_matrix


df = pd.read_csv("dataset-3.csv")

result_matrix = calculate_distance_matrix(df)

print(result_matrix)



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    
    unrolled_df = pd.melt(df, id_vars='id_start', value_vars=df.columns[1:], var_name='id_end', value_name='distance')

    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']].reset_index(drop=True)

    return unrolled_df

df_distance_matrix = calculate_distance_matrix(df)
result_unrolled_df = unroll_distance_matrix(df_distance_matrix)
print(result_unrolled_df)


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    reference_df = df[df['id_start'] == reference_id]
    reference_avg_distance = reference_df['distance'].mean()

    threshold_min = reference_avg_distance - (reference_avg_distance * 0.1)
    threshold_max = reference_avg_distance + (reference_avg_distance * 0.1)

    result_df = df.groupby('id_start')['distance'].mean().between(threshold_min, threshold_max).reset_index()
    return df

df_unrolled = unroll_distance_matrix(df_distance_matrix)
reference_id = 123
result_within_threshold = find_ids_within_ten_percentage_threshold(df_unrolled, reference_id)

print(result_within_threshold)




def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'
        df[column_name] = df['distance'] * rate_coefficient

    return df

df_unrolled = unroll_distance_matrix(df_distance_matrix)
result_with_toll_rates = calculate_toll_rate(df_unrolled)
print(result_with_toll_rates)



import datetime

def calculate_time_based_toll_rates(df) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    time_ranges = [
        {'start_time': datetime.time(0, 0, 0), 'end_time': datetime.time(10, 0, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start_time': datetime.time(10, 0, 0), 'end_time': datetime.time(18, 0, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start_time': datetime.time(18, 0, 0), 'end_time': datetime.time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    for time_range in time_ranges:
        mask_weekday = (df['start_time'].dt.time >= time_range['start_time']) & (df['start_time'].dt.time <= time_range['end_time']) & (df['start_time'].dt.weekday < 5)
        mask_weekend = (df['start_time'].dt.time >= time_range['start_time']) & (df['start_time'].dt.time <= time_range['end_time']) & (df['start_time'].dt.weekday >= 5)
        
        df.loc[mask_weekday, df.columns[5:]] *= time_range['weekday_factor']
        df.loc[mask_weekend, df.columns[5:]] *= time_range['weekend_factor']

    df['start_day'] = df['start_time'].dt.strftime('%A')
    df['end_day'] = df['end_time'].dt.strftime('%A')

    return df

df_unrolled = unroll_distance_matrix(df_distance_matrix)

result_with_time_based_toll_rates = calculate_time_based_toll_rates(df_unrolled)

print(result_with_time_based_toll_rates)

