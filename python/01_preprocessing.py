# =============================================================================
#  Student Performance Analysis
#  Task 1: Data Preprocessing & Cleaning
#  File   : 01_preprocessing.py
#  Run    : VS Code Run Button (top right)
# =============================================================================

import pandas as pd
import numpy as np
import os

# ── PATHS (auto-resolved regardless of where you run the script from) ────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data") + os.sep
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs", "reports") + os.sep

RAW_MATH    = DATA_DIR + "student-mat.csv"
RAW_POR     = DATA_DIR + "student-por.csv"
CLEAN_MATH  = DATA_DIR + "student-mat-clean.csv"
CLEAN_POR   = DATA_DIR + "student-por-clean.csv"

# =============================================================================
#  STEP 1 — LOAD DATASET
# =============================================================================
print("=" * 60)
print("STEP 1 — LOADING DATASET")
print("=" * 60)

# NOTE: This dataset uses semicolon (;) as separator
# Auto-detect separator (handles both comma and semicolon CSVs)
math_df = pd.read_csv(RAW_MATH, sep=None, engine='python')
por_df  = pd.read_csv(RAW_POR,  sep=None, engine='python')

print(f"Math dataset loaded  : {math_df.shape[0]} rows × {math_df.shape[1]} cols")
print(f"Por  dataset loaded  : {por_df.shape[0]} rows × {por_df.shape[1]} cols")

# =============================================================================
#  STEP 2 — CHECK DATA TYPES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 2 — DATA TYPES")
print("=" * 60)

print("\n── Math Dataset dtypes ──")
print(math_df.dtypes.to_string())

# =============================================================================
#  STEP 3 — CHECK MISSING VALUES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 3 — MISSING VALUES CHECK")
print("=" * 60)

math_nulls = math_df.isnull().sum()
por_nulls  = por_df.isnull().sum()

print("\n── Missing Values (Math) ──")
print(math_nulls[math_nulls > 0] if math_nulls.sum() > 0 else "No missing values found.")

print("\n── Missing Values (Por) ──")
print(por_nulls[por_nulls > 0] if por_nulls.sum() > 0 else "No missing values found.")

print(f"\nRows with ANY null (math) : {math_df.isnull().any(axis=1).sum()}")
print(f"Rows with ANY null (por)  : {por_df.isnull().any(axis=1).sum()}")

# =============================================================================
#  STEP 4 — HANDLE MISSING VALUES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 4 — HANDLE MISSING VALUES")
print("=" * 60)

for df, name in [(math_df, "math"), (por_df, "por")]:
    # Numeric → fill with median
    for col in df.select_dtypes(include="number").columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
            print(f"  [{name}] '{col}' numeric nulls filled with median")

    # Categorical → fill with mode
    for col in df.select_dtypes(include=["object", "str"]).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
            print(f"  [{name}] '{col}' categorical nulls filled with mode")

print("Missing value handling complete.")

# =============================================================================
#  STEP 5 — ENCODE CATEGORICAL VARIABLES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 5 — ENCODE CATEGORICAL VARIABLES")
print("=" * 60)

# Binary yes/no → 1/0
binary_cols = [
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic"
]
for col in binary_cols:
    math_df[col] = math_df[col].map({"yes": 1, "no": 0})
    por_df[col]  = por_df[col].map({"yes": 1, "no": 0})
print("  Binary columns encoded  : yes=1 / no=0")

# sex → F=0, M=1
math_df["sex"] = math_df["sex"].map({"F": 0, "M": 1})
por_df["sex"]  = por_df["sex"].map({"F": 0, "M": 1})
print("  sex encoded             : F=0 / M=1")

# address → R=0, U=1
math_df["address"] = math_df["address"].map({"R": 0, "U": 1})
por_df["address"]  = por_df["address"].map({"R": 0, "U": 1})
print("  address encoded         : R=0 / U=1")

# famsize → LE3=0, GT3=1
math_df["famsize"] = math_df["famsize"].map({"LE3": 0, "GT3": 1})
por_df["famsize"]  = por_df["famsize"].map({"LE3": 0, "GT3": 1})
print("  famsize encoded         : LE3=0 / GT3=1")

# Pstatus → A=0, T=1
math_df["Pstatus"] = math_df["Pstatus"].map({"A": 0, "T": 1})
por_df["Pstatus"]  = por_df["Pstatus"].map({"A": 0, "T": 1})
print("  Pstatus encoded         : A=0 / T=1")

