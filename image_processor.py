# image_processor.py
#
# A module for processing images using vision-language models.
# Supports Qwen3-VL models for image captioning and analysis.

import hashlib
import gc
import tempfile
from PIL import Image
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor
import os

# Available models configuration
MODEL_OPTIONS = {
    "Qwen3-VL-2B-Instruct": {
        "model_id": "Qwen/Qwen3-VL-2B-Instruct",
        "description": "Smaller, faster model (2B parameters)",
        "quantized": False
    },
    "Qwen3-VL-4B-Instruct": {
        "model_id": "Qwen/Qwen3-VL-4B-Instruct",
        "description": "Medium model (4B parameters)",
        "quantized": False
    },
    "Qwen3-VL-8B-Instruct": {
        "model_id": "Qwen/Qwen3-VL-8B-Instruct",
        "description": "Larger, more accurate model (8B parameters)",
        "quantized": False
    }
}

# Simple default prompt
DEFAULT_PROMPT = "Describe this image in detail."

class ImageProcessor:
    """
    A class for processing images with vision-language models.

    Handles model loading, image processing, and caption generation.
    Requires transformers >= 4.57.0 for Qwen3-VL support.
    """

    def __init__(self):
        """Initialize the ImageProcessor with empty model and processor."""
        self.model = None
        self.processor = None
        self.current_model_key = None

    def initialize_model_and_processor(self, model_key="Qwen3-VL-2B-Instruct"):
        """
        Initialize model and processor based on selected model key.

        Args:
            model_key (str): Key identifying which model to load from MODEL_OPTIONS.

        Returns:
            tuple: The initialized model and processor objects.
        """
        # Only reload if model has changed
        if self.model is not None and model_key == self.current_model_key:
            return self.model, self.processor

        # Clear previous model
        if self.model is not None:
            print(f"Switching from {self.current_model_key} to {model_key}")
            print("Clearing previous model from memory...")

            if torch.cuda.is_available():
                self.model = self.model.cpu()
                torch.cuda.empty_cache()

            del self.model
            del self.processor
            self.model = None
            self.processor = None

            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        # Get model configuration
        model_config = MODEL_OPTIONS[model_key]
        model_id = model_config["model_id"]

        print(f"Loading model: {model_id}")
        print(f"Note: Qwen3-VL requires transformers >= 4.57.0")

        # Load the model using AutoModelForImageTextToText
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_id)

        self.current_model_key = model_key

        return self.model, self.processor

    def process_image(self, image_path, prompt=None):
        """
        Process a single image with a given prompt.

        Args:
            image_path (str): Path to the image file.
            prompt (str, optional): Text prompt for image analysis.

        Returns:
            str: Generated caption.
        """
        if prompt is None:
            prompt = DEFAULT_PROMPT

        # Ensure model is loaded
        if self.model is None:
            self.initialize_model_and_processor()

        # Create messages in Qwen3-VL format
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_path},
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        # Prepare inputs using apply_chat_template
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )
        inputs = inputs.to(self.model.device)

        # Generate caption
        generated_ids = self.model.generate(**inputs, max_new_tokens=128)

        # Trim the prompt from generated output
        generated_ids_trimmed = [
            out_ids[len(in_ids):]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        # Decode to text
        caption = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]

        return caption
