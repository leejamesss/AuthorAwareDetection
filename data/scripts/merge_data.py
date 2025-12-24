"""
ICNALE Human-AI Data Merger Script

This script processes raw text files from the ICNALE corpus, augments them with metadata,
loads AI-generated data, and merges everything into a single JSONL format dataset.

Usage:
    python data/scripts/merge_data.py --human_input_dir "data/human_data/ICNALE_WE_2.6/WE_0_Unclassified_Unmerged" --metadata_file "data/metadata/human_metadata.csv" --ai_file "data/ai_data/ai_generated_dataset.jsonl" --output "data/authorawarebench.jsonl"
"""

import json
import logging
import argparse
import csv
from pathlib import Path
from typing import Set, Dict, Any, List
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def parse_filename(filename: str) -> tuple:
    """
    Parses the ICNALE filename to extract metadata.

    Expected format: WE_CHN_PTJ0_XXX_YYY_Z.txt

    Returns:
        tuple: (human_code, prompt_type)
    """
    parts = filename.split('_')
    corpus_tag, country_raw, topic_raw, seq_id = parts[0], parts[1], parts[2], parts[3]

    # Handle country code mapping (e.g., TWN -> TWEN)
    country_code = 'TWEN' if country_raw == 'TWN' else country_raw

    # Construct Human Code: WE_CHN_001
    human_code = f"{corpus_tag}_{country_code}_{seq_id}"
    
    # Extract Prompt Type: PTJ or SMK
    prompt_type = topic_raw[:3]

    return human_code, prompt_type


def load_human_metadata_and_codes(metadata_path: Path) -> tuple[Dict[str, Dict[str, str]], Set[str]]:
    """Loads human metadata from CSV file and creates a lookup dictionary and valid codes set."""
    metadata_dict = {}
    valid_codes = set()

    with open(metadata_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            human_code = row['human_code']
            metadata_dict[human_code] = {
                'cefr': row['cefr'],
                'sex': row['sex'],
                'genre': row['genre'],
                'language_env': row['language_env']
            }
            valid_codes.add(human_code)

    logger.info(f"Loaded metadata for {len(metadata_dict)} human codes")
    return metadata_dict, valid_codes


def load_ai_data(ai_path: Path) -> List[Dict[str, Any]]:
    """Loads AI-generated data from JSONL file."""
    ai_data = []
    with open(ai_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                ai_data.append(json.loads(line))

    logger.info(f"Loaded {len(ai_data)} AI-generated samples")
    return ai_data


def process_and_merge_data(human_input_dir: Path, output_file: Path, metadata_dict: Dict[str, Dict[str, str]],
                          valid_codes: Set[str], ai_data: List[Dict[str, Any]]):
    """Processes human files, augments with metadata, merges with AI data, and writes to JSONL."""

    # Find all .txt files recursively or in the specific folder
    txt_files = list(human_input_dir.glob('*.txt'))

    if not txt_files:
        logger.warning(f"No .txt files found in {human_input_dir}")
        return

    logger.info(f"Found {len(txt_files)} human text files. Starting processing...")

    human_entries = []

    # Process human data
    with tqdm(txt_files, desc="Processing human files", unit="file") as pbar:
        for txt_path in pbar:

            filename = txt_path.name
            human_code, prompt_type = parse_filename(filename)

            # Filtering logic
            if human_code not in valid_codes:
                continue

            # Content Reading
            # 'utf-8-sig' handles BOM automatically if present
            content = txt_path.read_text(encoding='utf-8-sig').strip()

            # Get metadata for this human code
            metadata = metadata_dict.get(human_code, {})

            # Construct Data Entry with metadata
            entry: Dict[str, Any] = {
                "text": content,
                "model": "human",
                "prompt_type": prompt_type,
                "human_code": human_code,
                "cefr": metadata["cefr"],
                "sex": metadata["sex"],
                "genre": metadata["genre"],
                "language_env": metadata["language_env"]
            }

            human_entries.append(entry)

    logger.info(f"Processed {len(human_entries)} human entries")

    # Merge with AI data
    all_entries = human_entries + ai_data
    logger.info(f"Total entries after merging: {len(all_entries)} ({len(human_entries)} human + {len(ai_data)} AI)")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for entry in tqdm(all_entries, desc="Writing merged data", unit="entry"):
            out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    logger.info(f"Merge complete. Output written to: {output_file.absolute()}")


def main():
    parser = argparse.ArgumentParser(description="Merge ICNALE human and AI data into JSONL format.")

    parser.add_argument(
        "--human_input_dir",
        type=str,
        default="data/human_data/ICNALE_WE_2.6/WE_0_Unclassified_Unmerged",
        help="Path to the folder containing raw human text files."
    )
    parser.add_argument(
        "--metadata_file",
        type=str,
        default="data/metadata/human_metadata.csv",
        help="Path to the CSV file containing human metadata and valid codes."
    )
    parser.add_argument(
        "--ai_file",
        type=str,
        default="data/ai_data/ai_generated_dataset.jsonl",
        help="Path to the JSONL file containing AI-generated data."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/authorawarebench.jsonl",
        help="Path for the output merged JSONL file."
    )

    args = parser.parse_args()

    human_input_dir = Path(args.human_input_dir)
    metadata_file = Path(args.metadata_file)
    ai_file = Path(args.ai_file)
    output_file = Path(args.output)

    metadata_dict, valid_codes = load_human_metadata_and_codes(metadata_file)
    ai_data = load_ai_data(ai_file)
    process_and_merge_data(human_input_dir, output_file, metadata_dict, valid_codes, ai_data)


if __name__ == "__main__":
    main()
