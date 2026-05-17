import csv

from dataclasses import fields
from pathlib import Path

from .models import Company


class MadeInChinaExporter:
    def __init__(
        self,
        directory: Path,
    ) -> None:
        self.directory = directory

    def export(
        self,
        filename: str,
        companies: list[Company],
    ) -> Path:
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filepath = self.directory / filename

        fieldnames = [field.name for field in fields(Company)]

        rows = [self.serialize_company(company) for company in companies]

        try:
            self.write_csv(
                filepath=filepath,
                fieldnames=fieldnames,
                rows=rows,
            )

        except OSError as e:
            raise RuntimeError(f"Failed to export CSV to '{filepath}'") from e

        return filepath

    def serialize_company(
        self,
        company: Company,
    ) -> dict[str, str | None]:
        return {field.name: getattr(company, field.name) for field in fields(Company)}

    def write_csv(
        self,
        filepath: Path,
        fieldnames: list[str],
        rows: list[dict],
    ) -> None:
        with filepath.open(
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, dialect="excel")

            writer.writeheader()
            writer.writerows(rows)
