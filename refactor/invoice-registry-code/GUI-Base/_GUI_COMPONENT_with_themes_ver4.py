import re

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QFileDialog, QInputDialog, QLineEdit, QAbstractButton, QSizePolicy, QMessageBox
)
from themes import THEMES


class WidgetsUpdater:
    def __init__(self):
        pass

    def update_label(self, label_widget, new_text):
        """
        Updates the text of a QLabel widget.

        Parameters:
            label_widget (QLabel): The QLabel widget to update.
            new_text (str): The new text to set on the label.

        Returns:
            None
        """
        if not isinstance(label_widget, QLabel):
            print("The provided widget is not a QLabel.")
            return

        label_widget.setText(new_text)

    def update_button(self, button_widget, new_text, new_callback=None):
        """
        Updates the text and callback of a QPushButton widget.

        Parameters:
            button_widget (QPushButton): The QPushButton widget to update.
            new_text (str): The new text to set on the button.
            new_callback (callable, optional): A new callback function to connect to the button's click event.

        Returns:
            None
        """
        if not isinstance(button_widget, QPushButton):
            print("The provided widget is not a QPushButton.")
            return

        # Update the text
        button_widget.setText(new_text)

        # If a new callback is provided, update it
        if new_callback:
            button_widget.clicked.disconnect()  # Disconnect any previous connections
            button_widget.clicked.connect(new_callback)  # Connect the new callback

    def update_combo_box(self, combo_box_widget, new_items, new_callback=None):
        """
        Updates the items and callback of a QComboBox widget.

        Parameters:
            combo_box_widget (QComboBox): The QComboBox widget to update.
            new_items (list): A list of new items to populate the combo box.
            new_callback (callable, optional): A new callback function to connect to the combo box's selection change event.

        Returns:
            None
        """
        if not isinstance(combo_box_widget, QComboBox):
            print("The provided widget is not a QComboBox.")
            return

        # Clear the existing items
        combo_box_widget.clear()

        # Add new items
        combo_box_widget.addItems(new_items)

        # If a new callback is provided, update it
        if new_callback:
            combo_box_widget.currentIndexChanged.disconnect()  # Disconnect any previous connections
            combo_box_widget.currentIndexChanged.connect(new_callback)  # Connect the new callback

    def update_table_data(self, table_widget, new_data):
        """
        Updates the QTableWidget's cells with new data.

        Parameters:
            table_widget (QTableWidget): The QTableWidget to update.
            new_data (list of list): A 2D list representing the new data for the table.

        Returns:
            None
        """
        if not isinstance(table_widget, QTableWidget):
            print("The provided widget is not a QTableWidget.")
            return

        # Clear current data
        table_widget.clearContents()

        # Set the new data into the table
        for row_idx, row_data in enumerate(new_data):
            for col_idx, cell_data in enumerate(row_data):
                # Make sure the table is large enough
                if row_idx >= table_widget.rowCount():
                    table_widget.insertRow(table_widget.rowCount())
                if col_idx >= table_widget.columnCount():
                    table_widget.insertColumn(table_widget.columnCount())

                # Update the cell
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))


