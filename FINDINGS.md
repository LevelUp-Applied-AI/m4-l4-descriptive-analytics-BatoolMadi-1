# Student Performance EDA — Findings

---

## 1. Dataset Description

The dataset contains student academic performance information including GPA,
study habits, attendance, department affiliation, internships, and scholarships.

**Dataset shape:** 2000 rows × 10 columns.

**Main columns include:**

* Academic metrics: GPA, attendance percentage, course load
* Behavioral factors: study hours weekly, commute time
* Categorical attributes: department, semester, internship status, scholarship status

### Data Quality Issues

Data profiling identified missing values in two variables:

* `commute_minutes`: 181 missing values (~9%), handled using **median imputation**.
* `scholarship`: 389 missing values (~19%), retained as-is for categorical analysis.
* `study_hours_weekly`: missing rows were removed due to small proportion and minimal analytical impact.

(See `output/data_profile.txt` for full profiling details.)

---

## 2. Distribution Insights

* GPA distribution appears approximately normal. 
* Study hours show **moderate variability** with slight **right skewness**, indicating a smaller group of students studies substantially more than average.
* Attendance percentage is generally high across students.
* Box plots comparing GPA across departments show overlapping ranges and similar medians, suggesting comparable academic performance between departments.
* Box plots and violin plots comparing GPA across departments show
overlapping ranges and similar medians, suggesting comparable
academic performance between departments.

The violin plot additionally reveals the full distribution density,
confirming that GPA values follow similar shapes across departments
and that no department shows a distinctly different performance pattern.

(See `output\gpa_by_department.png`)
(See `output\gpa_distribution.png`)
(See `output\gpa_violinplot.png`)

---

## 3. Correlation Analysis

The correlation heatmap shows a strong positive relationship between
study hours and GPA.

**Pearson Correlation Test**

* Correlation coefficient (r) = 0.639
* p-value < 0.001

This indicates a statistically significant positive relationship between
study time and academic performance.

However, **correlation does not imply causation**; higher GPA may also be
influenced by motivation, prior preparation, or other unobserved factors.

(See `output/correlation_heatmap.png`)
(See `output/study_hours_vs_GPA.png`)

---

## 4. Hypothesis Testing

### 4.1 T-test — Internship vs GPA

**Hypotheses**

* H0: Mean GPA is equal for students with and without internships.
* H1: Mean GPA differs between the two groups.

**Test Used:** Independent samples t-test

**Results**

* T-statistic = 13.56
* p-value < 0.001
* Cohen's d = 0.706

**Interpretation**

The result is statistically significant, indicating GPA differs between
students with and without internships.

The effect size represents a **medium-to-large practical effect**,
suggesting the difference is meaningful in real-world academic outcomes.

---

### 4.2 ANOVA — GPA Across Departments

**Hypotheses**

* H0: Mean GPA is equal across all departments.
* H1: At least one department has a different mean GPA.

**Test Used:** One-way ANOVA

**Results**

* F-statistic = 0.667
* p-value = 0.615

**Interpretation**

The result is not statistically significant. Academic performance appears
consistent across departments.

---

### 4.3 Chi-Square Test — Scholarship vs Department

**Hypotheses**

* H0: Scholarship status is independent of department.
* H1: Scholarship status is associated with department.

**Test Used:** Chi-square test of independence

**Results**

* Chi-square statistic = 13.95
* p-value = 0.304
* Degrees of freedom = 12

**Interpretation**

The result is not statistically significant, suggesting scholarship
allocation does not depend on academic department.

---

## 5. Key Takeaways

* Study hours show a strong positive association with GPA.
* Internship participation is linked to meaningful GPA differences.
* Academic performance remains stable across departments.
* Scholarship distribution appears independent of department choice.

---

## 6. Recommendations

1. **Encourage structured study programs**
   Study hours strongly correlate with GPA (r = 0.639, p < 0.001),
   suggesting time-management initiatives may improve outcomes.

2. **Expand internship opportunities**
   Internship participation shows a meaningful academic effect
   (Cohen's d = 0.706), indicating experiential learning benefits students.

3. **Maintain unified academic standards across departments**
   ANOVA results show no GPA differences between departments,
   supporting consistent institutional policies.

---

## 7. References to Visualizations

* See `output/correlation_heatmap.png`
* See `output/study_hours_vs_GPA.png`
* See `output/gpa_by_department.png`
* See `output/data_profile.txt`

---

## 8. Conclusion

Exploratory data analysis revealed that student behavior and experiential
learning factors have stronger associations with academic performance than
departmental affiliation. These findings provide evidence-based directions
for improving student success initiatives.

## Tier 1
Box plots and violin plots comparing GPA across departments show
overlapping ranges and similar medians, suggesting comparable
academic performance between departments.

The violin plot additionally reveals the full distribution density,
confirming that GPA values follow similar shapes across departments
and that no department shows a distinctly different performance pattern.

(See `output\gpa_violinplot.png`)

## Tier 2

An automated EDA report generator (eda_report.py) was implemented
as a reusable module. The tool accepts any pandas DataFrame and
automatically produces:

• Data profile summary
• Distribution plots for numeric variables
• Correlation heatmap
• Missing data visualization
• Outlier detection using the IQR method

The module was validated using test datasets with different
structures to ensure robustness.

## Tier 3

A statistical inference analysis was conducted to evaluate the
difference in GPA between students who completed an internship
and those who did not.

Confidence intervals were estimated using both parametric
(t-test) and non-parametric (bootstrap resampling) methods.
The resulting intervals were highly consistent, indicating
stable and reliable estimates of the population means.

Students with internships showed a higher mean GPA compared
to students without internships, and the non-overlapping
confidence interval ranges suggest a statistically meaningful
difference between the groups.

Power analysis was performed using the calculated effect size
(Cohen’s d = 0.7061), estimating that approximately 33 samples
per group are sufficient to reliably detect the observed effect
in future studies.

To validate statistical reliability, a simulation-based false
positive rate test was conducted. The observed rate (0.052)
closely matched the expected significance level (α = 0.05),
confirming that the analysis pipeline is well calibrated and
does not introduce inflated Type I error.

Overall, Tier 3 moves the analysis from descriptive exploration
to statistically supported conclusions.

(See terminal output from `main.py` execution for numerical results.)