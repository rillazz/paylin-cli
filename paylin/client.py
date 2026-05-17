import requests
import random
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .constants import USER_AGENTS
from .mappings import (
    BUSINESS_TYPE_CODES,
    CATEGORY_CODES,
    CERTIFICATION_CODES,
    EMPLOYEE_CODES,
    REVENUE_CODES,
)
from .models import Company, SearchFilters
from .utils import collapse_spaces


class MadeInChinaClient:
    BASE_URL = "https://ru.made-in-china.com/company-search"

    DETAIL_FIELD_MAPPINGS = {
        "Тип Бизнеса": "business_type",
        "Основные Товары": "main_products",
        "Количество Работников": "employee_count",
        "Адрес": "address",
        "Год Основания": "year_established",
        "Сертификация Системы Менеджмента": "management_system_certification",
        "Зарегистрированный Капитал": "registered_capital",
        "Год Экспорта": "export_years",
        "Ближайший Порт": "nearest_port",
        "Среднее Время Выполнения Заказа": "average_lead_time",
        "Основные Рынки": "main_markets",
        "Условия Платежа": "payment_terms",
        "Международные Коммерческие Условия(Инкотермс)": "incoterms",
        "Площадь Завода": "factory_size",
        "Производственные линии": "production_lines",
        "Доступна услуга ODM": "odm_available",
        "Доступно обслуживание OEM": "oem_available",
        "R&D Инженеры": "rnd_engineers",
    }

    def __init__(
        self,
        timeout: int = 20,
        retries: int = 3,
        proxy: str | None = None,
    ) -> None:
        self.timeout = timeout

        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
        )

        self.session.mount(
            "https://",
            adapter,
        )

        self.session.mount(
            "http://",
            adapter,
        )

        self.session.headers.update(
            {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

        self.session.cookies.update(
            {
                "p_s2": "50_",
            }
        )

        if proxy:
            parsed = urlparse(proxy)

            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid proxy URL: {proxy}")

            self.session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                }
            )

    def get_companies(
        self,
        filters: SearchFilters,
        limit: int,
    ) -> list[Company]:
        companies: list[Company] = []

        page = 1

        while len(companies) < limit:
            response_text = self.fetch_page(
                filters=filters,
                page=page,
            )

            if not response_text:
                break

            parsed_companies = self.parse_companies(
                response_text,
            )

            if not parsed_companies:
                break

            companies.extend(
                parsed_companies,
            )

            page += 1

        return companies[:limit]

    def fetch_page(
        self,
        filters: SearchFilters,
        page: int,
    ) -> str | None:
        url = self.construct_url(
            filters=filters,
            page=page,
        )

        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.text

        except requests.RequestException:
            return None

    def parse_companies(
        self,
        html: str,
    ) -> list[Company]:
        soup = BeautifulSoup(
            html,
            "lxml",
        )

        company_tags = soup.select(
            "div.list-node",
        )

        companies: list[Company] = []

        for company_tag in company_tags:
            try:
                company = self.parse_company(
                    company_tag,
                )

                if company:
                    companies.append(
                        company,
                    )

            except Exception:
                continue

        return companies

    def parse_company(
        self,
        company_tag: Tag,
    ) -> Company | None:
        company_link_tag = company_tag.select_one(
            "a.company-name-link",
        )

        if not company_link_tag:
            return None

        intro_tags = company_tag.select(
            "div.company-intro > div > span",
        )

        auth_tags = company_tag.select(
            "span.auth-block.basic-ability",
        )

        company_type_tag = intro_tags[0] if len(intro_tags) > 0 else None

        products_tag = intro_tags[1] if len(intro_tags) > 1 else None

        area_tag = auth_tags[0] if len(auth_tags) > 0 else None

        employees_tag = auth_tags[1] if len(auth_tags) > 1 else None

        name = company_link_tag.get(
            "title",
        )

        profile_url = company_link_tag.get(
            "href",
        )

        if not name or not profile_url:
            return None

        business_type = (
            company_type_tag.get(
                "title",
                "",
            )
            if company_type_tag
            else ""
        )

        products = (
            collapse_spaces(
                products_tag.get_text(
                    " ",
                    strip=True,
                ).replace(",", ";")
            )
            if products_tag
            else None
        )

        area = (
            collapse_spaces(
                area_tag.get_text(
                    " ",
                    strip=True,
                )
            )
            if area_tag
            else None
        )

        employees = (
            collapse_spaces(
                employees_tag.get_text(
                    " ",
                    strip=True,
                )
            )
            if employees_tag
            else None
        )

        return Company(
            name=collapse_spaces(str(name)),
            profile_url=str(profile_url),
            business_type=collapse_spaces(str(business_type).replace(",", ";")),
        )

    def construct_url(
        self,
        filters: SearchFilters,
        page: int,
    ) -> str:
        parts: list[str] = [f"{self.BASE_URL}/{quote(filters.keyword)}/C1"]

        if filters.business_type:
            parts.append(f"--BT_{BUSINESS_TYPE_CODES[filters.business_type]}")

        if filters.category:
            parts.append(f"--CD_{CATEGORY_CODES[filters.category]}-Catalog")

        if filters.certification:
            parts.append(f"--MC_{CERTIFICATION_CODES[filters.certification]}")

        if filters.province:
            parts.append(f"--CP_{filters.province}")

        if filters.revenue:
            parts.append(f"--AR_{REVENUE_CODES[filters.revenue]}")

        if filters.employees:
            parts.append(f"--NE_{EMPLOYEE_CODES[filters.employees]}")

        parts.append(f"/{page}.html")

        return "".join(parts)

    def fetch_company_details(
        self,
        company: Company,
    ) -> Company:
        detail_url = f"{company.profile_url}/company_info.html"

        try:
            response = self.session.get(
                detail_url,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.RequestException:
            return company

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

        description_tag = soup.select_one(
            ".intro-cnt.J-txt-cnt",
        )

        if description_tag:
            company.description = collapse_spaces(
                description_tag.get_text(
                    " ",
                    strip=True,
                )
            )

        profile_data = self.extract_profile_data(soup)

        for label, attribute in self.DETAIL_FIELD_MAPPINGS.items():

            setattr(company, attribute, profile_data.get(label))

        time.sleep(random.uniform(0.3, 1.0))

        return company

    def extract_profile_data(
        self,
        soup: BeautifulSoup,
    ) -> dict[str, str]:
        data: dict[str, str] = {}

        items = soup.select("div.sr-comProfile-item")

        for item in items:
            label_tag = item.select_one(".sr-comProfile-label")
            value_tag = item.select_one(".sr-comProfile-fields")

            if not label_tag or not value_tag:
                continue

            key = collapse_spaces(
                label_tag.get_text(
                    " ",
                    strip=True,
                )
                .replace(":", "")
                .replace("✓", "")
            )

            value = collapse_spaces(
                value_tag.get_text(
                    " ",
                    strip=True,
                )
            )

            if not key or not value:
                continue

            data[key] = value

        return data

    def enrich_companies(
        self,
        companies: list[Company],
        workers: int = 5,
    ) -> list[Company]:
        with ThreadPoolExecutor(
            max_workers=workers,
        ) as executor:
            futures = [
                executor.submit(
                    self.fetch_company_details,
                    company,
                )
                for company in companies
            ]

            for future in as_completed(
                futures,
            ):
                try:
                    future.result()

                except Exception:
                    continue

        return companies

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        self.close()
