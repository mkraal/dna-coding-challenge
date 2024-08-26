"""
Helper functions module
"""

import logging
import os
import glob
import sys

logger = logging.getLogger(__name__)


def clear_cache(directory):
    """Removes the index and meta files in target directory"""
    logger.info(f"Clearing meta and index files in {directory}")
    patterns = ["*_index.idx", "*_meta.json"]

    for pattern in patterns:
        full_path_pattern = os.path.join(directory, pattern)
        for file_path in glob.glob(full_path_pattern):
            os.remove(file_path)
    logger.info("Clearing complete")


def configure_logging():
    """Configure logging format"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)
