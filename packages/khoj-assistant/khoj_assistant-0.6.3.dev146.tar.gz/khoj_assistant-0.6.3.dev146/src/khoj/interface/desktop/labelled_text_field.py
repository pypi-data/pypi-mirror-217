# External Packages
from PyQt6 import QtWidgets

# Internal Packages
from khoj.utils.config import ProcessorType
from khoj.utils.config import SearchType


class LabelledTextField(QtWidgets.QWidget):
    def __init__(
        self, title, search_type: SearchType = None, processor_type: ProcessorType = None, default_value: str = None
    ):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.processor_type = processor_type
        self.search_type = search_type

        self.label = QtWidgets.QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(95)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.input_field = QtWidgets.QTextEdit(self)
        self.input_field.setFixedWidth(410)
        self.input_field.setFixedHeight(27)
        self.input_field.setText(default_value)

        layout.addWidget(self.input_field)
        layout.addStretch()
