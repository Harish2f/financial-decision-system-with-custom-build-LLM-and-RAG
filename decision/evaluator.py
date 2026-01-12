from sklearn.metrics import confusion_matrix

class Evaluator:
    def evaluate(self, y_true, y_pred):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        return {
            "tp": int(tp),
            "fp": int(fp),
            "fn": int(fn),
            "accuracy": accuracy
        }