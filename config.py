CHANNEL_ID = -1002242343472
MY_CHAT_ID = 748487218
WORKING_CHAT_ID = CHANNEL_ID

TIME_STEPS = 1000
IMAGE_SIZE = 256

HF_USERNAME = "vikosik3000"
HF_MODEL_NAME = "rugpt2-memes-finetuned"
TOKENIZER_PATH = "ai-forever/rugpt3small_based_on_gpt2"

EVAL_BATCH_SIZE = 6  # прощай видюха

FLUX_PROMPT = "!mEmE_c@t!"
LORA_GENERATION_PARAMS = {
    "loras": [
        {
            "path": "https://v3.fal.media/files/penguin/IlpAt8UtvWlInDEXWo7NL_pytorch_lora_weights.safetensors",
            "scale": 1.7
        }
    ],
    "prompt": "!mEmE_c@t!",
    "embeddings": [],
    "image_size": "square",
    "model_name": None,
    "guidance_scale": 5,
    "enable_safety_checker": True,
}