class WidgetsTypes(WidgetsUpdater):
    """
    This class will contain buttons which MainWindow's add_flexible_ribbon will utilize...
    creating a more modulated solution to tackle our problems easily...

    This class will deal with application of the CSS to all of its widgets as well.
    """
    def __init__(self, stylesheet=""):
        # Allow an optional stylesheet to be passed in; otherwise, use the default one.
        super().__init__()
        self.stylesheet = stylesheet

    def apply_stylesheet(self, widget):
        """
        Applies the stylesheet to the given widget.
        """
        widget.setStyleSheet(self.stylesheet)
        return widget

    def button(self, text="Button", on_click=None):
        """
        Creates and returns a QPushButton with the specified text.
        If an on_click callback is provided, it will be connected to the button's clicked signal.
        """
        btn = QPushButton(text)
        if on_click:
            btn.clicked.connect(on_click)
        return self.apply_stylesheet(btn)

    def label(self, text="Label"):
        """
        Creates and returns a QLabel with the specified text.
        """
        lbl = QLabel(text)
        return self.apply_stylesheet(lbl)

    def combo_box(self, items=None, callback=None):
        """
        Creates and returns a QComboBox with the specified items.
        If a list of items is provided, they will be added to the combo box.
        Also connects multiple callback functions to the combo box's currentIndexChanged signal.

        Parameters:
            items (list): The list of items to populate the combo box.
            callbacks (func): A callback functions to connect to the combo box's currentIndexChanged signal.

        Returns:
            QComboBox: The created combo box widget.
        """
        cb = QComboBox()

        if items is not None:
            cb.addItems(items)

        if callback:
            cb.currentIndexChanged.connect(callback)

        return self.apply_stylesheet(cb)

    def input_box(self, placeholder="Enter text"):
        """
        Creates and returns a QLineEdit with an optional placeholder text.
        """
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        return self.apply_stylesheet(line_edit)

    def table(self, rows=0, columns=0, data=None, headers=None):
        """
        Creates and returns a QTableWidget with the specified number of rows and columns.

        - Supports data population (`data` should be a list of lists).
        - Supports column headers (`headers` should be a list).
        - Applies stylesheet to maintain uniform design.

        Parameters:
            rows (int): Number of rows.
            columns (int): Number of columns.
            data (list of lists, optional): Data to populate the table (must match row/column count).
            headers (list, optional): Column headers.

        Returns:
            QTableWidget: The created table widget.
        """
        print(rows, columns, data, headers)
        tbl = QTableWidget(rows, columns)

        if headers:
            tbl.setHorizontalHeaderLabels(headers)

        if data:
            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    tbl.setItem(row_idx, col_idx, item)

        return self.apply_stylesheet(tbl)

    def prompt_user_input(self, title, prompt, default_text=""):
        """
        Prompts the user for input using a dialog box.

        Args:
            title (str): Title of the dialog box.
            prompt (str): Prompt message for the user.
            default_text (str, optional): Default text in the input box. Defaults to "".

        Returns:
            str: User's input or None if canceled.
        """
        input_dialog = QInputDialog()
        text, ok = input_dialog.getText(title, prompt, text=default_text)
        return text if ok else None

    def open_file_dialog(self, title, filter):
        """
        Opens a file dialog to select a file.

        Args:
            title (str): Title of the file dialog.
            filter (str): File filter (e.g., "Database Files (*.db *.sqlite)").

        Returns:
            str: Selected file path or None if canceled.
        """
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(title, "", filter, options=options)
        return file_name if file_name else None


