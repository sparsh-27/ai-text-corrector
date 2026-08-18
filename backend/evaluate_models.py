import jiwer
from classical_corrector import ClassicalCorrector
from modern_corrector import ModernCorrector
import json
import os

def evaluate_models():
    # Test dataset
    test_cases = [
        {"incorrect": "I am writting a leter to you", "correct": "I am writing a letter to you"},
        {"incorrect": "He dont know nothing about it", "correct": "He doesn't know anything about it"},
        {"incorrect": "There house is over their", "correct": "Their house is over there"},
        {"incorrect": "Can you borow me some money", "correct": "Can you lend me some money"},
        {"incorrect": "I goes to the store every day", "correct": "I go to the store every day"}
    ]
    
    print("Initializing Classical Corrector...")
    classical = ClassicalCorrector()
    print("Initializing Modern Corrector...")
    modern = ModernCorrector()
    
    classical_predictions = []
    modern_predictions = []
    references = []
    
    for case in test_cases:
        references.append(case["correct"])
        classical_predictions.append(classical.correct(case["incorrect"]))
        modern_predictions.append(modern.correct(case["incorrect"]))
        
    # Calculate Word Error Rate (lower is better)
    wer_classical = jiwer.wer(references, classical_predictions)
    wer_modern = jiwer.wer(references, modern_predictions)
    
    print(f"Classical Word Error Rate (WER): {wer_classical:.4f}")
    print(f"Modern Word Error Rate (WER): {wer_modern:.4f}")
    
    winner = "modern" if wer_modern < wer_classical else "classical"
    print(f"Winner: {winner.capitalize()} Corrector!")
    
    # Save the winner to a config file for API to use
    with open("config.json", "w") as f:
        json.dump({"best_model": winner}, f)
        
    return winner

if __name__ == "__main__":
    evaluate_models()
