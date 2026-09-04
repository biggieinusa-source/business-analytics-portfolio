# Portfolio Volatility Risk Scanner

An end-to-end analytics and decision-support project for identifying securities with elevated future volatility risk. The project combines machine-learning risk scores with an interactive Power BI dashboard so users can monitor portfolio risk, adjust alert thresholds, investigate recent alerts, compare models, and understand the factors driving predictions.

## Project Overview

Financial-market volatility changes over time and varies across securities and sectors. A fixed monitoring rule can therefore produce too many false alerts during some periods and miss meaningful risk during others.

This project addresses that problem by assigning each security-date observation a volatility risk score and converting that score into an alert using a selected classification threshold. The dashboard allows analysts to explore the resulting alerts and evaluate the trade-off between detecting volatility events and generating false positives.

## Business Objective

The primary objective is to support portfolio monitoring by answering five questions:

1. Which securities currently have the highest predicted volatility risk?
2. How does the portfolio alert rate change over time?
3. Which sectors generate the greatest concentration of alerts?
4. How effectively does the selected model detect actual high-volatility events?
5. Which market and security-level features contribute most strongly to the model's predictions?

The dashboard is designed as a decision-support tool. It prioritizes cases for analyst review; it does not provide investment advice or automatically execute trades.

## Dashboard Audience

Potential users include:

- Portfolio and investment analysts
- Market-risk analysts
- Risk managers
- Financial-data analysts
- Researchers studying volatility and classification thresholds

## Data Summary

The final scored dataset contains **204,135 observations** covering **502 securities**. Each observation represents a security on a particular date and includes:

- Security identifiers and company/sector information
- Market-return and price-range measures
- Rolling volatility and technical indicators
- Broader market indicators, including the VIX
- Actual high-volatility outcome
- Predicted volatility-risk score
- Predicted alert classification
- Prediction outcome, such as true positive or false positive

The Power BI model uses three principal tables:

| Table | Purpose |
|---|---|
| Risk Scores | Security-level observations, risk scores, outcomes, and descriptive attributes |
| Model Performance | Validation and final-test model metrics and thresholds |
| Model Drivers | Model coefficients, direction of effect, and relative feature importance |

A dedicated Date Table supports time-based filtering and monthly trend analysis.

## Analytical Approach

### 1. Time-based data separation

The observations were separated chronologically into training, validation, and testing periods. This design evaluates whether the models generalize to later market periods and reduces the risk of using future information to predict the past.

### 2. High-volatility classification

The target variable identifies whether an observation experienced a high-volatility event. Models return a probability or risk score rather than only a class label.

### 3. Models evaluated

Two classification models were compared:

- Logistic Regression
- XGBoost

Logistic Regression provides a transparent baseline and interpretable coefficients. XGBoost provides a flexible nonlinear benchmark.

### 4. Threshold optimization

The default probability threshold of 0.50 was not assumed to be optimal. Candidate thresholds were evaluated on the validation data, and the best F1 result for each model was identified.

| Model | Selected validation threshold | Precision | Recall | F1 score |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.400 | 29.6% | 65.5% | 40.8% |
| XGBoost | 0.475 | 29.1% | 64.5% | 40.1% |

Logistic Regression produced the higher validation F1 score and was selected for final testing at a threshold of **0.400**.

## Final-Test Performance

| Metric | Result |
|---|---:|
| Accuracy | 50.83% |
| Precision | 40.14% |
| Recall / Detection Rate | 88.58% |
| F1 Score | 55.24% |
| ROC-AUC | 68.71% |
| PR-AUC | 52.50% |
| Alert Rate | 75.60% |

### Interpretation

The selected threshold emphasizes detection. The model identifies approximately **88.6%** of actual high-volatility events, but its **40.1% precision** means that many alerts do not become actual high-volatility events. This trade-off may be appropriate when missing a volatility event is considered more costly than reviewing an additional alert.

Accuracy should not be interpreted alone because the outcome classes are uneven and the decision threshold intentionally favors recall. F1, PR-AUC, precision, recall, and the operational alert rate provide a more complete assessment.

## Key Model Drivers

The Logistic Regression coefficients were converted to absolute relative importance values for dashboard reporting. The leading drivers include:

| Feature | Relative importance | Coefficient direction |
|---|---:|---|
| VIX | 22.6% | Increases risk score |
| Average Range (20 days) | 14.2% | Increases risk score |
| Maximum Absolute Return (20 days) | 8.6% | Decreases risk score |
| Mean Absolute Return (20 days) | 7.1% | Increases risk score |
| Volatility (20 days) | 7.0% | Increases risk score |
| SPY Volatility (20 days) | 5.8% | Decreases risk score |
| Volume Ratio (20 days) | 3.5% | Increases risk score |
| Average Range (5 days) | 3.0% | Increases risk score |
| Price to SMA10 | 3.0% | Decreases risk score |
| Mean Absolute Return (5 days) | 2.7% | Decreases risk score |

