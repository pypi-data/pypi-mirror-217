from enum import Enum


class Device(Enum):
    MPS = 'mps'
    CPU = 'cpu'
    CUDA = 'cuda'
    CUDNN = 'cudnn'
    MKL = 'mkl'
    MKLDNN = 'mkldnn'
    OPENMP = 'openmp'
    QUANTIZED = 'quantized'


class PilMode(Enum):
    ONE = '1'
    L = 'L'
    P = 'P'
    RGB = 'RGB'
    RGBA = 'RGBA'
    CMYK = 'CMYK'
