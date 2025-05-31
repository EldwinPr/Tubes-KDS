import logging
import os
from datetime import datetime
import pandas as pd
from Bio.Seq import Seq

def setup_logging(log_level=logging.INFO):
    """
    Setup logging untuk track progress dan errors
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/data_processing_{timestamp}.log"
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def validate_sequence(sequence, min_length=400, max_length=800):
    """
    Validate DNA sequence quality
    
    Args:
        sequence (str): DNA sequence
        min_length (int): Minimum acceptable length
        max_length (int): Maximum acceptable length
    
    Returns:
        bool: True if sequence is valid
    """
    if not sequence:
        return False
    
    # Check length
    if len(sequence) < min_length or len(sequence) > max_length:
        return False
    
    # Check for valid nucleotides (allow ATGCN and ambiguous codes)
    valid_chars = set('ATGCNRYSWKMBDHV')
    sequence_chars = set(sequence.upper())
    
    if not sequence_chars.issubset(valid_chars):
        return False
    
    # Check for too many N's or ambiguous characters
    ambiguous_count = sum(1 for char in sequence.upper() if char in 'NRYSWKMBDHV')
    ambiguous_percentage = ambiguous_count / len(sequence)
    
    if ambiguous_percentage > 0.1:  # More than 10% ambiguous
        return False
    
    return True

def clean_sequence(sequence):
    """
    Clean and standardize DNA sequence
    
    Args:
        sequence (str): Raw DNA sequence
    
    Returns:
        str: Cleaned sequence
    """
    if not sequence:
        return ""
    
    # Remove whitespace and convert to uppercase
    cleaned = ''.join(sequence.split()).upper()
    
    # Remove any non-DNA characters except standard ambiguous codes
    valid_chars = 'ATGCNRYSWKMBDHV'
    cleaned = ''.join(char for char in cleaned if char in valid_chars)
    
    return cleaned

def save_checkpoint(data, filename, description=""):
    """
    Save intermediate data sebagai checkpoint
    
    Args:
        data: Data to save (pandas DataFrame, list, etc.)
        filename (str): Output filename
        description (str): Description for logging
    """
    logger = logging.getLogger(__name__)
    
    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(filename, index=False)
        else:
            # For other data types, use pickle
            import pickle
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
        
        logger.info(f"Checkpoint saved: {filename} - {description}")
        
    except Exception as e:
        logger.error(f"Error saving checkpoint {filename}: {e}")

def load_checkpoint(filename):
    """
    Load data dari checkpoint
    
    Args:
        filename (str): File to load
    
    Returns:
        Loaded data
    """
    logger = logging.getLogger(__name__)
    
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(filename)
        else:
            import pickle
            with open(filename, 'rb') as f:
                return pickle.load(f)
                
    except Exception as e:
        logger.error(f"Error loading checkpoint {filename}: {e}")
        return None

# Test function
def test_utils():
    """
    Test utility functions
    """
    # Test sequence validation
    test_sequences = [
        "ATGCGATCGATCGATCG" * 25,  # Valid sequence
        "ATGC" * 10,  # Too short
        "ATGCXYZ" * 50,  # Invalid characters
        "NNNNNNNNNN" * 50,  # Too many N's
    ]
    
    print("Testing sequence validation:")
    for i, seq in enumerate(test_sequences):
        is_valid = validate_sequence(seq)
        print(f"Sequence {i+1}: {'Valid' if is_valid else 'Invalid'}")
    
    # Test sequence cleaning
    dirty_sequence = "  atgc gatc  NNNN xyz  "
    cleaned = clean_sequence(dirty_sequence)
    print(f"\nCleaning test:")
    print(f"Original: '{dirty_sequence}'")
    print(f"Cleaned:  '{cleaned}'")

if __name__ == "__main__":
    test_utils()