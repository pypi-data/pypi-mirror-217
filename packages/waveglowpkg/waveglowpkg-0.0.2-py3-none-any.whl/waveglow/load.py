import torch
import os
import sys
import time
import gdown

def load_model(download=False):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    waveglow_path = os.path.join(curr_dir, 'waveglow.pt')
    sys.path.insert(0, curr_dir)
    # see if waveglow.pt exists
    if not os.path.exists(waveglow_path) or download:
        # download waveglow.pt
         print("Downloading WaveGlow Weights")
         f_id = '1UJ71BsMIO90LWokp2B84vOl7cvgpnkE4' 
         gdown.download(f'https://drive.google.com/uc?export=download&confirm=pbef&id={f_id}', waveglow_path, quiet=False)            
    
    wave_glow = torch.load(waveglow_path, map_location=device)['model']
    wave_glow = wave_glow.remove_weightnorm(wave_glow)
    
    if device == torch.device('cuda'):
        wave_glow.cuda().eval()
    else:
        wave_glow.eval()
    for m in wave_glow.modules():
        if 'Conv' in str(type(m)):
            setattr(m, 'padding_mode', 'zeros')
            
    return wave_glow