from typing import Any, Optional, Union
from typing_extensions import Literal
from adaptivecard._base_types import Element
from adaptivecard.mixin import Mixin



class TextBlock(Mixin, Element):
    """Elemento de texto"""
    def __init__(self,
                 text: Any = "",
                 color: Optional[Literal["default", "dark", "light", "accent", "good", "warning", "attention"]] = None,
                 fontType: Optional[Literal["default", "monospace"]] = None,
                 horizontalAlignment: Optional[Literal["left", "center", "right"]] = None,
                 isSubtle: Optional[bool] = None,
                 maxLines: Optional[int] = None,
                 size: Optional[Literal["default", "small", "medium", "large", "extraLarge"]] = None,
                 weight: Optional[Literal["default", "lighter", "bolder"]] = None,
                 wrap: Optional[bool] = None,
                 style: Optional[Literal["default", "heading"]] = None,
                 fallback: Optional[Union[str, Element]] = None,
                 height: Optional[Literal["auto", "stretch"]] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        self.type = "TextBlock"
        self.text = text
        self.color = color
        self.fontType = fontType
        self.horizontalAlignment = horizontalAlignment
        self.isSubtle = isSubtle
        self.maxLines = maxLines
        self.size = size
        self.weight = weight
        self.wrap = wrap
        self.style = style
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'text', 'color', 'fontType', 'horizontalAlignment', 'isSubtle', 'maxLines', 'size', 'weight', 'wrap', 'style', 'fallback',
                            'height', 'separator', 'spacing', 'id', 'isVisible')

    def __repr__(self):
        return f"{self.__class__.__name__}(text='{self.text}')"

    def __str__(self):
        return self.text

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'text' and isinstance(__name, str):
            __value = str(__value)
        return super().__setattr__(__name, __value)


class Image(Mixin, Element):
    def __init__(self,
                 url: str,
                 altText: Optional[str] = None,
                 backgroundColor: Optional[str] = None,
                 height: Optional[str] = None,
                 horizontalAlignment: Optional[Literal["left", "center", "right"]] = None,
                 selectAction: Optional[str] = None):
        self.type = "Image"
        self.json_fields = ('url', 'altText', 'backgroundColor', 'height', 'horizontalAlignment', 'selectAction')