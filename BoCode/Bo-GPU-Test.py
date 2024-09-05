import torch

if torch.cuda.is_available():
    print("GPU is available.")
    print(torch.cuda.get_device_name(0))
else:
    print("GPU is NOT available.")
