.. _one_way_anova_power:

Power Analysis for One-Way ANOVA Models
========================================

This document details the concept of statistical power in the context of one-way Analysis of Variance (ANOVA) models. Power analysis is crucial for designing experiments with a sufficient sample size to detect a statistically significant effect if one truly exists.

Introduction
------------

One-way ANOVA is used to compare the means of two or more independent groups. Power analysis for ANOVA helps determine the probability of correctly rejecting the null hypothesis ($H_0: \mu_1 = \mu_2 = ... = \mu_k$) when the alternative hypothesis ($H_1$: at least one mean is different) is true. A study with low power has a high chance of failing to detect a real effect (Type II error).

Key Parameters for Power Calculation
------------------------------------

The power of a one-way ANOVA test depends on several key parameters:

* **Significance Level ($\alpha$)**: The probability of rejecting the null hypothesis when it is actually true (Type I error). Commonly set at 0.05.
* **Sample Size per Group ($n$) or Group Sizes ($n_1, n_2, ..., n_k$)**: The number of observations in each of the $k$ groups. Equal sample sizes generally lead to higher power.
* **Number of Groups ($k$)**: The number of independent groups being compared.
* **Effect Size**: The magnitude of the difference between the group means. A larger effect size is easier to detect, leading to higher power. Several measures of effect size are used for ANOVA.
* **Within-Group Variance ($\sigma^2$)**: The variance of the observations within each group, assumed to be equal under the standard ANOVA assumptions (homoscedasticity).

Effect Size Measures for One-Way ANOVA
---------------------------------------

Several effect size measures are commonly used for one-way ANOVA:

* **Cohen's f**: A standardized measure of the variance of the population means relative to the common within-group standard deviation ($\sigma$).

  .. math::
     f = \frac{\sigma_m}{\sigma}

  where $\sigma_m$ is the standard deviation of the population means:

  .. math::
     \sigma_m = \sqrt{\frac{\sum_{i=1}^{k} (\mu_i - \mu)^2}{k}}

  and $\mu$ is the grand mean.

  **Attribution:** Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

* **Eta-squared ($\eta^2$)**: The proportion of the total variance in the dependent variable that is accounted for by the independent variable (group membership).

  .. math::
     \eta^2 = \frac{SS_{Between}}{SS_{Total}}

  where $SS_{Between}$ is the sum of squares between groups and $SS_{Total}$ is the total sum of squares.

  **Attribution:** Fisher, R. A. (1925). *Statistical methods for research workers*. Oliver and Boyd.

* **Partial Eta-squared ($\eta_p^2$)**: In more complex ANOVA designs, partial eta-squared represents the proportion of variance accounted for by a factor, partialling out the variance associated with other factors. In a one-way ANOVA, $\eta^2 = \eta_p^2$.

* **Omega-squared ($\omega^2$)**: A less biased estimator of the population variance accounted for by the factor compared to eta-squared.

  .. math::
     \omega^2 = \frac{SS_{Between} - (k - 1)MS_{Within}}{SS_{Total} + MS_{Within}}

  where $MS_{Within}$ is the mean square within groups.

  **Attribution:** Hays, W. L. (1963). *Statistics for psychologists*. Holt, Rinehart and Winston.

Non-Centrality Parameter ($\lambda$)
------------------------------------

The power calculation for ANOVA relies on the non-central F-distribution. The non-centrality parameter ($\lambda$) is a function of the effect size and the sample size:

.. math::
   \lambda = n \sum_{i=1}^{k} \frac{(\mu_i - \mu)^2}{\sigma^2} = n k f^2

for equal sample sizes ($n$ per group). For unequal sample sizes ($n_i$ per group), the formula becomes:

.. math::
   \lambda = \sum_{i=1}^{k} n_i \frac{(\mu_i - \mu)^2}{\sigma^2}

Power Calculation
-----------------

The power of the one-way ANOVA test is the probability of rejecting the null hypothesis when the alternative hypothesis is true. It is calculated as:

.. math::
   \text{Power} = P(F > F_{\alpha, df_1, df_2} | H_1 \text{ is true})

where:
* $F$ is the test statistic following a non-central F-distribution with $df_1 = k - 1$ degrees of freedom for the numerator (between groups) and $df_2 = N - k$ degrees of freedom for the denominator (within groups), and non-centrality parameter $\lambda$ (where $N$ is the total sample size).
* $F_{\alpha, df_1, df_2}$ is the critical value from the central F-distribution at the chosen significance level $\alpha$ and the respective degrees of freedom.

Considerations
--------------

* **Estimating Effect Size**: Determining a realistic effect size is crucial for power analysis. This can be based on previous research, pilot studies, or theoretical expectations. Cohen (1988) provides guidelines for small, medium, and large effect sizes (f = 0.10, 0.25, 0.40, respectively).
* **Assumptions of ANOVA**: Power calculations typically assume that the assumptions of ANOVA (independence of observations, normality of residuals, and homogeneity of variances) are met. Violations of these assumptions can affect the actual power of the test.
* **Post-Hoc Power**: Calculating power after observing the results of a study (post-hoc power) is generally discouraged. It is more informative to focus on the observed effect size and the confidence intervals. Power analysis is most useful during the study design phase (a priori power analysis).
* **Unequal Sample Sizes**: While formulas exist for unequal sample sizes, power is generally maximized when group sizes are equal. If unequal sample sizes are unavoidable, power calculations should account for these differences.

Conclusion
----------

Power analysis is an essential step in designing one-way ANOVA studies. By considering the significance level, sample sizes, number of groups, and expected effect size, researchers can determine the statistical power of their study and ensure an adequate chance of detecting a true effect. Utilizing statistical software is highly recommended for accurate power calculations.

References
----------

* Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.
* Fisher, R. A. (1925). *Statistical methods for research workers*. Oliver and Boyd.
* Hays, W. L. (1963). *Statistics for psychologists*. Holt, Rinehart and Winston.
* Maxwell, S. E., Delaney, H. D., & Kelley, K. (2018). *Designing experiments and analyzing data: A model comparison perspective* (3rd ed.). Routledge.
* Documentation for statistical software packages (R, Python, SAS).

.. _power_calculation_one_way_anova: