from typing import Any, Optional, Union, Sequence
from typing_extensions import Literal
from adaptivecard.mixin import Mixin
from adaptivecard._base_types import Element, Action




class Content:
    """Content é o elemento que recebe o AdaptiveCard e é adicionado à lista atachments, atributo de Message"""
    def __init__(self, content: "AdaptiveCard"):
        self.contentType = "application/vnd.microsoft.card.adaptive"
        self.content = content
        self.json_fields = ('contentType', 'content')


class Message(Mixin):
    """"Estrutura final do card tal como se requer para envio a um canal do Teams"""
    def __init__(self, attachments: Optional[Sequence["Content"]] = None):
        self.type = "message"
        if attachments is None:
            attachments = []
        if not self.is_sequence(attachments):
            raise TypeError("'attachments' attribute must be a collection of some kind")
        self.attachments = list(attachments)
        self.json_fields = ('type', 'attachments')

    def attach(self, content):
        self.attachments.append(content)


class AdaptiveCard(Mixin):
    """O template principal do card"""  # Essas descrições hão de ficar mais detalhadas à medida que eu desenvolver a lib e sua documentação
    def __init__(self, version: str = "1.2",
                 schema: str = "http://adaptivecards.io/schemas/adaptive-card.json",
                 body: Optional[Union[Element, Sequence[Element]]] = None,
                 actions: Optional[Union[Action, Sequence[Action]]] = None,
                 fallbackText: Optional[str] = None,
                 backgroundImage: Optional[str] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 speak: Optional[str] = None,
                 lang: Optional[str] = None,
                 verticalContentAlignment: Optional[Literal["top", "center", "bottom"]] = None):
        
        self.type = "AdaptiveCard"
        self.version = version  
        self.schema = schema
        self.body = body
        self.actions = actions
        self.fallbackText = fallbackText
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.rtl = rtl
        self.speak = speak
        self.lang = lang
        self.verticalContentAlignment = verticalContentAlignment
        self.json_fields = ('type', 'version', 'schema', 'body', 'actions', 'fallbackText', 'backgroundImage',
                                      'minHeight', 'rtl', 'speak', 'lang', 'verticalContentAlignment', 'actions')

    @property
    def empty(self):
        return len(self.body) == 0

    def append_element(self, element: Element):
        self.body.append(element)

    def append_action(self, action):
        if not hasattr(self, 'actions'):
            self.actions = []
        self.actions.append(action)

    def to_message(self):
        content = Content(content=self)
        msg = Message(attachments=[content])
        return msg
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'body':
            if __value is None:
                __value = []
            elif isinstance(__value, Element):
                __value = [__value]
            if not self.is_sequence(__value):
                raise TypeError(f"{__name} attribute must be a collection of some kind")
        if __name == 'actions' and isinstance(__value, Action):
            __value = [__value]
        return super().__setattr__(__name, __value)