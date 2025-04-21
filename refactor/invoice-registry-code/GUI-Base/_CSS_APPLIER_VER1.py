class TableWidgetCss:
    # TODO: IN FUTURE, UPDATE WITH MORE ROBUST IMPLEMENTATION OF COLORING FOR TABLE WIDGETS..
    pass


class CssManager:
    def __init__(self, general_theme: dict):
        """
        Initializes the CSS manager with a general theme dictionary.
        The general_theme is expected to be a dictionary mapping widget types
        (like "QPushButton", "QLabel", etc.) to another dictionary mapping
        pseudo selectors (or empty string for base) to a CSS snippet.
        """
        self.general_theme = general_theme

    @staticmethod
    def parse_css(css_str: str) -> dict:
        """
        Parse a CSS string into a dictionary mapping property names to values.
        For example:
            "background-color: #444444; color: #fff; padding: 8px;"
        becomes:
            {"background-color": "#444444", "color": "#fff", "padding": "8px"}
        Ignores empty lines and extra whitespace.
        """
        css_dict = {}
        # Remove any surrounding whitespace
        css_str = css_str.strip()
        # Split by semicolons
        for line in css_str.split(";"):
            line = line.strip()
            if not line:
                continue
            # Split by the first colon (to allow colons in values)
            if ":" in line:
                prop, value = line.split(":", 1)
                css_dict[prop.strip()] = value.strip()
        return css_dict

    @staticmethod
    def format_css(css_dict: dict) -> str:
        """
        Convert a dictionary of CSS properties into a CSS string.
        """
        return "\n    ".join(f"{prop}: {value};" for prop, value in css_dict.items())

    def merge_css_rules(self, base_css: str, modifier_css: str) -> str:
        """
        Merge two CSS snippets. The modifier_css values override the base_css values
        for overlapping properties. Returns the merged CSS string.
        """
        base_props = self.parse_css(base_css) if base_css else {}
        mod_props = self.parse_css(modifier_css) if modifier_css else {}
        # Update the base with modifier entries (overriding duplicates)
        merged = {**base_props, **mod_props}
        return self.format_css(merged)

    def get_widget_css(self, widget_type: str, widget_modifier: dict = None) -> str:
        """
        Given a widget type (e.g. "QPushButton") and an optional widget-specific
        dictionary of CSS modifications, return a complete CSS string for that widget.
        Both the general theme and the widget-specific dictionary are expected to have
        keys for pseudo selectors. For example:
            {
                "": "base css here",
                ":hover": "hover css here",
            }
        If widget_modifier is provided, its properties will be merged with the
        corresponding general theme rules.
        """
        # Start with the general theme for this widget type (or an empty dict if not provided)
        general_css_dict = self.general_theme.get(widget_type, {})
        # Prepare a merged dictionary (pseudo selector → css snippet)
        merged_css_dict = {}

        # Get the set of selectors to consider (base: "" and any pseudo selectors)
        selectors = set(general_css_dict.keys())
        if widget_modifier:
            selectors.update(widget_modifier.keys())

        for selector in selectors:
            base_rule = general_css_dict.get(selector, "")
            mod_rule = widget_modifier.get(selector, "") if widget_modifier else ""
            merged_css_dict[selector] = self.merge_css_rules(base_rule, mod_rule)

        # Now construct a full CSS string: for each pseudo selector, create a full selector
        # by appending the pseudo part (if any) to the widget type.
        full_css_lines = []
        for pseudo_selector, css_rules in merged_css_dict.items():
            # Construct selector: e.g., "QPushButton" or "QPushButton:hover"
            full_selector = f"{widget_type}{pseudo_selector}"
            full_css_lines.append(f"{full_selector} {{\n    {css_rules}\n}}")
        return "\n\n".join(full_css_lines)

    def apply_css_to_widget(self, widget, widget_type: str, widget_modifier: dict = None):
        """
        Given a widget instance (that supports setStyleSheet), its type as a string,
        and optionally a widget-specific CSS dictionary, this method builds the complete
        CSS string (merged with the general theme) and applies it to the widget.
        """
        # For other widgets, apply the general CSS
        css_str = self.get_widget_css(widget_type, widget_modifier)
        widget.setStyleSheet(css_str)

    def apply_css_to_all_widgets(self, widget_container: dict, widget_css_overrides: dict = None):
        """
        Recursively traverses a nested dictionary of widget and layout instances and applies
        the CSS to every widget using the provided CSS manager.

        Parameters:
            widget_container (dict): A nested dictionary where the leaves are widget instances.
            widget_css_overrides (dict, optional): A dictionary mapping widget types (like "QPushButton")
                to widget-specific CSS modifications. If provided, these overrides will be merged with
                the general theme for that widget type.
        """
        if widget_css_overrides is None:
            widget_css_overrides = {}

        for key, value in widget_container.items():
            # If the value is itself a dictionary, traverse it recursively.
            if isinstance(value, dict):
                self.apply_css_to_all_widgets(value, widget_css_overrides)
            else:
                # Otherwise, if the value is a widget (i.e. it supports setStyleSheet), apply the CSS.
                if hasattr(value, "setStyleSheet"):
                    # Retrieve the widget type from the class name (e.g., "QPushButton", "QLabel", etc.)
                    widget_type = value.__class__.__name__

                    # Look for a widget-specific override for this type.
                    # You might also use a more sophisticated lookup if you have a unique identifier per widget.
                    override = widget_css_overrides.get(widget_type, None)

                    # Apply the merged CSS to the widget.
                    self.apply_css_to_widget(value, widget_type, override)


# === USAGE EXAMPLE ===
if __name__ == "__main__":
    # General theme definition (singleton)
    general_theme = {
        "QMainWindow": {
            "": "background-color: #2d2d2d;"
        },
        "QPushButton": {
            "": """
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 8px;
                border-radius: 4px;
            """,
            ":hover": "background-color: #555555;"
        },
        "QTableWidget": {
            "": """
                background-color: #2b2b2b;
                gridline-color: #444;
                alternate-background-color: #323232;
                border: 1px solid #555;
                font-family: "Segoe UI", "Arial", sans-serif;
                font-size: 13px;
                color: #ddd;
                selection-background-color: #555;
                selection-color: white;
            """,
            "::item": """
                padding: 6px;
                border: 1px solid #444;
            """,
            "::item:hover": "background-color: #404040;",
            "::item:selected": """
                background-color: #666;
                color: white;
                border: 1px solid #777;
            """,
            "::viewport": "background-color: #222;",
            "QHeaderView::section": """
                background-color: #333;
                color: #ddd;
                padding: 5px;
                border: 1px solid #444;
                font-weight: bold;
            """
        },
        "QLabel": {
            "": """
                color: #ffffff;
                font-size: 14px;
            """
        }
    }

    # Suppose for a particular QPushButton we want to modify its base CSS only:
    widget_specific_css = {
        "": """
            background-color: #000;
            color: #fff;
        """,
        ":hover": "background-color: #777;"
    }

    # Create our CSS manager
    css_manager = CssManager(general_theme)

    # Imagine we have a QPushButton (in a real PyQt/PySide app, this would be an actual widget)
    class FakeWidget:
        def setStyleSheet(self, css):
            print("Applying CSS:")
            print(css)
    button = FakeWidget()

    # Apply merged CSS (general_theme merged with widget_specific_css)
    css_manager.apply_css_to_widget(button, "QPushButton", widget_specific_css)
