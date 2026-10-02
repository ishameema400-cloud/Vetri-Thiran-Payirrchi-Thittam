import os
import re
import time
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to(device)
pipe.enable_attention_slicing()

def generate_image(prompt, filename=None):
    if not filename:
        safe = re.sub(r"[^a-zA-Z0-9_-]", "_", prompt)[:20]
        filename = f"{safe}_{int(time.time() * 1000)}.png"

    image = pipe(
        prompt,
        num_inference_steps=12,
        height=320,
        width=320,
    ).images[0]

    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)
    return path