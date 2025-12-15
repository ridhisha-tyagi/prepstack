import pandas as pd

def clean_basic(df, guidance=True):
    """
    Basic dataset cleaning:
    - Strip whitespace from column names
    - Drop constant-value columns
    - Drop duplicate rows
    - Reset index to keep things clean

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    guidance : bool
        If True, prints helpful explanations

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe
    """

    df = df.copy()

    # 1) Strip whitespace from column names
    original_cols = df.columns.tolist()
    df.columns = [c.strip() for c in df.columns]
    if guidance:
        print(f"🧹 Stripped whitespace from {len(original_cols)} column names.")

    # 2) Drop constant columns
    constant_cols = [c for c in df.columns if df[c].nunique() <= 1]
    if constant_cols:
        df = df.drop(columns=constant_cols)
        if guidance:
            print(f"🚮 Dropped {len(constant_cols)} constant columns: {constant_cols}")

    # 3) Drop duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    if guidance and dropped > 0:
        print(f"📉 Removed {dropped} duplicate rows.")

    # 4) Reset index
    df = df.reset_index(drop=True)
    if guidance:
        print("✨ Index reset.")
        print("✨ Cleaning complete.")

    return df

