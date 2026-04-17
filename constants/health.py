BASE_SCORE=100

HEALTH_SCHEMA = {
    "name": {
        "label": "이름",
        "type": "base",
    },
     "age": {
        "label": "나이",
        "type": "base",
    },
     "gender": {
        "label": "성별",
        "type": "category",
        "classes": {
            "male": "남성",
            "female": "여성"
        }
    },
    "height": {
        "label": "키",
        "type": "num",
        "unit": "cm"
    },
    "weight": {
        "label": "체중",
        "type": "num",
        "unit": "kg"
    },
    "BMI": {
        "label": "체질량지수",
        "type": "num",
        "unit": "kg/m²"
    },
    "waist": {
        "label": "허리둘레",
        "type": "num",
        "unit": "cm"
    },

    "vision_left": {
        "label": "시력(좌)",
        "type": "num"
    },
    "vision_right": {
        "label": "시력(우)",
        "type": "num"
    },

    "hearing_left": {
        "label": "청력(좌)",
        "type": "category",
        "classes": {
            0: "정상",
            1: "이상"
        }
    },
    "hearing_right": {
        "label": "청력(우)",
        "type": "category",
        "classes": {
            0: "정상",
            1: "이상"
        }
    },

    "systolic_bp": {
        "label": "수축기 혈압",
        "type": "num",
        "unit": "mmHg"
    },
    "diastolic_bp": {
        "label": "이완기 혈압",
        "type": "num",
        "unit": "mmHg"
    },

    "hemoglobin": {
        "label": "혈색소",
        "type": "num",
        "unit": "g/dL"
    },

    "fasting_glucose": {
        "label": "공복혈당",
        "type": "num",
        "unit": "mg/dL"
    },

    "creatinine": {
        "label": "크레아티닌",
        "type": "num",
        "unit": "mg/dL"
    },

    "eGFR": {
        "label": "신사구체여과율",
        "type": "num",
        "unit": "mL/min/1.73m²"
    },

    "urine_protein": {
        "label": "요단백",
        "type": "category",
        "classes": {
            0: "음성",
            1: "의심",
            2: "양성"
        }
    },

    "AST": {
        "label": "AST",
        "type": "num",
        "unit": "IU/L"
    },
    "ALT": {
        "label": "ALT",
        "type": "num",
        "unit": "IU/L"
    },
    "rGTP": {
        "label": "γ-GTP",
        "type": "num",
        "unit": "IU/L"
    },

    "xray": {
        "label": "흉부방사선촬영",
        "type": "category",
        "classes": {
            0: "정상",
            1: "이상"
        }
    },

    "dental_exam": {
        "label": "구강검진",
        "type": "category",
        "classes": {
            0: "정상",
            1: "이상"
        }
    }
}