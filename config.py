CHANNEL_ID = -1002242343472
MY_CHAT_ID = 748487218
WORKING_CHAT_ID = MY_CHAT_ID

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
            "scale": 1.8
        }
    ],
    "prompt": "!mEmE_c@t!",
    "embeddings": [],
    "image_size": {
        "width": 512,
        "height": 512
    },
    "model_name": None,
    "guidance_scale": 6,
    "enable_safety_checker": True
}

UPSCALER_PARAMS = {
  "prompt": "masterpiece, best quality, highres",
  "image_url": "",
  "creativity": 0.35,
  "resemblance": 0.6,
  "guidance_scale": 4,
  "upscale_factor": 2,
  "negative_prompt": "(worst quality, low quality, normal quality:2)",
  "num_inference_steps": 18,
  "enable_safety_checker": True
}