import sys
from pathlib import Path


# пишет отчет о сеансах в report.txt
# старые строки читаем из файла и дописываем новую, потом перезаписываем таблицу
class ReportWriter:
    HEADER = ("login", "time_in", "time_out")

    @staticmethod
    def app_dir():
        # если запущено из exe, то сохраняем рядом с exe
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parent.parent

    @staticmethod
    def default_path():
        return ReportWriter.app_dir() / "report.txt"

    @staticmethod
    def load_rows(path):
        if not path.exists():
            return []
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("|-"):
                continue
            cells = tuple(c.strip() for c in line.strip("|").split("|"))
            if len(cells) == 3 and cells != ReportWriter.HEADER:
                rows.append(cells)
        return rows

    @staticmethod
    def make_line(cells, widths):
        parts = [cell.ljust(w) for cell, w in zip(cells, widths)]
        return "| " + " | ".join(parts) + " |"

    @staticmethod
    def render(rows):
        all_rows = [ReportWriter.HEADER] + rows
        widths = []
        for i in range(3):
            widths.append(max(len(row[i]) for row in all_rows))

        header = ReportWriter.make_line(ReportWriter.HEADER, widths)
        border = "+" + "-" * (len(header) - 2) + "+"
        separator = "|" + "|".join("-" * (w + 2) for w in widths) + "|"

        lines = [border, header, separator]
        for row in rows:
            lines.append(ReportWriter.make_line(row, widths))
        lines.append(border)
        return "\n".join(lines) + "\n"

    @staticmethod
    def save(session, path=None):
        if path is None:
            path = ReportWriter.default_path()
        path = Path(path)
        if not session.is_closed:
            session.close()
        rows = ReportWriter.load_rows(path)
        rows.append(session.as_row())
        path.write_text(ReportWriter.render(rows), encoding="utf-8")
        return path
