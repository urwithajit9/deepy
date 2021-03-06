#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, os
logging.basicConfig(level=logging.INFO)

from deepy.trainers import AdamTrainer, LearningRateAnnealer
from deepy.dataset import BinarizedMnistDataset, MiniBatches

from core import DrawModel

model_path = os.path.join(os.path.dirname(__file__), "models", "mnist1.gz")

if __name__ == '__main__':
    model = DrawModel(image_width=28, image_height=28, attention_times=64)

    trainer = AdamTrainer(model)

    mnist = MiniBatches(BinarizedMnistDataset(), batch_size=100)

    trainer.run(mnist, controllers=[LearningRateAnnealer(trainer)])

    model.save_params(model_path)