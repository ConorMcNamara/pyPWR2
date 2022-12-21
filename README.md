# pwr2

A Python implementation of the [pwr2](https://cran.r-project.org/web/packages/pwr2/index.html) R package; a library
for calculating the power, sample size and minimum detectable effect of 1 and 2-way ANOVA tests.

To quote the documentation

> User friendly functions for power and sample size analysis at one-way and two-way ANOVA settings take either effect
> size or delta and sigma as arguments. They are designed for both one-way and two-way ANOVA settings. 

## Quick Example

```
from pw2.pwr import pwr_1way
results = pwr_1way(5, 15, 0.05, None, 1.5, 1)
print(round(results["power"]), 4)
0.9074
```

## Notes

Whenever possible, I tried to follow the R naming and code-style to ensure as much 1-1 comparison as possible; however,
some liberties were taken to ensure the code follows PEP-8 guidelines.

## References

Pengcheng Lu, Junhao Liu, Devin Koestler. (2017). pwr2: Power and Sample Size Analysis for One-way and Two-way ANOVA
Models. https://cran.r-project.org/web/packages/pwr2/index.html
