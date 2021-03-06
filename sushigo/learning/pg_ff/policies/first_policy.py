import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

import numpy as np

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.affine1 = nn.Linear(22, 20)
        self.affine2 = nn.Linear(20, 11)

        self.saved_actions = []
        self.rewards = []

    def forward(self, x):
        x = F.tanh(self.affine1(x))
        action_scores = self.affine2(x)
        return F.softmax(action_scores)

def select_action(state, policy,allowed):
    state = torch.FloatTensor(state).unsqueeze(0)
    probs = policy(Variable(state))

    # pol_print = probs.data.numpy()/np.sum(probs.data.numpy())
    # print('%5.2f'*11%(tuple(pol_print[0])))

    allowed = Variable(torch.FloatTensor(allowed).unsqueeze(0))
    allowed.requires_grad = False
    allowed_probs = torch.mul(probs,allowed)

    # pol_print = allowed_probs.data.numpy()/np.sum(allowed_probs.data.numpy())
    # print('%5.2f'*11%(tuple(pol_print[0])))

    action = allowed_probs.multinomial()
    policy.saved_actions.append(action)
    return action.data.numpy()[0][0]

def finish_game(policy, optimizer):
    rewards = policy.rewards + [0]
    rewards = torch.Tensor(rewards)
    rewards = (rewards - rewards.mean()) / (rewards.std() + np.finfo(np.float32).eps)

    for action, r in zip(policy.saved_actions, rewards):
        action.reinforce(r)
    optimizer.zero_grad()
    autograd.backward(policy.saved_actions, [None for _ in policy.saved_actions])
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_actions[:]
