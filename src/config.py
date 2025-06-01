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
    TARGET_LOCATION = None
    
    # Data Limits - INCREASED for better dataset
    MAX_SEQUENCES_TEST = 100
    MAX_SEQUENCES_FULL = 200
    
    # Sequence Quality Filters
    MIN_SEQUENCE_LENGTH = 300   # Minimum COI sequence length
    MAX_SEQUENCE_LENGTH = 1000   # Maximum COI sequence length
    
    # File Paths
    RAW_DATA_PATH = "data/raw/"
    PROCESSED_DATA_PATH = "data/processed/"
    FINAL_DATA_PATH = "data/final/"
    LOG_PATH = "logs/"
    
    # Haplotype Analysis
    SIMILARITY_THRESHOLD = 0.98  # 95% similarity untuk grouping haplotypes