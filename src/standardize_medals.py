def standardize_medal_types(df):
    """
    Standardize the format of medal names in the dataframe to ensure consistency
    -> 'GOLD', 'gold', will be converted to: 'Gold' 

    Parameters:
    df (pd.DataFrame): DataFrame containing the medal data.

    Returns:
    pd.DataFrame: DataFrame with standardized medal name
    """
    if 'medal_type' in df.columns:
        df['medal_type'] = df['medal_type'].str.capitalize()
    if 'Medal' in df.columns:
        df['Medal'] = df['Medal'].str.capitalize()
    return df