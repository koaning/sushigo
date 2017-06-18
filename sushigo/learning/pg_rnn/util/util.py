

def adjust_learning_rate(optimizer,step,lr = 5E-3, half = 30):
    lr = lr * (1/2)**(step/half)
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
    return optimizer