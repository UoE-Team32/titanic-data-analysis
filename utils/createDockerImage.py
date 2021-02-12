#!/usr/bin/python

from __future__ import print_function

import sys
import platform
import argparse


def build_arm64_dockerfile(base_docker_file, base_img):
    docker_file = base_docker_file\
        .replace("%BUILD_IMAGE%", base_img)\
        .replace("%END_USER%", "ubuntu")
    return docker_file


def build_x86_dockerfile(base_docker_file):
    docker_file = base_docker_file.replace("%BUILD_IMAGE%", "tensorflow/tensorflow:latest")\
        .replace("%END_USER%", "root")
    return docker_file


def args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--xServer', action='store_true', default=False,
                        help='an integer for the accumulator')
    parser.add_argument('--procs', metavar='N', type=int, default=0,
                        help='an integer for the accumulator')

    return parser


def main(argv):
    docker_file = None
    with open("base.Dockerfile", "r") as fp:
        base_docker_file = fp.read()
        fp.close()

    if platform.machine() in ["arm64", "aarch64"]:
        if argv.xServer:
            docker_file = build_arm64_dockerfile(base_docker_file, "tensorflow-arm-tk")
        else:
            docker_file = build_arm64_dockerfile(base_docker_file, "linaro/tensorflow-arm-neoverse-n1:2.3.0-eigen")
    elif platform.machine() in ["x86_64", "x86"]:
        docker_file = build_x86_dockerfile(base_docker_file)
    else:
        print("Platform not supported")
        sys.exit(1)

    with open("../Dockerfile", "w") as fp:
        fp.write(docker_file)
        fp.close()


if __name__ == '__main__':
    args = args().parse_args()
    main(args)
