from datetime import datetime
from dataclasses import dataclass


@dataclass
class News:
    url: str
    title: str
    # __published: datetime

    def __repr__(self):
        return f"URL: {self.url}\tTitle: {self.title}\tPublished: {self.published}"
