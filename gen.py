import random
import torch
torch.cuda.set_device(0)
import cv2
import numpy as np
from tools.run_infinity import *

model_path='./weights/infinity_2b_reg.pth'
vae_path='./weights/infinity_vae_d32_reg.pth'
text_encoder_ckpt = "./weights/models--google--flan-t5-xl/snapshots/7d6315df2c2fb742f0f5b556879d730926ca9001"

args=argparse.Namespace(
    pn='1M',
    model_path=model_path,
    cfg_insertion_layer=0,
    vae_type=32,
    vae_path=vae_path,
    add_lvl_embeding_only_first_block=1,
    use_bit_label=1,
    model_type='infinity_2b',
    rope2d_each_sa_layer=1,
    rope2d_normalized_by_hw=2,
    use_scale_schedule_embedding=0,
    sampling_per_bits=1,
    text_encoder_ckpt=text_encoder_ckpt,
    text_channels=2048,
    apply_spatial_patchify=0,
    h_div_w_template=1.000,
    use_flex_attn=0,
    cache_dir='/dev/shm',
    checkpoint_type='torch',
    enable_model_cache=False, #modify
    seed=0,
    bf16=1,
    save_file='tmp.jpg'
)

# load text encoder
text_tokenizer, text_encoder = load_tokenizer(t5_path=args.text_encoder_ckpt)
# load vae
vae = load_visual_tokenizer(args)
# load infinity
infinity = load_transformer(vae, args)

prompt = """Ultra‑realistic 35 mm photograph of an outdoor public swimming pool at midday: crystal‑clear turquoise water splashing against tiled edges, sunlit steam rising, wet mosaic deck reflecting sharp summer light, scattered flip‑flops and colorful towels, lifeguard chair with a red umbrella in the background. In the foreground, fixed to a stainless‑steel safety fence, a slightly weather‑worn white sign with bold, uneven red lettering that reads “NO WEARING SHOSES” (intentionally misspelled), edges peeling and casting a delicate shadow on the slick tiles. Shot on a 50 mm f/2.8 lens, high dynamic range, authentic colors, subtle grain, cinematic realism."""
cfg = 3
tau = 0.5
h_div_w = 1/1 # aspect ratio, height:width
seed = random.randint(0, 10000)
enable_positive_prompt=0

h_div_w_template_ = h_div_w_templates[np.argmin(np.abs(h_div_w_templates-h_div_w))]
scale_schedule = dynamic_resolution_h_w[h_div_w_template_][args.pn]['scales']
scale_schedule = [(1, h, w) for (_, h, w) in scale_schedule]
generated_image = gen_one_img(
    infinity,
    vae,
    text_tokenizer,
    text_encoder,
    prompt,
    g_seed=seed,
    gt_leak=0,
    gt_ls_Bl=None,
    cfg_list=cfg,
    tau_list=tau,
    scale_schedule=scale_schedule,
    cfg_insertion_layer=[args.cfg_insertion_layer],
    vae_type=args.vae_type,
    sampling_per_bits=args.sampling_per_bits,
    enable_positive_prompt=enable_positive_prompt,
)
args.save_file = 'ipynb_tmpk.jpg'
os.makedirs(osp.dirname(osp.abspath(args.save_file)), exist_ok=True)
cv2.imwrite(args.save_file, generated_image.cpu().numpy())
print(f'Save to {osp.abspath(args.save_file)}')