"""
AppButton — a QPushButton that always shows a pointing-hand cursor on hover
and supports a visual 'variant' property for styling via QSS objectName.
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QCursor, QEnterEvent
from PySide6.QtWidgets import QPushButton, QWidget


class AppButton(QPushButton):
    """
    Drop-in replacement for QPushButton with:
    • Pointing-hand cursor automatically applied on hover
    • `variant` parameter sets the objectName so QSS can target it
      e.g. variant="primary"  →  objectName = "PrimaryButton"
           variant="danger"   →  objectName = "DangerButton"
           variant=""         →  plain secondary style
    """

    def __init__(
        self,
        text: str = "",
        variant: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if variant:
            # Convert e.g. "primary" → "PrimaryButton"
            obj_name = variant.capitalize() + "Button"
            self.setObjectName(obj_name)
