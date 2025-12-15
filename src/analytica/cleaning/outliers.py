from typing import Optional, Sequence
import pandas as pd
import numpy as np
from analytica.helpers import say, GuidanceMode


def cap_outliers_iqr(
    df: pd.DataFrame,
    *,
    columns: Optional[Sequence[str]] = None,
    factor: float = 1.5,
    guidance: GuidanceMode = "on",
) -> pd.DataFrame:
    """
    Cap outliers using the IQR method.

    For each numeric column:
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        values below lower are set to lower
        values above upper are set to upper
    """
    df_cap = df.copy()
    num_cols = columns if columns is not None else df_cap.select_dtypes(include="number").columns.tolist()

    if not num_cols:
        say("ℹ️ No numeric columns found for outlier capping.", guidance)
        return df_cap

    say(f"📉 Capping outliers using IQR factor={factor} for columns: {list(num_cols)}", guidance)

    for col in num_cols:
        series = df_cap[col]
        if series.nunique(dropna=True) <= 1:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - factor * iqr
        upper = q3 + factor * iqr

        before = series.copy()
        df_cap[col] = series.clip(lower, upper)
        changed = (before != df_cap[col]).sum()

        if changed > 0:
            say(f"  • Column '{col}': capped {changed} value(s) outside [{lower:.3f}, {upper:.3f}].", guidance)

    say("✅ Outlier capping complete.", guidance)
    return df_cap
