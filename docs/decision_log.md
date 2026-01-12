# Finance AI – Decision Log

## 1. Business Problem
Predict customers who are likely to cause financial risk due to late or missing payments.

Risk is defined as:
- More than 30% of invoices paid late
- or more than 10,000 in unpaid invoices

This definition comes from finance operations and is fully auditable.

---

## 2. Baseline Rule

A customer is flagged as high risk if:
- Average payment delay > 15 days
- or unpaid balance > 10,000

This rule is simple, explainable, and can be run directly in SQL.

---

## 3. Baseline Performance from SQL


Accuracy: 0.956 (95.6%)
- True positives: 325
- False positives: 0
- False negatives: 22

These numbers represent:
- how many risky customers we catch
- how many good customers we block
- how many risks we miss

---

## 4. Decision

ML will only be introduced if it improves:
- risk detection (higher true positives)
- without causing excessive or no false positives

Reason:
- False positives block good customers
- That causes lost revenue and legal issues

Otherwise, the baseline rule will be kept in production.

## 5. Baseline vs ML Comparison

Baseline rule results:

| Metric | Value |
|--------|-------|
| True Positives (risky customers caught) | 325 |
| False Positives (good customers blocked) | 0 |
| False Negatives (risky customers missed) | 22 |
| Accuracy | 95.6% |

ML model results (XGBoost):

| Metric | Value |
|--------|-------|
| True Positives | 347 |
| False Positives | 1 |
| False Negatives | 0 |
| Accuracy | 99.8% |

---

## 6. Business Impact

The ML model detects 22 additional high-risk customers compared to the baseline, at the cost of blocking 1 additional low-risk customer.

Assuming:
- A risky customer costs approximately 20,000 €
- Blocking a good customer costs approximately 5,000 €

Estimated financial impact:

Baseline:
22 × 20,000 € = 440,000 € potential loss

ML:
1 × 5,000 € = 5,000 € potential loss

The ML model reduces expected losses by approximately 435,000 €.

---

## 7. Decision

The ML model is approved for production use, as it significantly improves risk detection with minimal business downside.