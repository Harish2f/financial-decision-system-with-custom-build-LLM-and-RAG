from sklearn.metrics import confusion_matrix
import numpy as np

class Evaluator:
    def evaluate(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

        tn = int(cm[0, 0])
        fp = int(cm[0, 1])
        fn = int(cm[1, 0])
        tp = int(cm[1, 1])

        total = tn + fp + fn + tp
        accuracy = (tp + tn) / total if total > 0 else 0.0

        return {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "accuracy": accuracy
        }