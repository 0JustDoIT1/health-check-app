BASE_SCORE=100

GRADE_TEXT = {
    "A": {
        "label": "매우 건강",
        "texts": [
            "전반적으로 매우 건강한 상태입니다.",
            "현재 건강 지표가 매우 안정적입니다.",
            "추가 관리 없이도 양호한 상태를 유지하고 있습니다."
        ]
    },
    "B": {
        "label": "양호",
        "texts": [
            "전반적으로 양호한 건강 상태입니다.",
            "일부 항목에서 경미한 주의가 필요합니다.",
            "생활습관 관리 시 더욱 좋은 상태를 유지할 수 있습니다."
        ]
    },
    "C": {
        "label": "주의",
        "texts": [
            "건강 지표 일부에서 주의가 필요합니다.",
            "생활습관 개선이 권장됩니다.",
            "정기적인 관리가 필요한 상태입니다."
        ]
    },
    "D": {
        "label": "위험",
        "texts": [
            "여러 지표에서 이상 소견이 확인됩니다.",
            "건강 관리가 적극적으로 필요합니다.",
            "생활습관 개선 및 추가 검사가 권장됩니다."
        ]
    },
    "E": {
        "label": "고위험",
        "texts": [
            "건강 상태에 대한 적극적인 관리가 필요합니다.",
            "여러 항목에서 이상 소견이 확인됩니다.",
            "전문의 상담 및 정밀 검사가 권장됩니다."
        ]
    }
}

CATEGORY_TEXT = {
    "LIVER": "간 기능",
    "KIDNEY": "신장 기능",
    "CARDIO": "혈압",
    "METABOLIC": "신진 대사",
    "GLUCOSE": "혈당",
    "BLOOD": "혈액",
    "SENSORY": "감각 기능",
    "SCREENING": "영상·구강검진"
}

CATEGORY_REPORT = {
    "LIVER": {
        "normal": "간 기능 수치가 전반적으로 정상 범위입니다.",
        "mild": "간 효소 수치가 경미하게 상승하여 생활습관 관리가 필요합니다.",
        "moderate": "간 효소 수치 상승이 지속적으로 관찰되어 간 기능 저하가 의심됩니다.",
        "severe": "간 기능 수치가 크게 상승하여 정밀 검사가 필요합니다."
    },

    "KIDNEY": {
        "normal": "신장 기능 수치가 안정적으로 유지되고 있습니다.",
        "mild": "신장 기능 경미한 저하 또는 초기 단백뇨 소견이 있습니다.",
        "moderate": "신장 기능 저하가 의심되며 추가 검사가 필요합니다.",
        "severe": "신장 기능 저하가 뚜렷하게 관찰됩니다."
    },

    "CARDIO": {
        "normal": "혈압이 정상 범위로 유지되고 있습니다.",
        "mild": "혈압이 경계 수준으로 관리가 필요합니다.",
        "moderate": "혈압 상승이 지속되어 고혈압 위험이 있습니다.",
        "severe": "고혈압 소견이 확인되어 적극적인 치료가 필요합니다."
    },

    "METABOLIC": {
        "normal": "체성분 지표가 정상 범위입니다.",
        "mild": "체중 또는 허리둘레가 경계 수준입니다.",
        "moderate": "비만 관련 지표가 개선이 필요한 상태입니다.",
        "severe": "비만으로 인한 건강 위험이 높은 상태입니다."
    },

    "GLUCOSE": {
        "normal": "공복혈당이 정상 범위입니다.",
        "mild": "혈당이 경계 수준으로 관리가 필요합니다.",
        "moderate": "당뇨 전단계 가능성이 있습니다.",
        "severe": "당뇨 범위에 해당하여 관리가 필요합니다."
    },

    "BLOOD": {
        "normal": "혈액 지표가 정상 범위입니다.",
        "mild": "경미한 혈색소 변화가 있습니다.",
        "moderate": "빈혈 또는 혈액 농축 소견이 의심됩니다.",
        "severe": "혈액 이상이 뚜렷하여 추가 평가가 필요합니다."
    },

    "SENSORY": {
        "normal": "시력 및 청력이 정상 범위입니다.",
        "mild": "경미한 시력 또는 청력 저하가 있습니다.",
        "moderate": "감각 기능 저하가 확인됩니다.",
        "severe": "감각 기능 저하가 뚜렷합니다."
    },

    "SCREENING": {
        "normal": "영상 및 검진 결과에서 이상 소견이 없습니다.",
        "mild": "경미한 이상 소견이 관찰됩니다.",
        "moderate": "추적 관찰이 필요한 이상 소견입니다.",
        "severe": "정밀 검사가 필요한 이상 소견입니다."
    }
}

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