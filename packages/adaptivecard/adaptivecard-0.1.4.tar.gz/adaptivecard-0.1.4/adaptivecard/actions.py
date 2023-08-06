from typing import Optional
from typing_extensions import Literal
from adaptivecard.cards import AdaptiveCard
from adaptivecard.mixin import Mixin
from adaptivecard._base_types import Action


class ShowCard(Mixin, Action):
    def __init__(self,
                 card: AdaptiveCard,
                 title: Optional[str] = None,
                 iconUrl: Optional[str] = None,
                 id_: Optional[str] = None,
                 style: Optional[Literal["default", "positive", "destructive"]] = None,
                 fallback: Optional[Action] = None,
                 tooltip: Optional[str] = None,
                 isEnabled: Optional[bool] = None,
                 mode: Optional[Literal["primary", "secondary"]] = None):
        
        self.type = "Action.ShowCard"
        self.title = title
        self.iconUrl = iconUrl
        self.id = id_
        self.style = style
        self.fallback = fallback
        self.tooltip = tooltip
        self.isEnabled = isEnabled
        self.mode = mode
        self.card = card
        self.json_fields = ('type', 'title', 'iconUrl', 'id', 'style', 'fallback', 'tooltip', 'isEnabled', 'mode', 'card')
