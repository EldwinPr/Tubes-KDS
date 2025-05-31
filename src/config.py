class Config:
    """
    Configuration settings untuk NCBI data fetching dan processing
    """
    
    # NCBI Settings
    NCBI_EMAIL = "18222042@std.stei.itb.ac.id"
    NCBI_DATABASE = "nucleotide"
    
    # Search Parameters
    TARGET_SPECIES = "Biston betularia"
    TARGET_GENE = "COI"
    TARGET_LOCATION = "United Kingdom"
    
    # Data Limits
    MAX_SEQUENCES_TEST = 20     # Untuk testing awal
    MAX_SEQUENCES_FULL = 100    # Untuk full dataset
    
    # Sequence Quality Filters
    MIN_SEQUENCE_LENGTH = 400   # Minimum COI sequence length
    MAX_SEQUENCE_LENGTH = 800   # Maximum COI sequence length
    
    # File Paths
    RAW_DATA_PATH = "data/raw/"
    PROCESSED_DATA_PATH = "data/processed/"
    FINAL_DATA_PATH = "data/final/"
    LOG_PATH = "logs/"
    
    # Haplotype Analysis
    SIMILARITY_THRESHOLD = 0.97  # 97% similarity untuk grouping haplotypes