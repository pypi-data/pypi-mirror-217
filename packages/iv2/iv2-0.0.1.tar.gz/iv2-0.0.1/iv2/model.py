from typing import Optional, Callable
import torch
import torch.nn as nn
from torch import Tensor
import torch.nn.functional as F
import torchvision.models as models
from torch.nn.parameter import Parameter
from torch.nn.modules.batchnorm import BatchNorm2d
from torchvision.models.resnet import conv1x1, conv3x3


def l2n(x: Tensor, eps: float = 1e-6) -> Tensor:
    return x / (torch.norm(x, p=2, dim=1, keepdim=True) + eps).expand_as(x)


class L2N(nn.Module):

    def __init__(self, eps=1e-6):
        super(L2N, self).__init__()
        self.eps = eps

    def forward(self, x):
        return l2n(x, eps=self.eps)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'eps=' + str(self.eps) + ')'


class GeM(nn.Module):

    def __init__(self, p=3, eps=1e-6):
        super(GeM, self).__init__()
        self.p = Parameter(torch.ones(1)*p)
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        p: int = 3
        eps: float = 1e-6
        input = x.clamp(min=eps)
        _input = input.pow(p)
        t = F.avg_pool2d(_input, (7, 7)).pow(1./p)

        return t

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'p=' + '{:.4f}'.format(self.p.data.tolist()[0]) + ', ' + 'eps=' + str(self.eps) + ')'


class HalfBottleneck(nn.Module):
    expansion: int = 4

    def __init__(
        self,
        inplanes: int,
        planes: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        groups: int = 1,
        base_width: int = 64,
        dilation: int = 1,
        norm_layer: Optional[Callable[..., nn.Module]] = None,
    ) -> None:
        super().__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        width = int(planes * (base_width / 64.0)) * groups
        # Both self.conv2 and self.downsample layers downsample the input when stride != 1
        self.conv1 = conv1x1(inplanes, width)
        self.bn1 = norm_layer(width)
        self.conv2 = conv3x3(width, width, stride, groups, dilation)
        self.bn2 = norm_layer(width)
        # self.conv3 = conv1x1(width, planes * self.expansion)
        # self.bn3 = norm_layer(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        # self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        # out = self.conv3(out)
        # out = self.bn3(out)

        # if self.downsample is not None:
        #     identity = self.downsample(x)

        # out += identity
        # out = self.relu(out)

        return out


class ResNet47_50Net(nn.Module):
    """
    取 resnet50 的 47 层的输出，输出 512 维度
    """
    output_dim = 512

    def __init__(self, dim: int | None = None):
        super().__init__()
        resnet50_model = models.resnet50()
        features = list(resnet50_model.children())[:-3]

        lay4 = list(resnet50_model.children())[-3]
        lay4[-1] = HalfBottleneck(
            inplanes=2048,
            planes=512,
            groups=1,
            base_width=64,
            dilation=1,
            norm_layer=BatchNorm2d
        )
        features.append(lay4)

        self.features = nn.Sequential(*features)
        self.pool = GeM()
        self.norm = L2N()

        self.lwhiten = None
        self.whiten = None

    def forward(self, x: Tensor):
        # featured_t shape: torch.Size([1, dim, 7, 7])
        featured_t: Tensor = self.features(x)
        pooled_t: Tensor = self.pool(featured_t)
        normed_t: Tensor = self.norm(pooled_t)
        o: Tensor = normed_t.squeeze(-1).squeeze(-1)

        # 使每个图像为Dx1列向量(如果有许多图像，则为DxN)
        return o.permute(1, 0)
