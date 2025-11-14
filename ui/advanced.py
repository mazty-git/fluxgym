"""Advanced training options UI generation."""

import re
import gradio as gr
import train_network
from library import flux_train_utils


def remove_japanese_text(text):
    """
    Remove Japanese characters from text.

    Args:
        text (str): Input text that may contain Japanese characters

    Returns:
        str: Text with Japanese characters removed, or None if text is None
    """
    if text is None:
        return None

    # Japanese character ranges: Hiragana, Katakana, Kanji
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')

    # Remove Japanese characters
    cleaned = japanese_pattern.sub('', text)

    # Clean up any double spaces or trailing/leading whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # If the result is empty or just punctuation, return None
    if not cleaned or cleaned.isspace() or all(c in '.,;:()[]{}' for c in cleaned):
        return None

    return cleaned


def initialize_advanced_components():
    """
    Initialize advanced training option components.

    Dynamically generates UI components for advanced training parameters
    by parsing the Kohya sd-scripts training arguments. Filters out basic
    parameters that are already in the main UI and removes any Japanese
    text from help descriptions.

    Returns:
        tuple: (advanced_components, advanced_component_ids)
            - advanced_components: List of Gradio components
            - advanced_component_ids: List of component element IDs
    """
    # Define basic arguments that are already in the main UI
    basic_args = {
        'pretrained_model_name_or_path',
        'clip_l',
        't5xxl',
        'ae',
        'cache_latents_to_disk',
        'save_model_as',
        'sdpa',
        'persistent_data_loader_workers',
        'max_data_loader_n_workers',
        'seed',
        'gradient_checkpointing',
        'mixed_precision',
        'save_precision',
        'network_module',
        'network_dim',
        'learning_rate',
        'cache_text_encoder_outputs',
        'cache_text_encoder_outputs_to_disk',
        'fp8_base',
        'highvram',
        'max_train_epochs',
        'save_every_n_epochs',
        'dataset_config',
        'output_dir',
        'output_name',
        'timestep_sampling',
        'discrete_flow_shift',
        'model_prediction_type',
        'guidance_scale',
        'loss_type',
        'optimizer_type',
        'optimizer_args',
        'lr_scheduler',
        'sample_prompts',
        'sample_every_n_steps',
        'max_grad_norm',
        'split_mode',
        'network_args'
    }

    # Generate UI config from parser
    parser = train_network.setup_parser()
    flux_train_utils.add_flux_train_arguments(parser)
    args_info = {}

    for action in parser._actions:
        if action.dest != 'help':  # Skip the default help argument
            args_info[action.dest] = {
                "action": action.option_strings,  # Option strings like '--use_8bit_adam'
                "type": action.type,              # Type of the argument
                "help": action.help,              # Help message
                "default": action.default,        # Default value, if any
                "required": action.required       # Whether the argument is required
            }

    # Sort arguments alphabetically
    temp = []
    for key in args_info:
        temp.append({'key': key, 'action': args_info[key]})
    temp.sort(key=lambda x: x['key'])

    advanced_component_ids = []
    advanced_components = []

    for item in temp:
        key = item['key']
        action = item['action']

        # Skip if it's a basic argument
        if key in basic_args:
            continue

        action_type = str(action['type'])
        component = None

        with gr.Column(min_width=300):
            if action_type == "None":
                # Boolean flag
                component = gr.Checkbox()
            else:
                # String/number input
                component = gr.Textbox(value="")

            if component is not None:
                component.interactive = True
                component.elem_id = action['action'][0]
                component.label = component.elem_id
                component.elem_classes = ["advanced"]

                # Clean help text - remove Japanese characters
                if action['help'] is not None:
                    cleaned_help = remove_japanese_text(action['help'])
                    if cleaned_help:
                        component.info = cleaned_help
                    else:
                        # If help text was entirely Japanese, provide a generic message
                        component.info = "Advanced training parameter (see Kohya documentation)"

        advanced_components.append(component)
        advanced_component_ids.append(component.elem_id)

    return advanced_components, advanced_component_ids
