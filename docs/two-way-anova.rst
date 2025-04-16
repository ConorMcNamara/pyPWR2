.. _two_way_anova_power:

Power Analysis for Two-Way ANOVA Models
========================================

This document details the concept of statistical power in the context of two-way Analysis of Variance (ANOVA) models. Two-way ANOVA is used to examine the effects of two independent categorical variables (factors) on a continuous dependent variable, as well as their interaction effect. Power analysis is crucial for designing experiments with a sufficient sample size to detect statistically significant main effects and interaction effects if they truly exist.

Introduction
------------

Two-way ANOVA allows researchers to investigate the independent and joint effects of two factors on an outcome variable. Power analysis for this design helps determine the probability of correctly rejecting the null hypotheses associated with each main effect and the interaction effect. Insufficient power increases the risk of Type II errors, where real effects are not detected.

Key Parameters for Power Calculation
------------------------------------

The power of a two-way ANOVA test depends on several key parameters:

* **Significance Level ($\alpha$)**: The probability of rejecting a true null hypothesis (Type I error), typically set at 0.05.
* **Sample Size per Cell ($n$) or Cell Sizes ($n_{ij}$)**: The number of observations in each cell of the design (defined by the combination of levels of the two factors). Equal cell sizes generally maximize power.
* **Number of Levels for Factor A ($a$)**: The number of categories or levels of the first independent variable.
* **Number of Levels for Factor B ($b$)**: The number of categories or levels of the second independent variable.
* **Effect Size**: The magnitude of the effect of each main factor and their interaction. Larger effects are easier to detect. Different effect size measures are used for each effect.
* **Within-Cell Variance ($\sigma^2$)**: The variance of the observations within each cell, assumed to be equal across all cells under the standard ANOVA assumptions (homoscedasticity).

Effect Size Measures for Two-Way ANOVA
---------------------------------------

Similar to one-way ANOVA, various effect size measures exist for two-way ANOVA, focusing on each main effect and the interaction:

* **Partial Eta-squared ($\eta_p^2$)**: Represents the proportion of variance accounted for by each factor or the interaction, *partialling out* the variance associated with other effects in the model.

  * **For Main Effect A**:
    .. math::
       \eta_{pA}^2 = \frac{SS_A}{SS_A + SS_{Error}}

  * **For Main Effect B**:
    .. math::
       \eta_{pB}^2 = \frac{SS_B}{SS_B + SS_{Error}}

  * **For the Interaction Effect (A x B)**:
    .. math::
       \eta_{pAB}^2 = \frac{SS_{AB}}{SS_{AB} + SS_{Error}}

  where $SS_A$, $SS_B$, and $SS_{AB}$ are the sums of squares for main effect A, main effect B, and their interaction, respectively, and $SS_{Error}$ is the error sum of squares.

  **Attribution:** Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

* **Cohen's f**: Can be adapted for each effect in a two-way ANOVA:

  * **For Main Effect A**:
    .. math::
       f_A = \sqrt{\frac{\eta_{pA}^2}{1 - \eta_{pA}^2}}

  * **For Main Effect B**:
    .. math::
       f_B = \sqrt{\frac{\eta_{pB}^2}{1 - \eta_{pB}^2}}

  * **For the Interaction Effect (A x B)**:
    .. math::
       f_{AB} = \sqrt{\frac{\eta_{pAB}^2}{1 - \eta_{pAB}^2}}

  Cohen (1988) provides guidelines for small (f = 0.10), medium (f = 0.25), and large (f = 0.40) effect sizes for each effect.

  **Attribution:** Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

Non-Centrality Parameter ($\lambda$)
------------------------------------

The power calculation for each effect in a two-way ANOVA relies on the non-central F-distribution. The non-centrality parameter differs for each effect:

* **For Main Effect A**:
  .. math::
     \lambda_A = n \cdot b \cdot f_A^2

  (for equal cell sizes $n$)

* **For Main Effect B**:
  .. math::
     \lambda_B = n \cdot a \cdot f_B^2

  (for equal cell sizes $n$)

