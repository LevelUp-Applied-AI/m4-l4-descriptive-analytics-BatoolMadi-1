"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from eda_report import generate_eda_report


def load_and_profile(filepath):
    """Load the dataset and generate a data profile report."""
    df = pd.read_csv(filepath)

    shape = df.shape
    data_types = df.dtypes
    missing = df.isnull().sum()
    desc = df.describe()

    with open("output/data_profile.txt", "w") as f:
        f.write("DATA PROFILE\n\n")

        f.write(f"Shape: {shape}\n\n")

        f.write("Data Types:\n")
        f.write(str(data_types))
        f.write("\n\n")

        f.write("Missing Values:\n")
        f.write(str(missing))
        f.write("\n\n")

        f.write("Descriptive Statistics:\n")
        f.write(str(desc))

        f.write("\n\nCleaning Decisions:\n")
        f.write("- Commute_minutes: Missing values imputed with median (~10%, assumed MCAR).\n")
        f.write("- Study_hours_weekly: Rows dropped (~5% missing, minimal impact).\n")

        # *************************** Cleaning ***************************
        # commute_minutes → median imputation (~10%)

        df["commute_minutes"].fillna(
            df["commute_minutes"].median(),
            inplace=True
        ) 
        # study_hours_weekly → drop (~5%)
        df = df.dropna(subset=["study_hours_weekly"])

    return df

    # TODO: Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt


def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """

    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct",]

    for col in numeric_cols:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.savefig(f"output/{col}_distribution.png")
        plt.close()

    # GPA by department
    plt.figure(figsize=(10,8))
    sns.boxplot(x="department", y="gpa", data=df)
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.title("GPA by Department")
    plt.tight_layout()
    plt.savefig("output/GPA_by_department.png")
    plt.close()

    # scholarship counts
    plt.figure()
    df["scholarship"].value_counts().plot(kind="bar")
    plt.title("Scholarship Distribution")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("output/scholarship_distribution.png")
    plt.close()

    # *************************** Violin Plot ***************************

    plt.figure(figsize=(10,6))

    sns.violinplot(
        x="department",
        y="gpa",
        data=df
    )

    plt.title("GPA Distribution by Department (Violin Plot)")
    plt.tight_layout()

    plt.savefig("output/gpa_violinplot.png")
    plt.close()

    # TODO: Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # TODO: Use histograms with KDE overlay (sns.histplot) or box plots
    # TODO: Save each plot to the output/ directory



def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """

    numeric_df = df.select_dtypes(include=[np.number])

    corr = numeric_df.corr(method="pearson")

    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig("output/correlation_heatmap.png")
    plt.close()

    # scatter: study hours vs GPA
    plt.figure()
    sns.scatterplot(
        x=df["study_hours_weekly"],
        y=df["gpa"]
    )
    plt.title("Study Hours vs GPA")
    plt.tight_layout()
    plt.savefig("output/study_hours_vs_GPA.png")
    plt.close()

    plt.figure()
    sns.scatterplot(
        x=df["attendance_pct"],
        y=df["gpa"]
    )
    plt.title("Attendance vs GPA")
    plt.tight_layout()
    plt.savefig("output/attendance_vs_GPA.png")
    plt.close()

    # TODO: Compute the correlation matrix for numeric columns
    # TODO: Create a heatmap or scatter plots showing key relationships
    # TODO: Save the visualization(s) to the output/ directory



def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """

    results = {}

    # *************************** T-test ***************************

    with_int = df[df["has_internship"] == "Yes"]["gpa"]
    without_int = df[df["has_internship"] == "No"]["gpa"]

    t_stat, p_val = stats.ttest_ind(with_int, without_int)

    print("\nT-test: Internship vs GPA")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_val:.4f}")

    results["internship_ttest"] = (t_stat, p_val)

    # -------- Cohen's d (Effect Size) --------

    mean_diff = with_int.mean() - without_int.mean()
    pooled_sd = np.sqrt(
        ((with_int.std() ** 2) + (without_int.std() ** 2)) / 2
    )
    cohens_d = mean_diff / pooled_sd
    
    print(f"Cohen's d: {cohens_d:.4f}")

    results["internship_effect_size"] = cohens_d


    # *************************** ANOVA ***************************

    groups = [
        group["gpa"].values
        for _, group in df.groupby("department")
    ]

    f_stat, p_val_nova = stats.f_oneway(*groups)

    print("\nANOVA: GPA across Departments")
    print(f"F-statistic: {f_stat:.4f}")
    print(f"P-value: {p_val_nova:.4f}")

    results["dept_anova"] = (f_stat, p_val_nova)


    # *************************** Correlation Test ***************************
    
    corr_coef, p_cprr = stats.pearsonr(
        df["study_hours_weekly"],
        df["gpa"]
    )

    print("\nCorrelation Test: Study Hours vs GPA")
    print(f"Correlation Coefficient: {corr_coef:.4f}")
    print(f"P-value: {p_cprr:.4f}")

    results["study_gpa_corr"] = (corr_coef, p_cprr)

    # *************************** Chi-Square Test ***************************

    cont_table = pd.crosstab(df["scholarship"], df["department"])

    chi2, p_chi, dof, expected = stats.chi2_contingency(cont_table)

    print("\nChi-Square Test: Scholarship vs Department")
    print(f"Chi-square statistic: {chi2:.4f}")
    print(f"P-value: {p_chi:.4f}")
    print(f"Degrees of freedom: {dof}")

    results["scholarship_chi2"] = (chi2, p_chi, dof)

    return results

    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)

    df = load_and_profile("data/student_performance.csv")
    
    plot_distributions(df)
    plot_correlations(df)

    results = run_hypothesis_tests(df)

    print("\nEDA Complete. Findings have been saved to the output/ .")

    # TODO: Load and profile the dataset
    # TODO: Generate distribution plots
    # TODO: Analyze correlations
    # TODO: Run hypothesis tests
    # TODO: Write a FINDINGS.md summarizing your analysis

    generate_eda_report(df)


if __name__ == "__main__":
    main()
