import os
import re
import traceback
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QCheckBox, QHBoxLayout, QStackedWidget, QTextEdit,
    QMessageBox, QSpacerItem, QSizePolicy, QComboBox, QStyle
)
from PyQt6.QtCore import Qt, QTimer
from converter import build_fivem_resource

SETTINGS_PATH = os.path.join(os.getenv("APPDATA") or os.getenv("HOME"), "fivem_converter_settings.json")


def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_settings(data):
    try:
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

def get_theme_styles(mode):
    if mode == "dark":
        return {
            "bg": "#121212",
            "fg": "#ffffff",
            "input_bg": "#1e1e1e",
            "input_fg": "#dddddd",
            "border": "#aaa",
            "button_bg": "#2e2e2e",
            "button_fg": "#ffffff",
            "button_hover": "#3399ff"
        }
    else:
        return {
            "bg": "#ffffff",
            "fg": "#000000",
            "input_bg": "#f0f0f0",
            "input_fg": "#000000",
            "border": "#888",
            "button_bg": "#e0e0e0",
            "button_fg": "#000000",
            "button_hover": "#3399ff"
        }


class ConversionProgressPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.status_label = QLabel("")
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)

        self.recent_label = QLabel("Recently Converted:")
        self.recent_buttons_layout = QVBoxLayout()

        self.done_button = QPushButton("Convert Another")
        self.back_button = QPushButton("Back")

        layout.addWidget(self.status_label)
        layout.addWidget(self.summary_text)
        layout.addWidget(self.recent_label)
        layout.addLayout(self.recent_buttons_layout)
        layout.addWidget(self.done_button)
        layout.addWidget(self.back_button)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def update_recent(self, recent_entries):
        for i in reversed(range(self.recent_buttons_layout.count())):
            widget = self.recent_buttons_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for entry in recent_entries[-5:][::-1]:
            if isinstance(entry, dict):
                path = entry.get("path")
                timestamp = entry.get("timestamp")
            else:
                path = entry
                timestamp = ""
            name = os.path.basename(path)
            btn = QPushButton(f"📂 {name} ({timestamp})" if timestamp else f"📂 {name}")
            btn.clicked.connect(lambda _, p=path: os.startfile(p))
            self.recent_buttons_layout.addWidget(btn)


class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.intro_label = QLabel("🚗 FiveM Vehicle Packer")
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intro_label.setStyleSheet("font-size: 20pt; font-weight: bold;")

        self.subtitle_label = QLabel("Easy-to-use conversion tool for GTA V vehicle assets to FiveM Ready assets!")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("font-size: 10pt; font-style: italic; margin-bottom: 10px;")

        self.layout.addWidget(self.intro_label)
        self.layout.addWidget(self.subtitle_label)

        self.output_dir_label = QLabel("Select Output Directory:")
        self.layout.addWidget(self.output_dir_label)

        output_dir_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(os.getenv("TEMP", "/tmp"))
        self.browse_button = QPushButton("Browse")
        output_dir_layout.addWidget(self.output_dir_input)
        output_dir_layout.addWidget(self.browse_button)
        self.layout.addLayout(output_dir_layout)

        self.open_when_done = QCheckBox("Open output folder when done")
        self.open_when_done.setChecked(True)
        self.layout.addWidget(self.open_when_done)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["dark", "light"])
        self.layout.addWidget(QLabel("Select Theme:"))
        self.layout.addWidget(self.theme_selector)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.next_button = QPushButton("Next")
        self.next_button.setFixedHeight(40)
        self.layout.addWidget(self.next_button)


class FolderSelectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.instruction = QLabel("Drag and drop or browse to a folder containing extracted GTA mod files")
        self.instruction.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.layout.addWidget(self.instruction)

        self.info_label = QLabel(
            "\n1. Open the mod's `dlc.rpf` file using CodeWalker or OpenIV."
            "\n2. Extract all relevant files (e.g., `.meta`, `.ytd`, `.yft`, `.ydr`) to a new folder."
            "\n3. Place all these extracted files into a single folder."
            "\n4. Drag that folder into the box below or use the Browse button."
            "\n5. Confirm to begin automatic conversion to FiveM format."
        )
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)
        self.layout.addSpacing(10)

        self.drag_drop_label = DragDropLabel(self)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.drag_drop_label)
        self.layout.addSpacing(10)

        self.browse_button = QPushButton("Browse Folder")
        self.layout.addWidget(self.browse_button)

        self.back_button = QPushButton("Back")
        self.layout.addWidget(self.back_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def handle_folder_drop(self, folder_path):
        reply = QMessageBox.question(
            self,
            "Confirm Conversion",
            f"Start conversion for folder: {os.path.basename(folder_path)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.window().selected_mod_folder = folder_path
            self.instruction.setText(f"Selected folder: {os.path.basename(folder_path)}")
            self.window().run_conversion()


class DragDropLabel(QLabel):
    def __init__(self, parent):
        super().__init__("⬇️ Drag and drop a folder here ⬇️")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #888; padding: 40px;")
        self.parent_ref = parent

    def set_default_style(self, theme):
        if theme == "dark":
            self.setStyleSheet("border: 2px dashed #aaa; color: #aaa; padding: 40px;")
        else:
            self.setStyleSheet("border: 2px dashed #555; color: #555; padding: 40px;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.parent().handle_folder_drop(folder_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FiveM Vehicle Packer")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.resize(500, 500)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.welcome_page = WelcomePage()
        self.folder_select_page = FolderSelectPage()
        self.progress_page = ConversionProgressPage()

        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.folder_select_page)
        self.stack.addWidget(self.progress_page)

        self.settings = load_settings()
        self.theme = self.settings.get("theme", "dark")
        self.apply_theme()

        last_output = self.settings.get("output_dir")
        if last_output:
            self.welcome_page.output_dir_input.setText(last_output)
        self.welcome_page.theme_selector.setCurrentText(self.theme)

        self.welcome_page.browse_button.clicked.connect(self.select_output_dir)
        self.welcome_page.next_button.clicked.connect(self.goto_folder_select)
        self.welcome_page.theme_selector.currentTextChanged.connect(self.switch_theme)

        self.folder_select_page.browse_button.clicked.connect(self.select_mod_folder)
        self.folder_select_page.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.welcome_page))

        self.progress_page.done_button.clicked.connect(self.restart_app)
        self.progress_page.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.welcome_page))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.restart_app()
        elif event.key() == Qt.Key.Key_Return:
            current = self.stack.currentWidget()
            if current == self.welcome_page:
                self.goto_folder_select()

    def apply_theme(self):
        styles = get_theme_styles(self.theme)
        self.setStyleSheet(f"background-color: {styles['bg']}; color: {styles['fg']};")

        button_style = f"""
            QPushButton {{
                background-color: {styles['button_bg']};
                color: {styles['button_fg']};
                border: none;
                padding: 8px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {styles['button_hover']};
                color: white;
            }}
        """

        self.welcome_page.intro_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {styles['fg']};")
        self.welcome_page.subtitle_label.setStyleSheet(f"font-size: 10pt; font-style: italic; margin-bottom: 10px; color: {styles['fg']};")
        self.welcome_page.output_dir_label.setStyleSheet(f"color: {styles['fg']};")
        self.welcome_page.output_dir_input.setStyleSheet(f"background-color: {styles['input_bg']}; color: {styles['input_fg']}; border-radius: 4px;")
        self.welcome_page.open_when_done.setStyleSheet(f"color: {styles['fg']};")
        self.welcome_page.theme_selector.setStyleSheet(f"""
            QComboBox {{ background-color: {styles['input_bg']}; color: {styles['input_fg']}; border-radius: 4px; }}
            QComboBox:hover {{ background-color: {styles['button_hover']}; }}
        """)
        for btn in [self.welcome_page.browse_button, self.welcome_page.next_button]:
            btn.setStyleSheet(button_style)

        self.folder_select_page.instruction.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {styles['fg']};")
        self.folder_select_page.info_label.setStyleSheet(f"color: {styles['fg']};")
        self.folder_select_page.drag_drop_label.set_default_style(self.theme)
        for btn in [self.folder_select_page.browse_button, self.folder_select_page.back_button]:
            btn.setStyleSheet(button_style)

        self.progress_page.status_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {styles['fg']};")
        self.progress_page.summary_text.setStyleSheet(f"background-color: {styles['input_bg']}; color: {styles['input_fg']}; font-family: Consolas, monospace;")
        for btn in [self.progress_page.done_button, self.progress_page.back_button]:
            btn.setStyleSheet(button_style)

    def switch_theme(self, theme):
        self.theme = theme
        self.apply_theme()
        self.settings["theme"] = theme
        save_settings(self.settings)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.welcome_page.output_dir_input.setText(dir_path)
            self.settings["output_dir"] = dir_path
            save_settings(self.settings)

    def goto_folder_select(self):
        self.stack.setCurrentWidget(self.folder_select_page)

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
        self.stack.setCurrentWidget(self.progress_page)
        self.progress_page.status_label.setText("Converting... Please wait.")
        QTimer.singleShot(100, self.convert_files)

    def convert_files(self):
        output_dir = self.welcome_page.output_dir_input.text()
        open_when_done = self.welcome_page.open_when_done.isChecked()

        try:
            model_name = self.get_model_name(self.selected_mod_folder)
            if not model_name:
                self.progress_page.summary_text.append("⚠️ Warning: vehicles.meta missing or malformed. Using fallback model name: convertedcar")
                model_name = "convertedcar"

            output_folder = os.path.join(output_dir, model_name)

            self.progress_page.summary_text.clear()
            self.progress_page.summary_text.append("🧠 Reading metadata files...")
            self.progress_page.summary_text.append("📦 Packing meta files into a data folder...")
            self.progress_page.summary_text.append("🎨 Streaming textures and models into place...")
            self.progress_page.summary_text.append("📝 Generating fxmanifest.lua and vehicle_names.lua...")
            self.progress_page.summary_text.append("🧹 Doing a little cleanup and prep...")

            stream_files, meta_files = build_fivem_resource(
                self.selected_mod_folder, output_folder, model_name
            )

            self.progress_page.status_label.setText("✅ Conversion complete!")
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
                os.startfile(output_folder)

        except Exception as e:
            self.progress_page.status_label.setText("❌ Conversion failed.")
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
            return None

        try:
            with open(vehicles_meta, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = re.findall(r"<modelName>\s*(.*?)\s*</modelName>", content)
            return matches[0] if matches else None
        except Exception:
            return None

    def restart_app(self):
        self.stack.setCurrentWidget(self.folder_select_page)
        self.folder_select_page.instruction.setText("Drag and drop or browse to a folder containing extracted GTA mod files")
        self.folder_select_page.drag_drop_label.setText("⬇️ Drag and drop a folder here ⬇️")
        self.folder_select_page.drag_drop_label.set_default_style(self.theme)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
