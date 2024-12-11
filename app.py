from flask import Flask, jsonify
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton,
                             QMessageBox, QListWidget, QListWidgetItem, QLabel, QGroupBox,
                             QLineEdit, QInputDialog, QTextEdit, QStatusBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class SNMappingApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.postfix = None
        self.variant_path = None
        self.selected_variants = []
        self.variant_ids = {
            'GA':'I12345',
            'GD': 'I67890',
            'GX': 'I11223',
            'GY': 'I44556',
            'GZ': 'I77889'
        }

        # Set up the user interface
        self.init_ui()

    def init_ui(self):
        # Set the window properties
        self.setWindowTitle("SN and Mapping Sheet Tool")
        self.setGeometry(200, 200, 600, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Postfix Selection
        postfix_group = QGroupBox("Select Postfix")
        postfix_layout = QVBoxLayout()
        self.postfix_dropdown = QComboBox()
        self.postfix_dropdown.addItems(['Select', '_ETSYS', '_SABAL', '_SABIN', 'Other'])
        self.postfix_dropdown.setCurrentText('Select')
        self.postfix_dropdown.currentIndexChanged.connect(self.select_postfix)
        postfix_layout.addWidget(self.postfix_dropdown)
        postfix_group.setLayout(postfix_layout)
        main_layout.addWidget(postfix_group)

        # Variant Selection
        variant_group = QGroupBox("Select Variant")
        variant_layout = QVBoxLayout()
        self.variant_dropdown = QComboBox()
        self.variant_dropdown.addItems(['Select', 'GA', 'GD', 'GX', 'Other'])
        self.variant_dropdown.setCurrentText('Select')
        self.variant_dropdown.currentIndexChanged.connect(self.select_variant)
        variant_layout.addWidget(self.variant_dropdown)
        variant_group.setLayout(variant_layout)
        main_layout.addWidget(variant_group)

        # Button to create SN creation sheet
        self.create_sn_button = QPushButton("Create SN Creation Sheet")
        self.create_sn_button.clicked.connect(self.create_sn_sheet)
        main_layout.addWidget(self.create_sn_button)

        # Multi-selection for Variants
        multi_select_group = QGroupBox("Select Multiple Variants")
        multi_select_layout = QVBoxLayout()
        self.variant_list = QListWidget()
        self.variant_list.setSelectionMode(QListWidget.MultiSelection)
        self.populate_variant_list()
        multi_select_layout.addWidget(self.variant_list)
        multi_select_group.setLayout(multi_select_layout)
        main_layout.addWidget(multi_select_group)

        # Button to create mapping sheets
        self.create_mapping_button = QPushButton("Create Mapping Sheets")
        self.create_mapping_button.clicked.connect(self.create_mapping_sheet)
        main_layout.addWidget(self.create_mapping_button)

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Output will appear here...")
        main_layout.addWidget(self.output_display)

        # Status bar
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        # Set the main layout
        self.setLayout(main_layout)
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        """Stylesheet for a modern look and better visibility."""
        return """
        QWidget {
            font-family: Arial;
            font-size: 14px;
        }
        QGroupBox {
            font-weight: bold;
            color: #333333;
            border: 2px solid #007bff;
            border-radius: 5px;
            margin-top: 15px;
            padding: 10px;
        }
        QPushButton {
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QComboBox {
            padding: 8px;
        }
        QListWidget {
            border: 1px solid #ddd;
            background-color: #f9f9f9;
        }
        QTextEdit {
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 8px;
        }
        QStatusBar {
            background-color: #f0f0f0;
            color: #333;
        }
        """

    def select_postfix(self):
        """Handles postfix selection."""
        selected_postfix = self.postfix_dropdown.currentText()
        if selected_postfix == 'Other':
            self.postfix, ok = QInputDialog.getText(self, "Custom Postfix", "Enter custom postfix:")
        else:
            self.postfix = selected_postfix
        self.output_display.append(f"Selected Postfix: {self.postfix}")

    def select_variant(self):
        """Handles variant selection."""
        variant = self.variant_dropdown.currentText()
        if variant == 'Other':
            self.variant_path, ok = QInputDialog.getText(self, "Custom Variant Path", "Enter the full scope path:")
        else:
            self.variant_path = self.get_variant_path(variant)
        self.output_display.append(f"Selected Variant Path: {self.variant_path}")

    def get_variant_path(self, variant):
        """Returns the path for a given variant."""
        variant_paths = {'GA': 'path1', 'GD': 'path2', 'GX': 'path3'}
        return variant_paths.get(variant, 'default_path')

    def populate_variant_list(self):
        """Populates the multi-selection list."""
        variants = list(self.variant_ids.keys()) + ['more']
        for variant in variants:
            item = QListWidgetItem(variant)
            self.variant_list.addItem(item)

    def create_sn_sheet(self):
        """Creates an SN creation sheet."""
        if not self.postfix or not self.variant_path:
            QMessageBox.warning(self, "Error", "Please select a postfix and variant.")
            return
        self.output_display.append(f"SN Sheet Created with Postfix: {self.postfix} and Path: {self.variant_path}")
        self.status_bar.showMessage("SN Sheet Created Successfully!", 3000)

    def create_mapping_sheet(self):
        """Creates mapping sheets based on selected variants."""
        self.selected_variants.clear()
        selected_ids = []

        for item in self.variant_list.selectedItems():
            variant = item.text()
            if variant == 'more':
                self.prompt_for_ids()
            else:
                selected_ids.append(self.variant_ids.get(variant, "Unknown"))

        if self.selected_variants:
            selected_ids.extend(self.selected_variants)

        self.output_display.append(f"Mapping Sheets for IDs: {', '.join(selected_ids)}")
        self.status_bar.showMessage("Mapping Sheets Created Successfully!", 3000)

    def prompt_for_ids(self):
        """Prompts for additional IDs when 'more' is selected."""
        while True:
            custom_id, ok = QInputDialog.getText(self, "Enter ID", "Enter an additional ID (or leave blank to stop):")
            if not ok or not custom_id:
                break
            self.selected_variants.append(custom_id)


app = Flask(__name__)
@app.route("/main")
def main():
    app = QApplication(sys.argv)
    window = SNMappingApp()
    window.show()
    sys.exit(app.exec_())

@app.route("/")
def home():
    return main()
    #return jsonify(message="Hello, Flask on Vercel!")

if __name__ == "__main__":
    app.run()