Coefficient direction must be interpreted while holding the other model variables constant. Relative importance describes coefficient magnitude in the fitted model; it does not prove that a feature causes volatility.

## Power BI Report Pages

### Page 1: Risk Monitor

The Risk Monitor is the operational dashboard. It contains:

- Securities Monitored
- Dynamic Alert Rate
- Actual Volatility Events
- Dynamic Detection Rate
- Dynamic Precision
- User-controlled risk-threshold parameter
- Sector, security, and date-range slicers
- Risk signal versus selected alert threshold trend
- Alert rate by sector
- Latest security risk alerts
- Monthly actual volatility events versus alert rate

### Page 2: Model Insights

The Model Insights page explains model quality and behavior. It contains:

- Final-test F1 Score, PR-AUC, Precision, and Recall cards
- Top 10 volatility-risk drivers
- Validation comparison of Logistic Regression and XGBoost
- Model results summary for validation and final testing

### Page 3: Documentation

The Documentation page provides an in-report summary of the project purpose, dashboard instructions, metric definitions, model limitations, and responsible-use guidance.

## How to Use the Dashboard

1. Adjust the **Risk Threshold** to change the minimum score required to generate an alert.
2. Use **Sector**, **Security**, and **Date Range** slicers to define the portfolio view.
3. Review the KPI cards to understand monitoring coverage and alert performance.
4. Compare the average risk score with the selected threshold over time.
5. Use the sector chart to locate concentrations of elevated risk.
6. Review the latest-alert table to identify securities requiring investigation.
7. Open Model Insights to evaluate performance and interpret the strongest model drivers.
8. Clear selections before interpreting portfolio-wide KPI values.

## Metric Definitions

| Metric | Definition |
|---|---|
| Risk Score | Model-estimated probability or relative likelihood of a high-volatility event |
| Alert | Observation whose risk score is at or above the selected threshold |
| Alert Rate | Percentage of observations classified as alerts |
| Precision | Percentage of alerts that correspond to actual high-volatility events |
| Recall / Detection Rate | Percentage of actual high-volatility events detected by the model |
| F1 Score | Harmonic mean of precision and recall |
| ROC-AUC | Ranking performance across classification thresholds |
| PR-AUC | Precision-recall performance across thresholds; useful when outcomes are imbalanced |
| False Positive | Alert generated when no actual high-volatility event occurs |
| False Negative | Actual high-volatility event that the model fails to flag |

## Dashboard Design Decisions

- The alert threshold is user-controlled to expose the precision-recall trade-off.
- Operational monitoring and model evaluation are separated into different report pages.
- Interactions from the latest-alert table to the top KPI cards are disabled, preventing a selected row from unintentionally changing portfolio-level KPIs.
- Event counts and alert percentages use separate axes in the monthly combination chart.
- Feature importance is limited to the top 10 drivers to preserve readability.
- A light-gray canvas with white visual backgrounds improves contrast without distracting from the data.

## Project Critique

### Strengths

1. **The workflow connects modeling to an operational decision.** The project does more than report model metrics: it turns probabilities into alerts and shows how changing the threshold affects monitoring outcomes.
2. **The chronological evaluation design is appropriate for market data.** Separating training, validation, and testing by time is more realistic than a random split when the intended use is prediction on future observations.
3. **Threshold selection is explicit.** Comparing thresholds on validation data makes the precision-recall trade-off visible instead of treating 0.50 as automatically optimal.
4. **The simple model remained competitive.** Logistic Regression slightly exceeded XGBoost on validation F1, supporting the selection of the more interpretable model rather than assuming that the more complex algorithm must be better.
5. **The report separates operational monitoring from model governance.** Risk Monitor supports investigation, while Model Insights presents validation, final-test results, and model drivers.
6. **Interpretability is built into the deliverable.** Coefficient direction and relative importance help users understand the factors associated with higher or lower model scores.

### Weaknesses and Concerns

