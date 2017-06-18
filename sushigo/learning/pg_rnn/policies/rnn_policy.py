import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

import numpy as np
np.set_printoptions(2)

class Policy(nn.Module):
    def __init__(self, rnn_type, ninp, nhid, nlayers,num_classes):
        super(Policy, self).__init__()
        self.rnn = getattr(nn, rnn_type)(ninp, nhid, nlayers, bias=False)

        self.decoder = nn.Linear(nhid , num_classes)
        # self.init_weights()

        #Save variables to instance
        self.rnn_type = rnn_type
        self.nhid = nhid
        self.nlayers = nlayers

        self.init_hidden(1)

        self.saved_actions = []
        self.rewards = []

    def init_weights(self):
        initrange = 0.1
        self.decoder.bias.data.fill_(0)
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, input):
        output,self.hidden = self.rnn(input, self.hidden)
        #output in [seq_len,batch_size,hidden_size]
        # Note, the next lines assume batch_size=1 and seq_len=1
        decoded = self.decoder(output.squeeze(0))
        return decoded.exp()

    def init_hidden(self, bsz=1):
        weight = next(self.parameters()).data
        if self.rnn_type == 'LSTM':
            self.hidden = (Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()),
                    Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()))
        else:
            self.hidden =  Variable(weight.new(self.nlayers, bsz, self.nhid).zero_())

def select_action(state, policy,allowed):
    state = torch.FloatTensor(state).unsqueeze(0).unsqueeze(0)
    probs = policy(Variable(state))
    # pol_print = probs.data.numpy()/np.sum(probs.data.numpy())
    # print('%5.2f'*11%(tuple(pol_print[0])))

    allowed = Variable(torch.FloatTensor(allowed).unsqueeze(0))
    allowed.requires_grad = False
    allowed_probs = torch.mul(probs,allowed)
    action = allowed_probs.multinomial()
    policy.saved_actions.append(action)
    return action.data.numpy()[0][0]

def finish_game(policy, gamma, optimizer):
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
    policy.init_hidden()
