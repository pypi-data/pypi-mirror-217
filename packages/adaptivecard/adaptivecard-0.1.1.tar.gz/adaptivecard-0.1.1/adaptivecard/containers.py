from typing import Any, Optional, Union, Sequence, List, get_type_hints
from typing_extensions import Literal
from adaptivecard._base_types import Element, Action, ISelectAction
from adaptivecard.mixin import Mixin
from tabulate import tabulate
from typeguard import check_type
from adaptivecard.card_elements import TextBlock



class Container(Mixin, Element):
    """Um contâiner é um agrupamento de elementos"""
    def __init__(self,
                 items: Optional[Union[Element, Sequence[Element]]] = None,
                 style: Optional[Literal["default", "emphasis", "good", "attention", "warning", "accent"]] = None,
                 verticalContentAlignment: Optional[Literal["top", "center", "bottom"]] = None,
                 bleed: Optional[bool] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 height: Optional[Literal["auto", "stretch"]] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]] = None,
                 id: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        self.type = "Container"
        self.items = items
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.bleed = bleed
        self.minHeight = minHeight
        self.rtl = rtl
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.json_fields = ('type', 'items', 'style', 'verticalContentAlignment', 'bleed', 'minHeight', 'rtl',
                                      'height', 'separator', 'id', 'isVisible')

    @property
    def empty(self):
        return len(self.items) == 0

    def append_element(self, element: Element):
        self.items.append(element)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self.items})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'items':
            if __value is None:
                __value = []
            elif isinstance(__value, Element):
                __value = [__value]
        return super().__setattr__(__name, __value)


class ColumnSet(Mixin, Element):
    """ColumnSet define um grupo de colunas"""
    def __init__(self, columns: Optional[Sequence["Column"]] = None,
                 style: Optional[Literal["default", "emphasis", "good", "attention", "warning", "accent"]] = None,
                 bleed: Optional[bool] = None,
                 minHeight: Optional[str] = None,   # pensar em algum type check para isso
                 horizontalAlignment: Optional[Literal["left", "center", "right"]] = None,
                 height: Optional[Literal["auto", "stretch"]] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        if columns is None:
            columns = []
        if not self.is_sequence(columns):
            raise TypeError("'columns' attribute must be a Sequence of some kind")

        self.type = 'ColumnSet'
        self.columns = list(columns)
        self.style = style
        self.bleed = bleed
        self.minHeight = minHeight
        self.horizontalAlignment = horizontalAlignment
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'columns', 'style', 'bleed', 'minHeight', 'horizontalAlignment', 'height',
                                      'separator', 'spacig', 'id', 'isVisible')

    def add_to_columns(self, column_element):
        self.columns.append(column_element)


class Column(Mixin, Element):
    """O contâiner Column define um elemento de coluna, que é parte de um ColumnSet."""
    def __init__(self,
                 items: Optional[Sequence[Element]] = None,
                 backgroundImage=None,
                 bleed: Optional[bool] = None,
                 fallback: Optional["Column"] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Union[str, int]] = None,
                 style: Optional[str] = None,
                 verticalContentAlignment: Optional[str] = None,
                 width: Optional[Union[str, int]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        if items is None:
            items = []
        if not self.is_sequence(items):
            raise TypeError(f"'items' must be a Sequence of some kind, not {type(items)}")

        self.type = "Column"
        self.items = list(items)
        self.backgroundImage = backgroundImage
        self.bleed = bleed
        self.fallback = fallback
        self.minHeight = minHeight
        self.rtl = rtl
        self.separator = separator
        self.spacing = spacing
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.width = width
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'items', 'backgroundImage', 'bleed', 'fallback', 'minHeight', 'rtl', 'separator',
                                      'spacing', 'style', 'verticalContentAlignment', 'rtl', 'width', 'id', 'isVisible')

    def add_to_items(self, card_element):
        self.items.append(card_element)


class TableCell(Mixin):
    def __init__(self,
                 items: Optional[Union[Any, Sequence[Any]]] = None,
                 selectAction: Optional[ISelectAction] = None,
                 style: Optional[Literal["default", "emphasis", "good", "attention", "warning", "accent"]] = None,
                 verticalAlignment: Optional[Literal["top", "center", "bottom"]] = None,
                 bleed: Optional[bool] = None,
                 backgroundImage: Optional[str] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None):
      
        if items is None:
            items = []
        elif isinstance(items, Element):
            items = [items]
        elif not self.is_sequence(items):
            items = [TextBlock(text=str(items))]
        else:
            items = list(items)
            for i, item in enumerate(items):
                if not isinstance(item, Element):
                    items[i] = TextBlock(text=str(item))
        self.type = "TableCell"
        self.items = items
        self.selectAction = selectAction
        self.items = items
        self.style = style
        self.verticalAlignment = verticalAlignment
        self.bleed = bleed
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.rtl = rtl
        self.json_fields = ('type', 'items', 'selectAction', 'style', 'verticalAlignment', 'bleed', 'backgroundImage', 'minHeight', 'rtl')

    def add_to_items(self, element: Element):
        self.items.append(element)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[str(item) for item in self.items]})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"