class MainWindow(QMainWindow, WidgetsTypes):
    def __init__(self, pos_x=100, pos_y=100, width=800, height=600, screen_name="Fully Modular PyQt5 Application"):
        super().__init__()
        self.labels = {}  # Stores label widgets and their modifiable status
        self.input_values = []  # Stores all input box values
        self.input_boxes = []  # Stores all the input boxes instances.
        self.widgets_container = {}
        self.init_ui(pos_x, pos_y, width, height, screen_name)
        self.current_theme = "dark"  # Default theme (switch will cause some problems.. look into journels for details)
        self.current_theme_dict = THEMES[self.current_theme]


    def init_ui(self, pos_x, pos_y, width, height, screen_name):
        """
        Initialization must use the self.widgets_container. This self.widgets_container is what will be
        continuously as per user's call to this function will keep on modifying...

        :param pos_x:
        :param pos_y:
        :param width:
        :param height:
        :param screen_name:
        :return:
        """
        central_widget = QWidget()
        central_widget.setObjectName("qvboxlayout_central_widget")  # Set an object name
        self.setWindowTitle(screen_name)
        self.setGeometry(pos_x, pos_y, width, height)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.widgets_container["qvboxlayout_central_widget"] = self.main_layout

    def add_flexible_ribbon(self, ribbon_config, parent_layout, container_dict):
        """
            Recursively parses a nested dictionary to construct a flexible ribbon, handling containers,
            widgets, and ComboBox creation. Returns a dictionary of widget instances (and container layouts)
            for further modification.

            the return is self.widget_container

            Parameters:
                ribbon_config (dict): Configuration dictionary defining the UI structure. Keys that
                    represent container layouts must start with one of the following prefixes (case insensitive):
                        - "qhboxlayout_"  → QHBoxLayout
                        - "qvboxlayout_"  → QVBoxLayout
                        - "scrollh_"     → Horizontal scroll container (internally a QHBoxLayout, can be embedded in a QScrollArea)
                        - "scrollv_"     → Vertical scroll container (internally a QVBoxLayout, can be embedded in a QScrollArea)
                    For widget definitions, the dictionary should include the key "widget_type" with one of the following values:
                        - "button": Requires keys such as "text", "callback", "style", and "hover_style" (optional)
                        - "label":  Requires key "text" and optionally "style"
                        - "combo_box": Requires keys "items", "callback", "label_text", and optionally "style" and "hover_style"
                parent_layout (QLayout, optional): The layout to which the generated UI elements will be added.
                    Defaults to self.main_layout.

            Returns:
                dict: A dictionary mapping each key in the configuration to its created widget instance or
                      container layout. This allows for further dynamic modifications after creation.

            Supported Container Types:
                - qhboxlayout_: Creates a QHBoxLayout.
                - qvboxlayout_: Creates a QVBoxLayout.
                - scrollh_: Creates a horizontally scrollable container.
                - scrollv_: Creates a vertically scrollable container.

            Supported Widget Types:
                - button: Creates a QPushButton (via _add_button_to_layout). Must specify a "callback" (as a function or a string name)
                          and a "text" property.
                - label:  Creates a QLabel. Must specify a "text" property.
                - combo_box: Creates a QComboBox with an optional label. Must specify "items" (a list) and "callback".

            Examples:

            Example 1 - Basic Ribbon with Labels, Buttons, and a ComboBox:
                ribbon_config = {
                    "qhboxlayout_main": {
                        "title_label": {"widget_type": "label", "text": "Main Controls"},
                        "start_button": {"widget_type": "button", "text": "Start", "callback": "start_function"},
                        "stop_button": {"widget_type": "button", "text": "Stop", "callback": "stop_function"}
                    },
                    "qvboxlayout_settings": {
                        "combo_box_example": {
                            "widget_type": "combo_box",
                            "items": ["Option 1", "Option 2", "Option 3"],
                            "callback": "selection_changed",
                            "label_text": "Select an Option:"
                        }
                    }
                }
                widget_instances = self.add_flexible_ribbon(ribbon_config)

            Example 2 - Nested Layouts and Mixed Widgets:
                ribbon_config = {
                    "qhboxlayout_top": {
                        "header_label": {"widget_type": "label", "text": "User Panel"},
                        "qhboxlayout_buttons": {
                            "login_button": {"widget_type": "button", "text": "Login", "callback": "login_user"},
                            "logout_button": {"widget_type": "button", "text": "Logout", "callback": "logout_user"}
                        }
                    },
                    "qvboxlayout_preferences": {
                        "theme_selector": {
                            "widget_type": "combo_box",
                            "items": ["Light", "Dark"],
                            "callback": "change_theme",
                            "label_text": "Theme:"
                        }
                    }
                }
                widget_instances = self.add_flexible_ribbon(ribbon_config)
            """
        for key, value in ribbon_config.items():
            if isinstance(value, dict) and "widget_type" not in value:
                key_lowered = key.lower()
                if key_lowered.startswith("qvboxlayout_"):
                    new_layout = QVBoxLayout()
                    parent_layout.addLayout(new_layout)
                elif key_lowered.startswith("qhboxlayout_"):
                    new_layout = QHBoxLayout()
                    parent_layout.addLayout(new_layout)
                else:
                    print(f"UNKNOWN TYPE OF LAYOUT: {key} in {ribbon_config} SKIPPING...")
                    continue

                self.widgets_container[key] = new_layout
                # Initialize the nested dictionary for this container.
                container_dict[key] = {}
                # Recursively process the children.
                self.add_flexible_ribbon(value, new_layout, container_dict[key])
            else:
                widget_type = value.get("widget_type")
                widget_creators = {
                    "button": lambda v: self.button(v.get("text", "Button"), v.get("callback")),
                    "label": lambda v: self.label(v.get("text", "Label")),
                    "combo_box": lambda v: self.combo_box(v.get("items", []), v.get("callback", None)),
                    "input_box": lambda v: self.input_box(v.get("text", "Enter text")),
                    "table": lambda v: self.table(v.get("rows"), v.get("columns"),
                                                  v.get("data"), v.get("header"))
                }

                if widget_type in widget_creators:
                    print(widget_creators)
                    widget = widget_creators[widget_type](value)
                    parent_layout.addWidget(widget)
                    self.widgets_container[key] = widget
                    container_dict[key] = widget
                else:
                    print(f"UNKNOWN WIDGET TYPE: {widget_type} in {value} SKIPPING...")
        return self.widgets_container

    def find_widget(self, container, key_path):
        """
        Recursively searches for a widget inside a nested dictionary.

        Parameters:
            container (dict): The nested dictionary storing widgets.
            key_path (list): List of keys representing the hierarchical path to the widget.

        Returns:
            QWidget or None: The found widget or None if not found.
        """
        if not key_path:
            return None  # No path provided

        key = key_path[0]

        if key in container:
            if len(key_path) == 1:  # If it's the last key, return the widget
                return container[key]
            elif isinstance(container[key], dict):  # If still nested, continue searching
                return self.find_widget(container[key], key_path[1:])

        return None  # Key not found

    def apply_stylesheet_to_all_layout(self, css_dict):
        stylesheet = ""
        for selector, styles in css_dict.items():
            style_block = f"{selector} {{\n"
            for pseudo, style in styles.items():
                style_block += f"{pseudo} {style}\n"
            style_block += "}\n"
            stylesheet += style_block

        self.setStyleSheet(stylesheet)  # Apply to the whole application

    def clear_widgets(self):
        """
        Clears all widgets and nested layouts from the main layout.
        """

        def recursive_clear(layout):
            while layout.count():
                item = layout.takeAt(0)  # Take the first item in the layout
                widget = item.widget()  # Get the widget from the item
                if widget:
                    widget.deleteLater()  # Schedule the widget for deletion
                else:
                    nested_layout = item.layout()  # Check if the item is a layout
                    if nested_layout:
                        recursive_clear(nested_layout)  # Recursively clear the nested layout


        recursive_clear(self.main_layout)  # Start clearing from the main layout
        self.widgets_container = self.filter_nested_dict(self.widgets_container, "qvboxlayout_central_widget")

    @staticmethod
    def filter_nested_dict(d, key_to_keep):
        if isinstance(d, dict):
            return {key_to_keep: MainWindow.filter_nested_dict(d[key_to_keep], key_to_keep)} if key_to_keep in d else {}
        return d

    def show_message(self, title, message, message_type):
        """Display a dark mode message box with HTML-styled text."""
        msg = QMessageBox()
        message_type = message_type.lower()

        # Configuration mapping for message types.
        config = {
            "warning": {"icon": QMessageBox.Warning, "prefix": "Warning", "color": "#CCCCCC"},
            "error": {"icon": QMessageBox.Critical, "prefix": "Error", "color": "#FF5555"},
            "success": {"icon": QMessageBox.Information, "prefix": "Success", "color": "#55FF55"},
        }.get(message_type, {"icon": QMessageBox.Information, "prefix": "Info", "color": "#CCCCCC"})

        # Apply the configuration.
        msg.setIcon(config["icon"])
        msg.setWindowTitle(f"{config['prefix']}: {title}")
        msg.setText(f"<font color='{config['color']}'>{message}</font>")
        msg.setStandardButtons(QMessageBox.Ok)

        # Set a dark background for the QMessageBox.
        msg.setStyleSheet("QMessageBox { background-color: #2E2E2E; }")

        msg.exec_()

