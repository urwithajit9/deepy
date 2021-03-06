#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deepy import *
from attention import *

class AttentionReader(object):

    def __init__(self, input_dim, hidden_size, img_width, img_height, glimpse_size):
        self.img_height = img_height
        self.img_width = img_width
        self.glimpse_size = glimpse_size
        self.input_dim = input_dim
        self.hidden_size = hidden_size
        self.output_dim = 2*glimpse_size*glimpse_size

        self.zoomer = ZoomableAttentionWindow(self.img_height, self.img_width, self.glimpse_size)
        self.director_model = Chain(self.input_dim).stack(Dense(self.hidden_size), Dense(5))

    def read(self, x, x_hat, h_dec):
        director_output = self.director_model.output(h_dec)

        center_y, center_x, delta, sigma, gamma = self.zoomer.extract_attention_params(director_output)

        w     = gamma * self.zoomer.zoom_in(x    , center_y, center_x, delta, sigma)
        w_hat = gamma * self.zoomer.zoom_in(x_hat, center_y, center_x, delta, sigma)

        return T.concatenate([w, w_hat], axis=1)