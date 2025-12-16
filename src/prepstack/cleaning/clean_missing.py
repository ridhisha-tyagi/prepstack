import pandas as pd
import numpy as np

def missing_summary(df, guidance=True):
    """Returns a summary of missing values."""
    summary = df.isnull().sum()
    summary = summary[summary > 0].sort_values(ascending=False)

    if guidance:
        print(f"🔍 Found {len(summary)} columns with missing values.")
        for col, count in summary.items():
            print(f"   • {col}: {count} missing")

    return summary


def fill_numeric(df, strategy="median", value=None, guidance=True):
    """
    Fill numeric missing values.
    strategy = 'mean' | 'median' | 'constant'
    """
    df = df.copy()
    nums = df.select_dtypes(include=[np.number])

    if strategy in ["mean", "median"]:
        for col in nums.columns:
            fill_val = nums[col].mean() if strategy == "mean" else nums[col].median()
            df[col].fillna(fill_val, inplace=True)
            if guidance:
                print(f"🧮 Filled {col} using {strategy} ({fill_val:.2f})")

    elif strategy == "constant":
        if value is None:
            raise ValueError("value must be provided for constant strategy")
        df[nums.columns] = df[nums.columns].fillna(value)
        if guidance:
            print(f"🔢 Filled all numeric columns with constant = {value}")

    return df


def fill_categorical(df, strategy="mode", value=None, guidance=True):
    """
    Fill categorical missing values.
    strategy = 'mode' | 'constant'
    """
    df = df.copy()
    cats = df.select_dtypes(include=["object"])

    if strategy == "mode":
        for col in cats.columns:
            fill_val = cats[col].mode()[0]
            df[col].fillna(fill_val, inplace=True)
            if guidance:
                print(f"📝 Filled {col} with mode ('{fill_val}')")

    elif strategy == "constant":
        if value is None:
            raise ValueError("value must be provided for constant strategy")
        df[cats.columns] = df[cats.columns].fillna(value)
        if guidance:
            print(f"🔤 Filled all categorical columns with constant = '{value}'")

    return df


def drop_missing(df, threshold=0.5, guidance=True):
    """
    Drops columns where missing ratio > threshold.
    threshold = 0.5 → drop if more than 50% missing
    """
    df = df.copy()
    to_drop = [col for col in df.columns if df[col].isnull().mean() > threshold]

    df = df.drop(columns=to_drop)

    if guidance:
        print(f"🗑️ Dropped {len(to_drop)} columns with > {threshold*100:.0f}% missing.")
        if len(to_drop):
            print("   →", to_drop)

    return df
