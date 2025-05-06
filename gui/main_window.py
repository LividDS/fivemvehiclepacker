import os
import re
import sys
import traceback
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QFileDialog,
    QMessageBox, QPushButton, QToolBar, QWidget, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from .welcome_page import WelcomePage
from .folder_select_page import FolderSelectPage
from .progress_page import ConversionProgressPage
from .multi_vehicle_page import MultiVehicleCompilerPage
from .utils import load_settings, save_settings, open_folder
from .settings_dialog import SettingsDialog
from .help_dialog import HelpDialog
from converter import build_fivem_resource

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FiveM Vehicle Packer")
        self.resize(500, 500)

        self.settings = load_settings()
        self.language = self.settings.get("language", "en")

        self.stack = QStackedWidget()
        self.single_vehicle_page = QWidget()
        self.multi_vehicle_page = MultiVehicleCompilerPage(language_code=self.language)

        self.welcome_page = WelcomePage(language_code=self.language)
        self.folder_select_page = FolderSelectPage(language_code=self.language)
        self.progress_page = ConversionProgressPage(language_code=self.language)

        self.inner_stack = QStackedWidget()
        self.inner_stack.addWidget(self.welcome_page)
        self.inner_stack.addWidget(self.folder_select_page)
        self.inner_stack.addWidget(self.progress_page)
        self.single_vehicle_page.setLayout(QHBoxLayout())
        self.single_vehicle_page.layout().addWidget(self.inner_stack)

        self.stack.addWidget(self.single_vehicle_page)
        self.stack.addWidget(self.multi_vehicle_page)
        self.setCentralWidget(self.stack)

        self.init_toolbar()

        last_output = self.settings.get("output_dir")
        if last_output:
            self.welcome_page.output_dir_input.setText(last_output)

        self.welcome_page.browse_button.clicked.connect(self.select_output_dir)
        self.welcome_page.next_button.clicked.connect(self.goto_folder_select)

        self.folder_select_page.browse_button.clicked.connect(self.select_mod_folder)
        self.folder_select_page.back_button.clicked.connect(lambda: self.inner_stack.setCurrentWidget(self.welcome_page))

        self.progress_page.done_button.clicked.connect(self.restart_app)
        self.progress_page.back_button.clicked.connect(lambda: self.inner_stack.setCurrentWidget(self.welcome_page))

    def init_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        button_style = """
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 10px;
                margin-right: 6px;
            }
            QPushButton:hover {
                background-color: #3399ff;
                color: white;
            }
        """

        single_btn = QPushButton("Single Vehicle Converter")
        single_btn.setStyleSheet(button_style)
        single_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.single_vehicle_page))
        toolbar.addWidget(single_btn)

        multi_btn = QPushButton("Multi-Vehicle Compiler")
        multi_btn.setStyleSheet(button_style)
        multi_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.multi_vehicle_page))
        toolbar.addWidget(multi_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("Settings")
        settings_btn.setStyleSheet(button_style)
        settings_btn.clicked.connect(self.open_settings_dialog)
        toolbar.addWidget(settings_btn)

        help_btn = QPushButton("❓")
        help_btn.setToolTip("Help")
        help_btn.setStyleSheet(button_style)
        help_btn.clicked.connect(self.open_help_dialog)
        toolbar.addWidget(help_btn)

    def open_settings_dialog(self):
        dialog = SettingsDialog(current_lang=self.language, parent=self)
        if dialog.exec():
            new_lang = dialog.get_selected_language()
            if new_lang != self.language:
                self.language = new_lang
                self.settings["language"] = new_lang
                save_settings(self.settings)
                QMessageBox.information(self, "Restart Required", "Please restart the app to apply language changes.")

    def open_help_dialog(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.restart_app()
        elif event.key() == Qt.Key.Key_Return:
            current = self.inner_stack.currentWidget()
            if current == self.welcome_page:
                self.goto_folder_select()

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.welcome_page.output_dir_input.setText(dir_path)
            self.settings["output_dir"] = dir_path
            save_settings(self.settings)

    def goto_folder_select(self):
        self.inner_stack.setCurrentWidget(self.folder_select_page)

    def select_mod_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Mod Folder")
        if folder_path:
            reply = QMessageBox.question(
                self,
                "Confirm Conversion",
                f"Start conversion for folder: {os.path.basename(folder_path)}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.selected_mod_folder = folder_path
                self.folder_select_page.instruction.setText("Drag and drop or browse to a folder containing extracted GTA mod files")
                self.run_conversion()

    def run_conversion(self):
        self.inner_stack.setCurrentWidget(self.progress_page)
        self.progress_page.status_label.setText("Converting... Please wait.")
        QTimer.singleShot(100, self.convert_files)

    def convert_files(self):
        output_dir = self.welcome_page.output_dir_input.text()
        open_when_done = self.welcome_page.open_when_done.isChecked()

        try:
            model_name = self.get_model_name(self.selected_mod_folder)
            if not model_name:
                self.progress_page.summary_text.append("\u26a0\ufe0f Warning: vehicles.meta missing or malformed. Using fallback model name: convertedcar")
                model_name = "convertedcar"

            output_folder = os.path.join(output_dir, model_name)

            self.progress_page.summary_text.clear()
            self.progress_page.summary_text.append("\ud83e\udde0 Reading metadata files...")
            self.progress_page.summary_text.append("\ud83d\udce6 Packing meta files into a data folder...")
            self.progress_page.summary_text.append("\ud83c\udfa8 Streaming textures and models into place...")
            self.progress_page.summary_text.append("\ud83d\uddd8 Generating fxmanifest.lua and vehicle_names.lua...")
            self.progress_page.summary_text.append("\ud83e\uddf9 Doing a little cleanup and prep...")

            stream_files, meta_files = build_fivem_resource(
                self.selected_mod_folder, output_folder
            )

            self.progress_page.status_label.setText("\u2705 Conversion complete!")
            summary = f"Model: {model_name}\nStreamed files: {len(stream_files)}\nMeta files: {len(meta_files)}\nSaved to: {output_folder}"
            self.progress_page.summary_text.append("\n" + summary)

            recent = self.settings.get("recent_conversions", [])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_entry = {"path": output_folder, "timestamp": timestamp}

            if not any((entry.get("path") if isinstance(entry, dict) else entry) == output_folder for entry in recent):
                recent.append(new_entry)
                self.settings["recent_conversions"] = recent[-10:]
                save_settings(self.settings)

            self.progress_page.update_recent(self.settings["recent_conversions"])

            if open_when_done:
                open_folder(output_folder)

        except Exception as e:
            self.progress_page.status_label.setText("\u274c Conversion failed.")
            error_details = traceback.format_exc()
            self.progress_page.summary_text.setText(f"Error: {str(e)}\n\nDetails:\n{error_details}")

    def get_model_name(self, folder_path):
        vehicles_meta = None
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file == "vehicles.meta":
                    vehicles_meta = os.path.join(root, file)
                    break
        if not vehicles_meta:
            print("vehicles.meta not found in folder:", folder_path)
            return None

        try:
            with open(vehicles_meta, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = re.findall(r"<modelName>\s*(.*?)\s*</modelName>", content)
            if matches:
                return matches[0]
            else:
                print("No <modelName> found in vehicles.meta.")
                return None
        except Exception as e:
            print(f"Error reading or parsing vehicles.meta: {e}")
            return None

    def restart_app(self):
        self.inner_stack.setCurrentWidget(self.folder_select_page)
        self.folder_select_page.instruction.setText("Drag and drop or browse to a folder containing extracted GTA mod files")
        self.folder_select_page.drag_drop_label.setText("\u2b07\ufe0f Drag and drop a folder here \u2b07\ufe0f")
        self.folder_select_page.drag_drop_label.set_default_style("light")