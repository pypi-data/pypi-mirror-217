from typing import Union, Optional, Collection, Any, List


class Element:
    pass


class ABCTableRow:
    cells: Union["TableCell", Collection["TableCell"]]


class ABCTableCell:
    items: Optional[list]
    selectAction: Any
    style: Optional[str]
    verticalAlignment: Optional[str]
    bleed: Optional[bool]
    backgroundImage: Optional[str]
    backgroundImage: Optional[str]
    minHeight: Optional[str]
    rtl: Optional[bool]


class ABCContent:
    content: "AdaptiveCard"
    contentType: str


class ABCMessage:
    type: str
    attachments: Optional[Collection["Content"]]


class ABCAdaptiveCard:
    version: str
    schema: str
    body: Optional[Collection[Element]]
    fallbackText: Optional[str]
    backgroundImage: Optional[str]
    minHeight: Optional[str]
    rtl: Optional[bool]
    speak: Optional[str]
    lang: Optional[str]
    verticalContentAlignment: Optional[str]


class ABCContainer:
    items: Optional[list]
    style: Optional[str]
    verticalContentAlignment: Optional[str]
    bleed: Optional[bool]
    minHeight: Optional[str]
    rtl: Optional[bool]
    height: Optional[str]
    separator: Optional[str]
    id: Optional[str]
    isVisible: Optional[bool]



class ABCColumnSet:
    columns: Optional[Collection["Column"]]
    style: Optional[str]
    bleed: Optional[bool]
    minHeight: Optional[str]
    horizontalAlignment: Optional[str]
    height: Optional[str]
    separator: Optional[bool]
    spacing: Optional[str]
    id_: Optional[str]
    isVisible: Optional[bool]


class ABCColumn:
    items: Optional[Collection[Union["Image", "TextBlock"]]]
    backgroundImage: Any
    bleed: Optional[bool]
    fallback: Optional["Column"]
    minHeight: Optional[str]
    rtl: Optional[bool]
    separator: Optional[bool]
    spacing: Optional[Union[str, int]]
    style: Optional[str]
    verticalContentAlignment: Optional[str]
    width: Optional[Union[str, int]]
    id_: Optional[str]
    isVisible: Optional[bool]


class ABCTable:
    columns: Collection[int]
    rows: List["TableRow"]
    firstRowAsHeader: Optional[bool]
    showGridLines: Optional[bool]
    gridStyle: Optional[str]
    horizontalCellContentAlignment: Optional[str]
    verticalCellContentAlignment: Optional[str]
    fallback: Optional[Union["ColumnSet", "Container", "Image", "Table"]]
    height: Optional[str]
    separator: Optional[bool]
    spacing: Optional[str]
    id_: Optional[str]
    isVisible: Optional[bool]


class ABCTextBlock:
    text: str
    color: Optional[str]
    fontType: Optional[str]
    horizontalAlignment: Optional[str]
    isSubtle: Optional[bool]
    maxLines: Optional[int]
    size: Optional[str]
    weight: Optional[str]
    wrap: Optional[bool]
    style: Optional[str]
    fallback: Optional[Union[str, "ColumnSet", "Container", "TextBlock"]]
    height: Optional[str]
    separator: Optional[bool]
    spacing: Optional[str]
    id_: Optional[str]
    isVisible: Optional[bool]


class ABCImage:
    type: str
    url: str
    altText: Optional[str]
    backgroundColor: Optional[str]
    height: Optional[str]
    horizontalAlignment: Optional[str]
    selectAction: Optional[str]
