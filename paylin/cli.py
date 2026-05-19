import typer

from pathlib import Path
from typing import Annotated
from rich.console import Console

from paylin.analyzer import Analyzer


from .enums import BusinessType, Certification, Category, Revenue, Employees
from .exporter import MadeInChinaExporter
from .client import MadeInChinaClient
from .models import SearchFilters
from .utils import construct_filename

app = typer.Typer()
console = Console()


@app.command()
def main(
    query: str,
    okved: str,
    api_key: str,
    proxy: Annotated[
        str | None,
        typer.Option(
            help="HTTP/HTTPS/SOCKS proxy URL. Example: http://user:pass@host:port"
        ),
    ] = None,
    province: str | None = None,
    business_type: BusinessType | None = None,
    certification: Certification | None = None,
    category: Category | None = None,
    revenue: Revenue | None = None,
    employees: Employees | None = None,
    min_score: Annotated[int, typer.Option(min=1, max=10)] = 7,
    limit: Annotated[int, typer.Option(min=1)] = 50,
    output_dir: Annotated[Path, typer.Option()] = Path("./output/"),
):
    """made-in-china parser"""
    console.print("Paylin-cli", highlight=False)

    filters = SearchFilters(
        keyword=query,
        business_type=business_type,
        certification=certification,
        category=category,
        province=province,
        revenue=revenue,
        employees=employees,
    )
    try:
        with MadeInChinaClient(proxy=proxy) as client:
            console.print("Fetching companies...")
            companies = client.get_companies(filters=filters, limit=limit)
            console.print(f"Companies ({len(companies)}) fetched")
            console.print("Getting company details...")
            companies = client.enrich_companies(companies)
            console.print("Details fetched")

            console.print("Exporting raw csv file...")

            filename = construct_filename(query=query, filtered=False)
            exporter = MadeInChinaExporter(directory=output_dir)

            filepath = exporter.export(filename, companies)

            console.print(
                f"[green]Unfiltered results ({len(companies)}) were written in file {filepath}"
            )

            console.print("Running AI analysis...")
            analyzer = Analyzer(token=api_key, okved_code=okved)
            companies = analyzer.analyze_companies(companies)
            filtered_filepath = exporter.export("filtered_" + filename, companies)
            console.print(
                f"[green]Filtered results ({len(companies)}) were written in file {filtered_filepath}"
            )
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

        raise typer.Exit(1)


if __name__ == "__main__":
    app()
