"""
Sample gallery management functions.

This module handles pagination and display of generated sample images.
"""
import os
from slugify import slugify
from utils.file_utils import resolve_path_without_quotes


def get_samples(lora_name, page=1, page_size=24):
    """
    Get samples with pagination support.

    Args:
        lora_name: Name of the LoRA model
        page: Page number (1-indexed)
        page_size: Number of samples per page

    Returns:
        List of file paths for the current page
    """
    output_name = slugify(lora_name)
    try:
        samples_path = resolve_path_without_quotes(f"outputs/{output_name}/sample")
        files = [os.path.join(samples_path, file) for file in os.listdir(samples_path)]
        files.sort(key=lambda file: os.path.getctime(file), reverse=True)

        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        return files[start_idx:end_idx]
    except:
        return []


def get_total_samples_count(lora_name):
    """
    Get the total number of samples available.

    Args:
        lora_name: Name of the LoRA model

    Returns:
        Total number of sample files
    """
    output_name = slugify(lora_name)
    try:
        samples_path = resolve_path_without_quotes(f"outputs/{output_name}/sample")
        files = [f for f in os.listdir(samples_path) if os.path.isfile(os.path.join(samples_path, f))]
        return len(files)
    except:
        return 0


def load_more_samples(lora_name, current_page, page_size=24):
    """
    Load the next page of samples and return updated info.

    Args:
        lora_name: Name of the LoRA model
        current_page: Current page number
        page_size: Number of samples per page

    Returns:
        Tuple of (all_samples, next_page, info_text)
    """
    next_page = current_page + 1
    all_samples = []

    # Get all samples up to and including the next page
    for page in range(1, next_page + 1):
        samples = get_samples(lora_name, page=page, page_size=page_size)
        all_samples.extend(samples)

    total_count = get_total_samples_count(lora_name)
    shown_count = len(all_samples)
    info_text = f"Showing {shown_count} of {total_count} samples"

    return all_samples, next_page, info_text


def reset_gallery(lora_name, page_size=24):
    """
    Reset gallery to show only the first page.

    Args:
        lora_name: Name of the LoRA model
        page_size: Number of samples per page

    Returns:
        Tuple of (samples, page_number, info_text)
    """
    samples = get_samples(lora_name, page=1, page_size=page_size)
    total_count = get_total_samples_count(lora_name)
    shown_count = min(page_size, total_count)
    info_text = f"Showing {shown_count} of {total_count} samples"
    return samples, 1, info_text


def update_gallery_display(lora_name, current_page, page_size=24):
    """
    Update gallery display with current pagination state.

    Args:
        lora_name: Name of the LoRA model
        current_page: Current page number
        page_size: Number of samples per page

    Returns:
        Tuple of (all_samples, info_text)
    """
    all_samples = []

    # Get all samples up to current page
    for page in range(1, current_page + 1):
        samples = get_samples(lora_name, page=page, page_size=page_size)
        all_samples.extend(samples)

    total_count = get_total_samples_count(lora_name)
    shown_count = len(all_samples)
    info_text = f"Showing {shown_count} of {total_count} samples"

    return all_samples, info_text
