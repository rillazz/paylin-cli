import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from .models import Company


class CompanyAnalysis(BaseModel):
    relevance_score: int
    reason: str
    import_potential: Literal["high", "medium", "low"]
    flags: list[str]


class Analyzer:
    def __init__(
        self,
        token: str,
        okved_code: str,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-v4-flash",
        workers: int = 5,
    ) -> None:
        self.client = OpenAI(
            api_key=token,
            base_url=base_url,
        )

        self.model = model
        self.workers = workers
        self.okved_code = okved_code

    def analyze_companies(
        self,
        companies: list[Company],
    ) -> list[Company]:
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [
                executor.submit(
                    self.analyze_company,
                    company,
                )
                for company in companies
            ]

            for future in as_completed(futures):
                try:
                    future.result()

                except Exception:
                    continue

        return companies

    def analyze_company(
        self,
        company: Company,
    ) -> Company:
        supplier_data = self.build_supplier_payload(company)

        prompt = self.build_prompt(supplier_data, self.okved_code)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты — аналитик российско-китайской торговли. Оценивай строго и реалистично. Возвращай ТОЛЬКО валидный JSON без пояснений."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            content = response.choices[0].message.content

            if not content:
                return company

            parsed = json.loads(content)

            analysis = CompanyAnalysis.model_validate(parsed)

            company.relevance_score = analysis.relevance_score
            company.relevance_reason = analysis.reason
            company.import_potential = analysis.import_potential
            company.flags = ", ".join(analysis.flags)

        except (
            json.JSONDecodeError,
            ValidationError,
            Exception,
        ):
            pass

        return company

    def build_supplier_payload(
        self,
        company: Company,
    ) -> dict:
        return {
            "name": company.name,
            "business_type": company.business_type,
            "description": company.description,
            "main_products": company.main_products,
            "employee_count": company.employee_count,
            "factory_size": company.factory_size,
            "main_markets": company.main_markets,
            "certifications": (company.management_system_certification),
            "payment_terms": company.payment_terms,
            "incoterms": company.incoterms,
            "export_years": company.export_years,
            "nearest_port": company.nearest_port,
            "oem_available": company.oem_available,
            "odm_available": company.odm_available,
        }

    def build_prompt(self, supplier_data: dict, okved_code: str) -> str:
        return f"""
Оцени релевантность китайской компании как потенциального импортёра российских товаров категории {okved_code}.

Ответ строго в JSON:

{{
    "relevance_score": integer from 1 to 10,
    "reason": "short explanation",
    "import_potential": "high" | "medium" | "low",
    "flags": [
        "possible red flag",
        "another issue"
    ]
}}

Данные:

{json.dumps(supplier_data, ensure_ascii=False, indent=2)}
"""
