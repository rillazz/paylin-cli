from .enums import Certification, BusinessType, Revenue, Employees, Category

CERTIFICATION_CODES = {
    Certification.ISO_9001: 10,
    Certification.ISO_14001: 6,
    Certification.ISO_9001_2015: -5,
    Certification.ISO_9000: 9,
    Certification.GMP: 26,
    Certification.OTHER: -4,
    Certification.BSCI: 20,
    Certification.ISO_20000: 8,
    Certification.ISO_14000: 5,
    Certification.ISO_45001_2018: 100375,
    Certification.QC_080004: 12,
    Certification.ISO_14064: 7,
    Certification.HSE: 4,
    Certification.OHSAS_OHSMS_18005: 11,
    Certification.IATF16949: 31,
    Certification.HACCP: 27,
    Certification.ISO_22000: 35,
    Certification.BRC: 19,
    Certification.FSC: 40,
    Certification.IFS: 34,
    Certification.ASME: 23,
    Certification.SEDEX: 21,
    Certification.GAP: 33,
    Certification.SA_8004: 13,
    Certification.SHE_AUDITS: 18,
    Certification.ISO_10012: 41,
    Certification.QHSE: 17,
    Certification.EICC: 3,
    Certification.WRAP: 22,
    Certification.ANSI_ESD: 1,
    Certification.QSR: 29,
    Certification.HQE: 15,
    Certification.ISO_17025: 42,
    Certification.ISO_50001: 37,
    Certification.ISO_13485: 28,
    Certification.PAS_28000: 30,
    Certification.AIB: 32,
    Certification.BREEAM: 14,
    Certification.ISO_29001: 36,
    Certification.LEED: 16,
    Certification.BS_25999_2: 2,
    Certification.ISO_14001_2015: -6,
}

BUSINESS_TYPE_CODES = {
    BusinessType.MANUFACTURER: 1,
    BusinessType.TRADER: 2,
    BusinessType.GROUP: 4,
    BusinessType.SOHO: 11,
    BusinessType.OTHER: 8,
}

REVENUE_CODES = {
    Revenue.UNDER_1M: 1,
    Revenue.FROM_1M_TO_2_5M: 2,
    Revenue.FROM_2_5M_TO_5M: 3,
    Revenue.FROM_5M_TO_10M: 4,
    Revenue.FROM_10M_TO_50M: 5,
    Revenue.FROM_50M_TO_100M: 6,
    Revenue.MORE_THAN_100M: 7,
}


EMPLOYEE_CODES = {
    Employees.LESS_THAN_5: 1,
    Employees.FROM_5_TO_50: 2,
    Employees.FROM_51_TO_200: 3,
    Employees.FROM_201_TO_500: 4,
    Employees.FROM_501_TO_1000: 5,
    Employees.MORE_THAN_1000: 6,
}

CATEGORY_CODES = {
    Category.MACHINERY: "Manufacturing-Processing-Machinery",
    Category.INDUSTRIAL: "Industrial-Equipment-Components",
    Category.PACKAGING: "Packaging-Printing",
    Category.AGRICULTURE_FOOD: "Agriculture-Food",
    Category.CHEMICALS: "Chemicals",
    Category.CONSUMER_GOODS: "Light-Industry-Daily-Use",
    Category.TOOLS: "Tools-Hardware",
    Category.HEALTH_MEDICINE: "Health-Medicine",
    Category.ARTS: "Arts-Crafts",
    Category.SERVICE: "Service",
}
