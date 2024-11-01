import torch
from diffusers import AutoencoderKLAllegro, AllegroPipeline
from diffusers.utils import export_to_video
vae = AutoencoderKLAllegro.from_pretrained("rhymes-ai/Allegro", subfolder="vae", torch_dtype=torch.float32)
pipe = AllegroPipeline.from_pretrained(
    "rhymes-ai/Allegro", vae=vae, torch_dtype=torch.bfloat16
)
# pipe.to("cuda")
# pipe.vae.enable_tiling()
prompt = "A focused software developer."

positive_prompt = """
(masterpiece), (best quality), (ultra-detailed), (unwatermarked), 
{} 
emotional, harmonious, vignette, 4k epic detailed, shot on kodak, 35mm photo, 
sharp focus, high budget, cinemascope, moody, epic, gorgeous
"""

negative_prompt = """
nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, 
low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry.
"""

prompt = prompt.format(prompt.lower().strip())

video = pipe(prompt, negative_prompt=negative_prompt, guidance_scale=7.5, max_sequence_length=512, num_inference_steps=1, generator = torch.Generator().manual_seed(1)).frames[0]
export_to_video(video, "output.mp4", fps=15)