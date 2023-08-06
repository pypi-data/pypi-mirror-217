"""content.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import List
from typing import Optional

# Third-Party Packages #
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# Local Packages #
from .basetable import BaseTable


# Definitions #
# Classes #
class ContentNode(BaseTable):
    __tablename__ = "contents"

    id: Mapped[int] = mapped_column(primary_key=True)
