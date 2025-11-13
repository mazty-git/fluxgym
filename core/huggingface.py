"""HuggingFace integration for model uploading and authentication."""

import os
import gradio as gr
from huggingface_hub import HfApi
from library import huggingface_util
from argparse import Namespace


# Global state for current account
current_account = None


def account_hf():
    """
    Check if user is logged in to HuggingFace.

    Returns:
        dict: Dictionary with 'token' and 'account' keys if logged in, None otherwise
    """
    try:
        with open("HF_TOKEN", "r") as file:
            token = file.read()
            api = HfApi(token=token)
            try:
                account = api.whoami()
                return {"token": token, "account": account['name']}
            except:
                return None
    except:
        return None


def logout_hf():
    """
    Log out from HuggingFace by removing the token file.

    Returns:
        tuple: Gradio update objects for (hf_token, hf_login, hf_logout, repo_owner)
    """
    os.remove("HF_TOKEN")
    global current_account
    current_account = account_hf()
    print(f"current_account={current_account}")
    return (
        gr.update(value=""),
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(value="", visible=False)
    )


def login_hf(hf_token):
    """
    Log in to HuggingFace with the provided token.

    Args:
        hf_token (str): HuggingFace API token

    Returns:
        tuple: Gradio update objects for (hf_token, hf_login, hf_logout, repo_owner)
    """
    api = HfApi(token=hf_token)
    try:
        account = api.whoami()
        if account is not None:
            if "name" in account:
                with open("HF_TOKEN", "w") as file:
                    file.write(hf_token)
                global current_account
                current_account = account_hf()
                return (
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(value=current_account["account"], visible=True)
                )
        return gr.update(), gr.update(), gr.update(), gr.update()
    except:
        print(f"incorrect hf_token")
        return gr.update(), gr.update(), gr.update(), gr.update()


def upload_hf(base_model, lora_rows, repo_owner, repo_name, repo_visibility, hf_token):
    """
    Upload trained LoRA model to HuggingFace.

    Args:
        base_model (str): Base model name
        lora_rows (str): Path to LoRA files
        repo_owner (str): Repository owner username
        repo_name (str): Repository name
        repo_visibility (str): 'public' or 'private'
        hf_token (str): HuggingFace API token
    """
    src = lora_rows
    repo_id = f"{repo_owner}/{repo_name}"
    gr.Info(f"Uploading to Huggingface. Please Stand by...", duration=None)
    args = Namespace(
        huggingface_repo_id=repo_id,
        huggingface_repo_type="model",
        huggingface_repo_visibility=repo_visibility,
        huggingface_path_in_repo="",
        huggingface_token=hf_token,
        async_upload=False
    )
    print(f"upload_hf args={args}")
    huggingface_util.upload(args=args, src=src)
    gr.Info(f"[Upload Complete] https://huggingface.co/{repo_id}", duration=None)


def loaded():
    """
    Initialize HuggingFace account state on app load.

    Returns:
        tuple: Gradio update objects for (hf_token, hf_login, hf_logout, hf_account)
    """
    global current_account
    current_account = account_hf()
    print(f"current_account={current_account}")
    if current_account is not None:
        return (
            gr.update(value=current_account["token"]),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=current_account["account"], visible=True)
        )
    else:
        return (
            gr.update(value=""),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(value="", visible=False)
        )