# Multi-class → one-hot encoding
multi_cols = ["Mjob", "Fjob", "reason", "guardian", "school"]
math_df = pd.get_dummies(math_df, columns=multi_cols, drop_first=True)
por_df  = pd.get_dummies(por_df,  columns=multi_cols, drop_first=True)
print(f"  One-hot encoded         : {multi_cols}")
print(f"\n  New shape (math) : {math_df.shape}")
print(f"  New shape (por)  : {por_df.shape}")

# =============================================================================
#  STEP 6 — VALIDATE DATA RANGES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 6 — VALIDATE DATA RANGES")
print("=" * 60)

try:
    assert math_df["G3"].between(0, 20).all(),       "G3 out of range [0-20]!"
    assert math_df["G1"].between(0, 20).all(),       "G1 out of range [0-20]!"
    assert math_df["G2"].between(0, 20).all(),       "G2 out of range [0-20]!"
    assert math_df["studytime"].between(1, 4).all(), "studytime out of range [1-4]!"
    assert math_df["Medu"].between(0, 4).all(),      "Medu out of range [0-4]!"
    assert math_df["Fedu"].between(0, 4).all(),      "Fedu out of range [0-4]!"
    assert math_df["failures"].between(0, 4).all(),  "failures out of range [0-4]!"
    print("  All range validations passed.")
except AssertionError as e:
    print(f"  Validation WARNING: {e}")

# =============================================================================
#  STEP 7 — IQR OUTLIER REMOVAL (ALL NUMERIC COLUMNS)
# =============================================================================
print("\n" + "=" * 60)
print("STEP 7 — IQR OUTLIER REMOVAL")
print("=" * 60)

def remove_outliers_iqr(df, label="dataset"):
    """
    Removes rows where any numeric column falls outside
    Q1 - 1.5*IQR  or  Q3 + 1.5*IQR  (Tukey's fences).
    """
    df_clean = df.copy()
    num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    report   = []

    for col in num_cols:
        Q1  = df_clean[col].quantile(0.25)
        Q3  = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lo  = Q1 - 1.5 * IQR
        hi  = Q3 + 1.5 * IQR

        mask  = (df_clean[col] < lo) | (df_clean[col] > hi)
        count = int(mask.sum())

        if count > 0:
            report.append({
                "column"        : col,
                "lower_fence"   : round(lo, 2),
                "upper_fence"   : round(hi, 2),
                "outliers_found": count
            })
        df_clean = df_clean[~mask]

    print(f"\n── IQR Outlier Report ({label}) ──")
    if report:
        rdf = pd.DataFrame(report)
        print(rdf.to_string(index=False))
    else:
        print("  No outliers detected in any column.")

    print(f"\n  Rows before  : {len(df)}")
    print(f"  Rows after   : {len(df_clean)}")
    print(f"  Rows dropped : {len(df) - len(df_clean)}")
    return df_clean


math_df = remove_outliers_iqr(math_df, "Math")
por_df  = remove_outliers_iqr(por_df,  "Portuguese")

# =============================================================================
#  STEP 8 — SAVE CLEANED DATA
# =============================================================================
print("\n" + "=" * 60)
print("STEP 8 — SAVE CLEANED DATA")
print("=" * 60)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save to data/ (used by all other task scripts)
math_df.to_csv(CLEAN_MATH, index=False)
por_df.to_csv(CLEAN_POR,   index=False)

# Save summary report to outputs/reports/
math_df.describe().to_csv(OUTPUT_DIR + "math_summary_stats.csv")

print(f"  Saved → {CLEAN_MATH}")
print(f"  Saved → {CLEAN_POR}")
print(f"  Saved → {OUTPUT_DIR}math_summary_stats.csv")

# =============================================================================
#  FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE — FINAL SUMMARY")
print("=" * 60)
print(f"  Math cleaned shape  : {math_df.shape}")
print(f"  Por  cleaned shape  : {por_df.shape}")
print(f"\n  Sample (Math — first 3 rows):")
print(math_df[["sex","age","studytime","failures","absences",
               "Medu","Fedu","G1","G2","G3"]].head(3).to_string(index=False))
print("\n  Task 1 DONE. Ready for 02_studytime_analysis.py")
print("=" * 60)