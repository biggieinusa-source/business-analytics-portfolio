# Online Shopper Purchase Prediction Dashboard

## Project Overview

This Power BI project analyzes 2,441 scored online-shopping sessions to explain purchase behavior, compare classification-model results, identify important purchase drivers, and communicate prediction outcomes through an interactive dashboard.

The report is designed to help marketing, e-commerce, and analytics teams understand:

- How frequently website sessions result in purchases
- Which model provides the strongest predictive performance
- Which behavioral features are most associated with purchases
- How conversion varies by month and visitor type
- Where the prediction process produces correct and incorrect classifications

## Dashboard Preview

![Online Shopper Purchase Prediction Dashboard](online-shopper-dashboard-preview.png)

## Key Performance Indicators

| Metric | Result |
|---|---:|
| Total Sessions | 2,441 |
| Actual Purchases | 382 |
| Conversion Rate | 15.65% |
| Prediction Accuracy | 72.88% |

## Key Findings

- Random Forest produced the strongest ROC-AUC score at 78.2%.
- Logistic Regression achieved the highest recall at 78.3%.
- November recorded the highest monthly conversion rate at 25.8%.
- Exit rate was the strongest purchase-prediction driver at 17.8%.
- Product-related page duration was the second-largest driver at 14.2%.
- New visitors converted at a substantially higher rate than returning visitors.
- Prediction outcomes included 1,545 true negatives, 514 false positives, 234 true positives and 148 false negatives.

## Dashboard Features

- Month-controlled interactive slicer
- Dynamic KPI cards
- Model-performance comparison
- Top-eight purchase-driver analysis
- Monthly conversion-rate trend
- Visitor-type conversion comparison
- Confusion-matrix outcome visualization
- Chronological month sorting through a dedicated month table

## Tools and Techniques

- Microsoft Power BI Desktop
- Power Query
- DAX measures
- Data modelling and relationships
- Interactive slicers
- Conditional visual interactions
- KPI and predictive-performance visualization
- Business-insight development

## Business Recommendations

1. Investigate the acquisition channels, campaigns and landing-page experiences associated with converting new visitors.
2. Apply successful first-visit experiences to the larger returning-visitor population.
3. Reduce exit and bounce behavior on product-related pages.
4. Improve product-page content and engagement because product-related duration is a major prediction driver.
5. Prioritize improvements that reduce false positives, which represent the largest model-error category.
6. Use the monthly conversion trend to plan campaigns around stronger seasonal periods.

## Download the Power BI Report

[Download the Power BI dashboard file](online-shopper-purchase-prediction-dashboard.pbix)

> The public interactive Power BI link will be added after Power BI Service access is approved.

## Author

**Gerald Hlabiso**  

[LinkedIn](https://www.linkedin.com/in/gerald-hlabiso-9899a4161/) |
[Portfolio](https://gerald-hlabiso.github.io/business-analytics-portfolio/)
