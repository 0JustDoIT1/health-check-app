document.addEventListener("DOMContentLoaded", function () {
  const ocrBtn = document.getElementById("ocrBtn");
  const ocrFile = document.getElementById("ocrFile");
  const form = document.querySelector("form");
  const fileNameEl = document.getElementById("ocrFileName");
  const statusEl = document.getElementById("ocrStatus");
  const fileSelectBtn = document.getElementById("fileSelectBtn");

  if (
    !ocrBtn ||
    !ocrFile ||
    !form ||
    !fileNameEl ||
    !statusEl ||
    !fileSelectBtn
  )
    return;

  ocrFile.addEventListener("change", function () {
    if (ocrFile.files && ocrFile.files.length > 0) {
      fileNameEl.textContent = `선택된 파일: ${ocrFile.files[0].name}`;
      statusEl.textContent = "";
    } else {
      fileNameEl.textContent = "선택된 파일 없음";
      statusEl.textContent = "";
    }
  });

  fileSelectBtn.addEventListener("click", function () {
    ocrFile.click();
  });

  ocrBtn.addEventListener("click", async function () {
    const file = ocrFile.files[0];
    if (!file) {
      alert("검진표 파일을 선택하세요.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    const originalText = ocrBtn.textContent;
    ocrBtn.disabled = true;
    ocrBtn.textContent = "처리중...";
    statusEl.textContent = "검진표를 확인하고 항목을 불러오는 중입니다.";

    try {
      const response = await fetch("http://localhost:4000/ocr", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!data.success) {
        alert("자동입력 실패: " + (data.error || "알 수 없는 오류"));
        statusEl.textContent = "";
        return;
      }

      const parsed = data.parsedData || {};

      setValue("height", parsed.height);
      setValue("weight", parsed.weight);
      setValue("BMI", parsed.BMI);
      setValue("waist", parsed.waist);
      setValue("vision_left", parsed.vision_left);
      setValue("vision_right", parsed.vision_right);
      setValue("systolic_bp", parsed.systolic_bp);
      setValue("diastolic_bp", parsed.diastolic_bp);
      setValue("hemoglobin", parsed.hemoglobin);
      setValue("fasting_glucose", parsed.fasting_glucose);
      setValue("creatinine", parsed.creatinine);
      setValue("eGFR", parsed.eGFR);
      setValue("AST", parsed.AST);
      setValue("ALT", parsed.ALT);
      setValue("rGTP", parsed.rGTP);

      setSelect("hearing_left", parsed.hearing_left, {
        정상: "0",
        의심: "1",
        이상: "1",
      });

      setSelect("hearing_right", parsed.hearing_right, {
        정상: "0",
        의심: "1",
        이상: "1",
      });

      setSelect("urine_protein", parsed.urine_protein, {
        음성: "0",
        의심: "1",
        양성: "2",
      });

      setSelect("xray", parsed.xray, {
        음성: "0",
        양성: "1",
      });

      setSelect("dental_exam", parsed.dental_exam, {
        정상: "0",
        이상: "1",
        음성: "0",
        양성: "1",
      });

      statusEl.textContent =
        "자동 입력이 완료되었습니다. 저장 전 입력값을 다시 확인하고 필요한 경우 수정해주세요.";

      ocrFile.value = "";
      fileNameEl.textContent = "선택된 파일 없음";

      alert("검진표 정보가 자동 입력되었습니다.");
    } catch (error) {
      console.error(error);
      alert("자동입력 요청 중 오류가 발생했습니다.");
      statusEl.textContent = "";
    } finally {
      ocrBtn.disabled = false;
      ocrBtn.textContent = originalText;
    }
  });

  form.addEventListener("submit", function () {
    ocrFile.value = "";
    fileNameEl.textContent = "선택된 파일 없음";
    statusEl.textContent = "";
  });

  function setValue(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = value ?? "";
  }

  function setSelect(id, textValue, mapping) {
    const el = document.getElementById(id);
    if (!el) return;
    const mapped = mapping[textValue];
    if (mapped !== undefined) {
      el.value = mapped;
    }
  }
});
