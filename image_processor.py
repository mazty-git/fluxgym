# image_processor.py
#
# A module for processing images using vision-language models.
# Supports Qwen2.5-VL models for image captioning and analysis.

import hashlib
import gc
import tempfile
from PIL import Image
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import os

# Available models configuration
MODEL_OPTIONS = {
    "Qwen2.5-VL-3B-Instruct": {
        "model_id": "Qwen/Qwen2.5-VL-3B-Instruct",
        "description": "Smaller, faster model (3B parameters)",
        "quantized": False
    },
    "Qwen2.5-VL-7B-Instruct": {
        "model_id": "Qwen/Qwen2.5-VL-7B-Instruct",
        "description": "Larger, more accurate model (7B parameters)",
        "quantized": False
    }
}

# Simple default prompt
DEFAULT_PROMPT = "Describe this image in detail."

class ImageProcessor:
    """
    A class for processing images with vision-language models.

    Handles model loading, image processing, and caption generation.
    """

    def __init__(self):
        """Initialize the ImageProcessor with empty model and processor."""
        self.model = None
        self.processor = None
        self.current_model_key = None

    def initialize_model_and_processor(self, model_key="Qwen2.5-VL-3B-Instruct"):
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

        # Set model token limits for images
        min_pixels = 256*28*28
        max_pixels = 1280*28*28

        # Load the model
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(
            model_id, min_pixels=min_pixels, max_pixels=max_pixels
        )

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

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_path},
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        # Prepare inputs
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Generate caption
        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        trimmed_tokens = [
            out[len(inp):] for inp, out in zip(inputs.input_ids, generated_ids)
        ]
        caption = self.processor.batch_decode(
            trimmed_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        return caption
