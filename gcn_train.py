# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import tensorflow as tf
import yaml
import pandas as pd
from utils.generate_adj_matrix import gen_adj_mx
# from generate_adj_matrix import gen_adj_mx
from lib.utils import load_graph_data
from model.gcn_supervisor import DCRNNSupervisor


def main(args):
    with open(args.config_filename) as f:   #
        supervisor_config = yaml.load(f)

        adj_mx = gen_adj_mx(epsilon=0.5)

        tf_config = tf.ConfigProto()
        if args.use_cpu_only:
            tf_config = tf.ConfigProto(device_count={'GPU': 1})
        tf_config.gpu_options.allow_growth = True
        with tf.Session(config=tf_config) as sess:
            supervisor = DCRNNSupervisor(adj_mx=adj_mx, **supervisor_config)

            supervisor.train(sess=sess)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()      #
    parser.add_argument('--config_filename', default='Data/model/dcrnn_config.yaml', type=str,
                        help='Configuration filename for restoring the model.')
    parser.add_argument('--use_cpu_only', default=False, type=bool, help='Set to true to only use cpu.')
    args = parser.parse_args()
    main(args)