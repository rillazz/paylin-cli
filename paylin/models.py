from dataclasses import dataclass

from .enums import BusinessType, Category, Certification, Revenue, Employees


from dataclasses import dataclass


@dataclass
class Company:
    name: str
    profile_url: str

    business_type: str | None = None
    employee_count: str | None = None
    main_products: str | None = None

    description: str | None = None
    address: str | None = None

    year_established: str | None = None
    management_system_certification: str | None = None
    registered_capital: str | None = None

    export_years: str | None = None
    nearest_port: str | None = None
    average_lead_time: str | None = None

    main_markets: str | None = None
    payment_terms: str | None = None
    incoterms: str | None = None

    factory_size: str | None = None
    production_lines: str | None = None

    odm_available: str | None = None
    oem_available: str | None = None
    rnd_engineers: str | None = None

    relevance_score: int | None = None
    relevance_reason: str | None = None
    import_potential: str | None = None
    flags: str | None = None


@dataclass(slots=True)
class SearchFilters:
    keyword: str
    province: str | None = None
    business_type: BusinessType | None = None
    category: Category | None = None
    certification: Certification | None = None
    revenue: Revenue | None = None
    employees: Employees | None = None
