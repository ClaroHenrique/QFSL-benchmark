 
import torch.optim as optim

def create_optimizer(params, learning_rate, epochs=200):
    optimizer = optim.Adam(params, lr=learning_rate, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    return optimizer, scheduler
