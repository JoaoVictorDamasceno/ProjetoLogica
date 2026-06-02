import json
import os

def calculate_metrics(y_true, y_pred):
    valid_pairs = [(t, p) for t, p in zip(y_true, y_pred) if p is not None]
    
    if not valid_pairs:
        return {
            "accuracy": 0, 
            "precision": 0, 
            "recall": 0, 
            "f1": 0, 
            "total_valid": 0, 
            "failures": len(y_true)
        }
    
    # TP (True Positive), TN (True Negative), FP (False Positive), FN (False Negative)
    tp = sum(1 for t, p in valid_pairs if t is True and p is True)
    tn = sum(1 for t, p in valid_pairs if t is False and p is False)
    fp = sum(1 for t, p in valid_pairs if t is False and p is True)
    fn = sum(1 for t, p in valid_pairs if t is True and p is False)
    
    accuracy = (tp + tn) / len(valid_pairs)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "total_valid": len(valid_pairs),
        "failures": len(y_true) - len(valid_pairs)
    }