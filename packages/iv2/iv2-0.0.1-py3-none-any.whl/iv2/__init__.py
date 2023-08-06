from typing import List, Union, Optional, Callable
from pathlib import Path
from io import BytesIO
import torch
import numpy
from PIL import Image
from numpy import ndarray
from torch import Tensor
from torch import device as TorchDevice
from torchvision import transforms
from iv2.schemas import Device, PilMode
from iv2.model import ResNet47_50Net

__version__ = '0.0.1'
VERSION = __version__

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class ResNet:
    def __init__(
        self,
        # weight_file: Union[Path, str],
        device: Union[Device, str] = Device.CPU,
        runtime_model: Union[Path, str, None] = None
    ) -> None:
        assert isinstance(device, (Device, str))
        self.device = TorchDevice(
            device.value if isinstance(device, Device) else device)

        # if isinstance(weight_file, Path):
        #     weight_file = str(weight_file)

        # self.weight_file = weight_file

        assert isinstance(runtime_model, (Path, str))
        self.runtime_model = str(runtime_model) if isinstance(
            runtime_model, Path) else runtime_model

        self.runtime_network = ResNet47_50Net

        self.load_network()
        # self.init_transform()

    def load_network(self):
        state: dict = torch.load(self.runtime_model)

        if self.runtime_network == ResNet47_50Net:
            state['state_dict']['whiten.weight'] = state['state_dict']['whiten.weight'][::, ::]
            state['state_dict']['whiten.bias'] = state['state_dict']['whiten.bias'][::]

            network: ResNet47_50Net = ResNet47_50Net()
            network.load_state_dict(state['state_dict'], strict=False)
            network.eval()
            network.to(self.device)
            self.network = network

    def images_to_vectors(self, images: Tensor) -> Tensor:
        with torch.no_grad():
            _img_tensor = images.to(self.device)
            # features shape: torch.Size([dim, 1])
            features = self.network(_img_tensor)
            vectors = torch.transpose(features, 0, 1)
            return vectors

    def gen_vector(
        self,
        image: Union[Image.Image, ndarray, Path, str, bytes],
        convert_mode: Optional[PilMode] = None,
        preprocess_func: Optional[Callable[[Image.Image], Image.Image]] = None
    ) -> List[float]:
        if isinstance(image, bytes):
            image_file_like = BytesIO(image)
            image = Image.open(image_file_like)
        elif isinstance(image, Image.Image):
            pass
        elif isinstance(image, Path) or isinstance(image, str):
            image = Image.open(str(image))
        elif isinstance(image, ndarray):
            image = Image.fromarray(image)
        else:
            raise Exception(f'Unsupported type: {type(image)}')
        if convert_mode:
            image = image.convert(convert_mode.value)

        batch_size = 1

        if preprocess_func:
            image = preprocess_func(image)

        # preprocessed_image shape: torch.Size([3, 224, 224])
        preprocessed_image: torch.Tensor = preprocess(image)

        # unsqueezed_image shape: torch.Size([1, 3, 224, 224])
        unsqueezed_image = preprocessed_image.unsqueeze(0)

        # _images shape: torch.Size([1, 3, 224, 224])
        _images = torch.cat([unsqueezed_image]*batch_size, dim=0)

        # vectors shape: torch.Size([1, dim])
        vectors = self.images_to_vectors(_images)

        return vectors.squeeze(0).tolist()

    def gen_vectors(
        self,
        images: List[Union[Image.Image, ndarray, Path, str, bytes]],
        convert_mode: Optional[PilMode] = None,
        preprocess_func: Optional[Callable[[Image.Image], Image.Image]] = None
    ) -> List[List[float]]:

        _images: list[Image.Image] = []

        assert isinstance(images, List)
        assert len(images) > 0

        for index, image in enumerate(images):
            if isinstance(image, bytes):
                image_file_like = BytesIO(image)
                image = Image.open(image_file_like)
            elif isinstance(image, Image.Image):
                pass
            elif isinstance(image, Path) or isinstance(image, str):
                image = Image.open(str(image))
            elif isinstance(image, ndarray):
                image = Image.fromarray(image)
            else:
                raise Exception(f'Unsupported type: {type(image)}')

            if preprocess_func:
                image = preprocess_func(image)

            if convert_mode:
                image = image.convert(convert_mode.value)
            assert isinstance(image, Image.Image)
            _images.append(image)

        assert isinstance(
            _images[0], Image.Image), f'images[0] type: {type(_images[0])}'

        for index, image in enumerate(_images):
            preprocessed_image: torch.Tensor = preprocess(image)
            unsqueezed_image = preprocessed_image.unsqueeze(0)
            _images[index] = unsqueezed_image

        _images = torch.cat(_images, dim=0)

        vectors = self.images_to_vectors(_images)

        return vectors.tolist()


def l2(vector1: List[float], vector2: List[float], sqrt: bool = True) -> float:
    """
    标准的 l2 函数，是要开根号的，但是 milvus 出于节约性能考虑，是不开根号的
    所以，我们这里，默认和 milvus 保持一致
    可参考：https://segmentfault.com/a/1190000043678303
    """
    vector1 = numpy.array(vector1)
    vector2 = numpy.array(vector2)
    if sqrt:
        return float(numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2))))
    else:
        return float(numpy.sum(numpy.square(vector1 - vector2)))
