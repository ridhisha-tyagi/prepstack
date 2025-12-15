from typing import Optional, Sequence, Dict
import pandas as pd
from analytica.helpers import say, GuidanceMode


def cast_columns(
    df: pd.DataFrame,
    *,
    to_int: Optional[Sequence[str]] = None,
    to_float: Optional[Sequence[str]] = None,
    to_category: Optional[Sequence[str]] = None,
    to_datetime: Optional[Dict[str, str]] = None,
    guidance: GuidanceMode = "on",
) -> pd.DataFrame:
    """
    Cast groups of columns to specific dtypes.

    Parameters
    ----------
    to_int : list of column names to convert to int (errors='coerce')
    to_float : list of column names to convert to float (errors='coerce')
    to_category : list of columns to convert to category
    to_datetime : dict {column_name: format_string or None}
        Example: {'signup_date': '%Y-%m-%d', 'churn_date': None}
    """
    df_cast = df.copy()

    if to_int:
        for col in to_int:
            if col in df_cast.columns:
                df_cast[col] = pd.to_numeric(df_cast[col], errors="coerce").astype("Int64")
                say(f"🔁 Cast '{col}' → Int64 (nullable).", guidance)

    if to_float:
        for col in to_float:
            if col in df_cast.columns:
                df_cast[col] = pd.to_numeric(df_cast[col], errors="coerce").astype(float)
                say(f"🔁 Cast '{col}' → float.", guidance)

    if to_category:
        for col in to_category:
            if col in df_cast.columns:
                df_cast[col] = df_cast[col].astype("category")
                say(f"🔁 Cast '{col}' → category.", guidance)

    if to_datetime:
        for col, fmt in to_datetime.items():
            if col in df_cast.columns:
                df_cast[col] = pd.to_datetime(df_cast[col], format=fmt, errors="coerce")
                say(f"🔁 Cast '{col}' → datetime (format={fmt}).", guidance)

    say("✨ Type casting complete.", guidance)
    return df_cast