* **For the Interaction Effect (A x B)**:
  .. math::
     \lambda_{AB} = n \cdot (a - 1) \cdot (b - 1) \cdot f_{AB}^2

  (for equal cell sizes $n$)

For unequal cell sizes ($n_{ij}$), the formulas become more complex and depend on the specific pattern of cell sizes and the definition of the effect size used.

Power Calculation
-----------------

The power for each effect (main effect A, main effect B, and the interaction A x B) is the probability of rejecting the corresponding null hypothesis when the alternative hypothesis is true. It is calculated as:

.. math::
   \text{Power}_X = P(F > F_{\alpha, df_{numerator}, df_{denominator}} | H_{1,X} \text{ is true})

where:
* $X$ represents the effect (A, B, or AB).
* $F$ is the test statistic following a non-central F-distribution with the appropriate degrees of freedom for the numerator and denominator, and the corresponding non-centrality parameter ($\lambda_A$, $\lambda_B$, or $\lambda_{AB}$).
* The degrees of freedom are:
    * Main Effect A: $df_{numerator} = a - 1$, $df_{denominator} = N - a \cdot b$
    * Main Effect B: $df_{numerator} = b - 1$, $df_{denominator} = N - a \cdot b$
    * Interaction A x B: $df_{numerator} = (a - 1)(b - 1)$, $df_{denominator} = N - a \cdot b$
    * where $N$ is the total sample size ($N = n \cdot a \cdot b$ for equal cell sizes).
* $F_{\alpha, df_{numerator}, df_{denominator}}$ is the critical value from the central F-distribution at the chosen significance level $\alpha$ and the respective degrees of freedom.

Software for Power Analysis
--------------------------

Calculating the power of two-way ANOVA by hand is intricate due to the non-central F-distribution. Statistical software packages and programming languages offer functions to perform these calculations:

* **R**: The `power.anova.test()` function in the `pwr` package can be used for balanced designs by specifying the number of groups for each factor. More complex scenarios might require simulations or other packages.
* **Python**: The `FTestAnovaPower()` class in the `statsmodels` library can handle balanced and some unbalanced designs.
* **SAS**: The `PROC POWER` statement with the `TWOWAYANOVA` option.
* **G*Power**: A free and widely used software tool specifically designed for power analysis, including various ANOVA designs.

**Attribution:** Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and clinical sciences. *Behavior Research Methods*, *39*(2), 175-191.

Considerations
--------------

* **Estimating Effect Sizes**: Determining realistic effect sizes for main effects and interactions is crucial. This often relies on prior research, theoretical predictions, or pilot studies.
* **Balanced vs. Unbalanced Designs**: Power is generally maximized when cell sizes are equal. Unbalanced designs can lead to reduced power and can complicate the interpretation of main effects in the presence of interactions. Power analysis for unbalanced designs requires specifying the individual cell sizes.
* **Interaction Effects**: Power to detect interaction effects is often lower than the power to detect main effects, especially if the interaction effect size is small. Larger sample sizes are typically needed to achieve adequate power for interactions.
* **Assumptions of ANOVA**: Power calculations assume that the underlying assumptions of ANOVA (independence, normality, and homogeneity of variances) are met. Violations can affect the actual power.
* **Post-Hoc Power**: As with one-way ANOVA, post-hoc power calculations are generally discouraged. Focus should be on the observed effect sizes and confidence intervals.

Conclusion
----------

Power analysis is a critical step in designing two-way ANOVA studies. By carefully considering the significance level, sample size per cell, number of levels for each factor, and expected effect sizes for both main effects and the interaction, researchers can determine the statistical power of their study and ensure a reasonable chance of detecting true effects. Utilizing appropriate statistical software is essential for accurate power calculations, especially for more complex or unbalanced designs.

References
----------

* Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.
* Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and clinical sciences. *Behavior Research Methods*, *39*(2), 175-191.
* Maxwell, S. E., Delaney, H. D., & Kelley, K. (2018). *Designing experiments and analyzing data: A model comparison perspective* (3rd ed.). Routledge.
* Documentation for statistical software packages (R, Python, SAS).

.. _power_calculation_two_way_anova: