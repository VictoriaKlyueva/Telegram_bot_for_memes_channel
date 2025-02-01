import torch
from PIL import Image
from diffusers import DDPMScheduler, UNet2DModel
from config import TIME_STEPS, IMAGE_SIZE, EVAL_BATCH_SIZE
from utils import save_image
from models.yolo_model import check_image

# Load diffusion model and scheduler
scheduler = DDPMScheduler.from_pretrained("google/ddpm-cat-256")
model = UNet2DModel.from_pretrained("google/ddpm-cat-256").to('cuda')
scheduler.set_timesteps(TIME_STEPS)

upload_directory = "models_files/diffuser"
model.from_pretrained(upload_directory).to('cuda')
scheduler.from_pretrained(upload_directory)

print("Диффузионная модель загружена")


def generate_image_diffuser():
    while True:
        random_noise = torch.randn((EVAL_BATCH_SIZE, 3, IMAGE_SIZE, IMAGE_SIZE)).to('cuda')
        model_input = random_noise

        count = 0
        for t in scheduler.timesteps:
            with torch.no_grad():
                noisy_residual = model(model_input, t).sample
                prev_noisy_sample = scheduler.step(noisy_residual, t, model_input).prev_sample
                model_input = prev_noisy_sample

            if count % 100 == 0:
                print(f'Шаг: {count} / {scheduler.timesteps[0]}')

            count += 1

        image_batch = (model_input / 2 + 0.5).clamp(0, 1)
        image_batch = image_batch.cpu().permute(0, 2, 3, 1).numpy()

        for i in range(EVAL_BATCH_SIZE):
            image = image_batch[i]
            image = Image.fromarray((image * 255).round().astype("uint8"))

            if check_image(image):
                return image
            else:
                path = f'generated_data/bad_image_{i}.png'
                save_image(image, path)
                print(f"Фото отклонено для изображения {i}")
