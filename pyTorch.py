import torch
import torch.nn as nn
# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using:", device)
# Simple model
model = nn.Linear(10, 5).to(device)
# Random input
x = torch.randn(2, 10).to(device)
output = model(x)
print("Output:", output)