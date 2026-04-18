document.addEventListener("DOMContentLoaded", function () {
  // 페이지가 로드되면 실행
  const flashMessages = document.querySelectorAll(".flash-message");

  flashMessages.forEach(function (msg) {
    // 처음에는 숨겨져 있으니, 0초 후에 opacity를 1로 바꾸면서 표시
    setTimeout(function () {
      msg.style.visibility = "visible"; // 메시지가 보이도록 설정
      msg.style.opacity = "1"; // opacity를 1로 변경하여 보이게 함
    }, 100); // 나타나는 시간 0.1초 뒤로 변경 (즉시 나타남)

    // 2초 후에 사라지게 설정
    setTimeout(() => {
      msg.style.opacity = "0"; // opacity를 0으로 바꾸어서 사라짐
      setTimeout(() => msg.remove(), 500); // 완전히 사라진 후 삭제
    }, 2000); // 2초 후에 사라지기 시작
  });
});
