const express = require("express");
const multer = require("multer");
const cors = require("cors");
const vision = require("@google-cloud/vision");
const dotenv = require("dotenv");
const fs = require("fs");
const path = require("path");

dotenv.config();

console.log("=== 지금 실행된 server.js는 health-ocr/server.js 입니다 ===");

const app = express();
app.use(cors());
app.use(express.json());

// 업로드 폴더 생성
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// multer 설정
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({ storage });

// Google Vision
const client = new vision.ImageAnnotatorClient({
  keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
});


// 숫자 하나 추출
function extractAfterKeyword(text, keyword) {
  const idx = text.indexOf(keyword);
  if (idx === -1) return "";

  const slice = text.slice(idx, idx + 120);
  const match = slice.match(/[\d.]+/);
  return match ? match[0] : "";
}


// 숫자 2개 (1.0 / 1.0 같은 것)
function extractPairAfterKeyword(text, keyword) {
  const idx = text.indexOf(keyword);
  if (idx === -1) return ["", ""];

  const slice = text.slice(idx, idx + 120);

  let match = slice.match(/([\d.]+)\s*\/\s*([\d.]+)/);
  if (match) return [match[1], match[2]];

  // 붙어있는 경우 (154.445.3)
  match = slice.match(/(\d+\.\d+)(\d+\.\d+)/);
  if (match) return [match[1], match[2]];

  return ["", ""];
}


// 키워드 앞뒤로 찾아서 혈압 같은 것 추출
function extractPairAroundKeyword(text, keyword) {
  const idx = text.indexOf(keyword);
  if (idx === -1) return ["", ""];

  const start = Math.max(0, idx - 80);
  const end = Math.min(text.length, idx + 80);
  const slice = text.slice(start, end);

  const match = slice.match(/([\d.]+)\s*\/\s*([\d.]+)/);
  return match ? [match[1], match[2]] : ["", ""];
}

// 핵심 파싱 함수
function parseHealthCheckText(text) {
  const t = text.replace(/\\n/g, "\n");

  // 키 / 몸무게
  let height = "";
  let weight = "";

  const hwMatch = t.match(/(\d{3}\.\d)(\d{2}\.\d)/);
  if (hwMatch) {
    height = hwMatch[1];
    weight = hwMatch[2];
  }

  // BMI
  let BMI = "";
  const bmiMatch = t.match(/체질량지수[^\d]*(\d+\.\d+)/);
  if (bmiMatch) {
    BMI = bmiMatch[1];
  }
  // 허리둘레
  let waist = "";
  const waistSection = t.split("허리둘레")[1]?.split("시각이상")[0] || "";
  const waistNumbers = waistSection.match(/\d+\.\d+/g) || [];
  if (waistNumbers.length > 0) {
    waist = waistNumbers[waistNumbers.length - 1];
  }
  // 시력
  const [vision_left, vision_right] = extractPairAfterKeyword(t, "시력");

  // 청력
  const [hearing_left_raw, hearing_right_raw] = extractPairAfterKeyword(t, "청력");

  // 혈압
  let systolic_bp = "";
  let diastolic_bp = "";

  const bpMatch = t.match(/(\d{2,3})\s*\/\s*(\d{2,3})\s*mmHg/);
  if (bpMatch) {
    systolic_bp = bpMatch[1];
    diastolic_bp = bpMatch[2];
  }

  return {
    age: "",
    gender: "",

    height,
    weight,
    BMI,
    waist,

    vision_left,
    vision_right,

    hearing_left: hearing_left_raw === "1" ? "정상" : hearing_left_raw,
    hearing_right: hearing_right_raw === "1" ? "정상" : hearing_right_raw,

    systolic_bp,
    diastolic_bp,

    hemoglobin: extractAfterKeyword(t, "혈색소"),
    fasting_glucose: extractAfterKeyword(t, "공복혈당"),
    creatinine: extractAfterKeyword(t, "혈청크레아티닌"),
    eGFR: extractAfterKeyword(t, "신사구체여과율"),

    AST: extractAfterKeyword(t, "AST"),
    ALT: extractAfterKeyword(t, "ALT"),
    rGTP:
      extractAfterKeyword(t, "감마지티피") ||
      extractAfterKeyword(t, "X-GTP"),

    urine_protein: t.includes("요단백") && t.includes("정상") ? "음성" : "",
    xray: t.includes("흉부촬영") && t.includes("정상") ? "음성" : "",

    dental_exam: "",
    score: "",
    grade: "",
  };
}


// 서버 체크
app.get("/", (req, res) => {
  res.send("OCR server is running");
});


// OCR API
app.post("/ocr", upload.single("image"), async (req, res) => {
  try {
    console.log("=== /ocr 요청 들어옴 ===");

    if (!req.file) {
      return res.status(400).json({ error: "이미지 파일이 없습니다." });
    }

    const filePath = req.file.path;

    const [result] = await client.documentTextDetection(filePath);
    const text = result.fullTextAnnotation?.text || "";

    const parsedData = parseHealthCheckText(text);

    console.log("parsedData:", parsedData);

    res.json({
      success: true,
      text,
      parsedData,
    });

  } catch (error) {
    console.error("OCR 오류:", error);
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});


// 서버 실행
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