1. **The model's discrimination is moderate.** A final-test ROC-AUC of 68.71% indicates useful ranking information, but it is not strong enough to treat every alert as a reliable prediction.
2. **High recall is achieved with a high alert rate.** The model detects 88.58% of actual events, but it alerts on 75.60% of scored observations. Alerting on roughly three quarters of observations may overwhelm users and reduces the practical significance of the recall figure.
3. **Precision remains limited.** At 40.14% precision, fewer than half of the generated alerts correspond to actual high-volatility events. The operational cost of investigating false positives should therefore be quantified.
4. **The target rate changes across time periods.** High-volatility prevalence was approximately 25.0% in training, 21.1% in validation, and 34.2% in testing. This shift can change precision, alert volume, and the apparent value of a fixed threshold.
5. **F1 alone may not represent the business objective.** F1 weights precision and recall equally, but the real costs of a missed event and an unnecessary alert may differ substantially.
6. **Coefficient magnitude is not causality.** The drivers describe associations within the fitted model. Correlated predictors, scaling choices, and changing market regimes can affect coefficient size and direction.
7. **The evaluation is portfolio-wide.** Aggregate results can hide weaker performance for particular sectors, securities, liquidity groups, or volatility regimes.
8. **The dashboard is currently a snapshot.** Without automated refresh, drift monitoring, and retraining controls, model performance can deteriorate without being detected.

### Key Risks and Mitigations

| Risk | Why it matters | Recommended mitigation |
|---|---|---|
| Alert fatigue | A 75.60% alert rate may produce too many cases for meaningful review | Set alert-volume targets, add severity tiers, and optimize the threshold using review capacity and business costs |
| Concept or regime drift | Market relationships and volatility prevalence change over time | Monitor feature, prediction, target, and performance drift; define retraining triggers |
| Temporal leakage | Rolling features or preprocessing fitted across split boundaries could expose future information | Audit feature timestamps, fit preprocessing on training data only, and use walk-forward validation |
| Uneven subgroup performance | Strong aggregate results can conceal weak sectors or securities | Report precision, recall, PR-AUC, and alert rate by sector, liquidity group, and market regime |
| Misinterpretation of risk scores | Users may treat scores as certainty or investment advice | Provide definitions, confidence guidance, tooltips, and a visible responsible-use statement |
| Threshold instability | A threshold selected in one period may not remain optimal | Reassess thresholds on rolling validation windows and compare performance under several cost assumptions |
| Data-quality failures | Missing, delayed, duplicated, or stale market observations can produce unreliable scores | Add automated data-quality checks, refresh timestamps, exception logs, and missing-data alerts |

### Overall Assessment

The project is a strong portfolio demonstration of an end-to-end analytics workflow because it integrates feature engineering, model comparison, threshold optimization, interpretability, and interactive business reporting. Its strongest contribution is the translation of model probabilities into a transparent monitoring process.

The current model should be presented as a **screening and prioritization tool**, not a production-grade trading or risk engine. The next stage should focus less on maximizing a single classification metric and more on operational usefulness: reducing alert volume, assigning costs to false positives and false negatives, testing stability across time and subgroups, and monitoring drift after deployment.

## Limitations

- Financial relationships can change over time because of market regime shifts and concept drift.
- Historical predictive performance does not guarantee future performance.
- The model identifies statistical associations rather than causal relationships.
- A recall-focused threshold can create a high operational alert volume.
- Precision, recall, and alert rate depend on the chosen threshold and selected reporting period.
- The available features and target definition constrain what the model can learn.
- The dashboard does not incorporate transaction costs, portfolio weights, liquidity constraints, or individual risk tolerance.

## Responsible Use

This project is intended for analytics, research, and portfolio-monitoring demonstrations. Model alerts should be combined with current market information, domain expertise, and independent review. The results are not financial advice and should not be used as the sole basis for an investment decision.

## Potential Enhancements

- Add automated data refresh and scheduled model scoring
- Monitor feature drift, target drift, and performance drift
- Add threshold cost analysis for false positives and false negatives
- Compare performance across sectors and market regimes
- Add explainability at the individual-security level
- Incorporate portfolio weights and value-at-risk measures
- Add deployment monitoring and retraining triggers
- Publish a secure Power BI Service version with role-based access

## Tools and Technologies

- Python
- pandas and NumPy
- scikit-learn
- XGBoost
- Power BI Desktop
- Power Query
- DAX
- Parquet
- Git and GitHub

## Repository Structure

```text
portfolio-volatility-risk-scanner/
├── README.md
├── notebooks/          # Data preparation, modeling, and evaluation notebooks
├── data/               # Data documentation or approved sample data
├── power-bi/           # Power BI report and dashboard assets
├── images/             # Dashboard screenshots for this README
└── requirements.txt    # Python dependencies
```

Large data files and confidential or licensed source data should not be committed directly to GitHub. Use a data dictionary, sample dataset, or download instructions where appropriate.

## Author

**Gerald Hlabiso**  
M.S. Analytics, Saint Louis University — Expected December 2026  
[Portfolio](https://gerald-hlabiso.github.io/business-analytics-portfolio/) · [GitHub](https://github.com/gerald-hlabiso) · [LinkedIn](https://www.linkedin.com/in/gerald-hlabiso-9899a4161/)

## License

Add the repository's selected license here. If no license is provided, others may view the public repository but do not automatically receive permission to reuse its contents.
