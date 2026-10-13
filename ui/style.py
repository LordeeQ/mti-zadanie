from PyQt6.QtGui import QColor, QFont, QPalette


class AppStyle:
    QSS = """
    QWidget { background: #f8fafc; color: #0f172a; }
    QGroupBox {
        border: 1px solid #cbd5e1; border-radius: 8px;
        margin-top: 14px; padding: 10px; font-weight: 600;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }
    QLineEdit {
        background: white; border: 1px solid #cbd5e1; border-radius: 6px;
        padding: 4px 8px; min-height: 22px;
    }
    QLineEdit:focus { border: 1px solid #2563eb; }
    QSpinBox, QComboBox { min-height: 26px; background: white; }
    QPushButton {
        background: #2563eb; color: white; border: none; border-radius: 6px;
        padding: 6px 14px; min-height: 22px; font-weight: 600;
    }
    QPushButton:hover { background: #1d4ed8; }
    QPushButton:disabled { background: #94a3b8; }
    QPushButton[role="danger"] { background: #dc2626; }
    QPushButton[role="danger"]:hover { background: #b91c1c; }
    QPushButton[role="success"] { background: #16a34a; }
    QPushButton[role="success"]:hover { background: #15803d; }
    QTableWidget, QListWidget {
        background: white; alternate-background-color: #f1f5f9;
        color: #0f172a; border: 1px solid #cbd5e1; border-radius: 6px;
        gridline-color: #e2e8f0;
        selection-background-color: #dbeafe; selection-color: #0f172a;
    }
    QHeaderView::section {
        background: #e2e8f0; padding: 6px; border: none; font-weight: 600;
    }
    QTabWidget::pane { border: 1px solid #cbd5e1; border-radius: 6px; top: -1px; }
    QTabBar::tab {
        background: #e2e8f0; padding: 8px 18px; margin-right: 2px;
        border-top-left-radius: 6px; border-top-right-radius: 6px;
    }
    QTabBar::tab:selected { background: white; color: #2563eb; }
    QStatusBar { background: #e2e8f0; }
    QMenuBar { background: #e2e8f0; }
    QMenuBar::item:selected { background: #cbd5e1; }
    """

    # на винде с темной темой qt берет темные цвета из системы,
    # из-за этого строки в таблице были темно-синие. ставим свою светлую палитру
    @staticmethod
    def light_palette():
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor("#f8fafc"))
        p.setColor(QPalette.ColorRole.WindowText, QColor("#0f172a"))
        p.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        p.setColor(QPalette.ColorRole.AlternateBase, QColor("#f1f5f9"))
        p.setColor(QPalette.ColorRole.Text, QColor("#0f172a"))
        p.setColor(QPalette.ColorRole.Button, QColor("#e2e8f0"))
        p.setColor(QPalette.ColorRole.ButtonText, QColor("#0f172a"))
        p.setColor(QPalette.ColorRole.Highlight, QColor("#dbeafe"))
        p.setColor(QPalette.ColorRole.HighlightedText, QColor("#0f172a"))
        p.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        p.setColor(QPalette.ColorRole.ToolTipText, QColor("#0f172a"))
        p.setColor(QPalette.ColorRole.PlaceholderText, QColor("#94a3b8"))
        return p

    @staticmethod
    def apply(app):
        app.setStyle("Fusion")
        app.setPalette(AppStyle.light_palette())
        font = QFont(app.font())
        font.setPointSize(10)
        app.setFont(font)
        app.setStyleSheet(AppStyle.QSS)