class TableRow(Mixin, Sequence):
    def __init__(self, cells: List, style: Optional[Literal["default", "emphasis", "good", "attention", "warning", "accent"]] = None):
        self.type = "TableRow"
        for i, cell in enumerate(cells):
            if not isinstance(cell, TableCell):
                cells[i] = TableCell(cell)
        self.cells = cells
        self.style = style
        self.json_fields = ("type", "cells", "style")
    def __getitem__(self, __i):
        if isinstance(__i, slice):
            return self.__class__(cells=self.cells[__i])
        return self.cells.__getitem__(__i)
    def __setitem__(self, __key, __value):
        self.cells.__setitem__(__key, TableCell(__value))
    def __add__(self, __value):
        return self.__class__(self.cells + __value.cells)
    def __len__(self):
        return len(self.cells)
    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.cells)})"
    def __str__(self):
        return "[" + ", ".join([str(cell) for cell in self.cells]) + "]"


class Table(Mixin, Element):

    def __init__(self,
                 rows: Optional[Sequence[Sequence[Union[Element, TableCell]]]] = None,
                 firstRowAsHeader: Optional[bool] = None,
                 columns: Sequence[int] = [],
                 showGridLines: Optional[bool] = None,
                 gridStyle: Optional[Literal["default", "emphasis", "good", "attention", "warning", "accent"]] = None,
                 horizontalCellContentAlignment: Optional[Literal["left", "center", "right"]] = None,
                 verticalCellContentAlignment: Optional[Literal["top", "center", "bottom"]] = None,
                 fallback: Optional[Element] = None,
                 height: Optional[Literal["auto", "stretch"]] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        self.type = "Table"

        self.rows = rows
        self._columns = list(columns)
        self.firstRowAsHeader = firstRowAsHeader
        self.showGridLines = showGridLines
        self.gridStyle = gridStyle
        self.horizontalCellContentAlignment = horizontalCellContentAlignment
        self.verticalCellContentAlignment = verticalCellContentAlignment
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'columns', 'rows', 'firstRowAsHeader', 'showGridLines', 'gridStyle',
                                      'horizontalCellContentAlignment', 'verticalContentAlignment', 'fallback', 'height',
                                      'separator', 'spacing', 'id', 'isVisible')
    
    @property
    def columns(self):
        if len(self.rows) > 0:
            if len(self._columns) == 0:
                return [{"width": 1} for _ in self.rows[0]]
            else:
                return [{"width": value} for value in self._columns]

    @columns.setter
    def columns(self, value):
        check_type(value, get_type_hints(self.__init__)['columns'])
        cols = list(value)
        if len(self.rows) > 0 and len(cols) < len(self.rows[0]):
            raise Exception("'length of columns must match the length of rows'")
        self._columns = value

    def __getitem__(self, __i):
        return self.rows.__getitem__(__i)
    
    def append_row(self, row: Sequence):
        if not self.is_sequence(row):
            raise Exception("'row' attribute must be a sequence of some kind")
        row = TableRow(row)
        self.rows.append(row)
    
    def __len__(self):
        return len(self.rows)
    
    def __str__(self):
        rows = [["\n".join([str(item) for item in cell.items]) for cell in row.cells] for row in self.rows]
        if self.firstRowAsHeader:
            headers = rows[0]
            rows = rows[1:]
        else:
            headers = []
        return tabulate(rows, headers=headers, tablefmt='grid')

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'rows':
            rows = __value
            if rows is None:
                rows = []
            elif not self.is_sequence(rows):
                raise TypeError("'rows' attribute must be a sequence of some kind")
            elif len(rows) > 0 and not all(self.is_sequence(row) for row in rows):
                raise TypeError("'rows' attribute must be a sequence of sequences")
            else:
                for i, row in enumerate(rows):
                    for j, cell in enumerate(row):
                        if not isinstance(cell, TableCell):
                            row[j] = TableCell(cell)
                    rows[i] = TableRow(cells=row)

            if len(rows) > 1 and not all([len(rows[i]) == len(rows[i-1]) for i, _ in enumerate(rows[1:])]):
                raise Exception("Length mismatch, all rows must have the same length")
            __value = rows
        return super().__setattr__(__name, __value)


class ActionSet(Mixin, Element):
    def __init__(self,
                 actions: Optional[Union[Action, Sequence[Action]]] = None,
                 fallback: Optional[Element] = None,
                 height: Optional[Any] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None
                 ) -> None:
        self.type = "ActionSet"
        self.actions = actions
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ("actions", "fallback", "height", "separator", "spacing", "id", "isVisible")
    
    def append_action(self, action: Action):
        self.actions.append(action)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __value is None:
            __value = []
        elif isinstance(__value, Element):
            __value = [__value]
        return super().__setattr__(__name, __value)