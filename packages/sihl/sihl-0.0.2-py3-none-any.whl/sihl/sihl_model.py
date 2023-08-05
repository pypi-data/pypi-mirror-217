from __future__ import annotations

from typing import Iterable

from torch import Tensor, nn

from sihl.timm_backbone import TimmBackbone
from sihl.torchvision_backbone import TorchvisionBackbone


class SihlModel(nn.Module):
    def __init__(
        self,
        backbone: TorchvisionBackbone | TimmBackbone,
        neck: nn.Module | None,
        heads: list[nn.Module],
    ):
        super().__init__()
        self.backbone = backbone
        self.neck = neck
        self.heads = nn.ModuleList(heads)

    def forward(self, input: Tensor) -> list[Tensor | tuple[Tensor, ...]]:
        x = self.backbone(input)
        if self.neck is not None:
            x = self.neck(x)
        return [head(x) for head in self.heads]
