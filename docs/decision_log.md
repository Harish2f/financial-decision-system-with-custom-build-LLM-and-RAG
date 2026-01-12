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