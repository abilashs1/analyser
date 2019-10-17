import sys
from PySide2.QtWidgets import (QPushButton, QDialog, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout, QWidget,
                             QHBoxLayout, QFrame, QLabel,
                             QApplication, QRadioButton, QButtonGroup)

from PySide2.QtGui import (QPalette, QColor, QFont)
    
def get_white_color():
    backgroundPalette = QPalette()
    backgroundColor = QColor(255, 255, 255)
    backgroundPalette.setColor(QPalette.Background, backgroundColor)
    return backgroundPalette

def get_white_color_text():
    backgroundPalette = QPalette()
    backgroundColor = QColor(255, 255, 255)
    backgroundPalette.setColor(QPalette.Foreground, backgroundColor)
    return backgroundPalette


def get_verifone_color():
    backgroundPalette = QPalette()
    backgroundColor = QColor(3, 169, 229)
    backgroundPalette.setColor(QPalette.Background, backgroundColor)
    return backgroundPalette

class SectionExpandButton(QRadioButton):
    """a QPushbutton that can expand or collapse its section
    """
    def __init__(self, item, text = "", group = None, parent = None):
        super().__init__(text, parent)
        self.section = item
        self.clicked.connect(self.on_clicked)
        self.setStyleSheet("background-color: rgba(3, 169, 229, 0)")
        self.setPalette(get_white_color_text())
        self.group = group
        self.setFont(QFont("Times", 18, QFont.Bold))
        
        group.addButton(self)
    def on_clicked(self):
        """toggle expand/collapse of section by clicking
        """
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)
            
        for button in self.group.buttons():
            if (button != self):
                button.section.setExpanded(False)

class CollapsibleWidget(QWidget):
    """a dialog to which collapsible sections can be added;
    subclass and reimplement define_sections() to define sections and
        add them as (title, widget) tuples to self.sections
    """
    def __init__(self):
        super().__init__()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setPalette(get_verifone_color())
        self.setStyleSheet("background-color: rgba(3, 169, 229, 0)")
        layout = QVBoxLayout()
        self.buttonGroup = QButtonGroup()
        layout.addWidget(self.tree)        
        self.setLayout(layout)
        self.tree.setIndentation(0)
        self.setPalette(get_verifone_color())
        self.sections = []
        self.setFixedWidth(500)
    
    def get_tree(self):
        return self.tree
            
    def add_sections(self):
        """adds a collapsible sections for every 
        (title, widget) tuple in self.sections
        """
        for (title, widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1, widget)            
            button1.addChild(section1)

    def include_section(self, title, frame):
        """reimplement this to define all your sections
        and add them as (title, widget) tuples to self.sections
        """
        self.sections.append((title, frame))

    def add_button(self, title):
        """creates a QTreeWidgetItem containing a button 
        to expand or collapse its section
        """
        item = QTreeWidgetItem()
        item.setBackgroundColor(0, QColor(3, 169, 229))
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text = title, group = self.buttonGroup))
        
        return item

    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QTreeWidgetItem(button)
        section.setDisabled(True)
        section.setBackgroundColor(0, QColor(3, 169, 229))
        self.tree.setItemWidget(section, 0, widget)
        return section
