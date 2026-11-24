/* JavaScript 영역: 사용자 이벤트 처리 및 중복 신청 방지 로직 */
function applyCourse(buttonElement) {
    const confirmApply = confirm("수강을 신청하시겠습니까?\n\n※ 국민내일배움카드 발급 대상자인지 미리 확인 부탁드립니다.");
    
    if (confirmApply) {
        alert("성공적으로 수강 신청이 완료되었습니다.\n담당자가 곧 서류 심사 및 면접 관련 안내를 위해 연락드릴 예정입니다.");
        
        // 페이지 내의 모든 신청 버튼을 가져옵니다.
        const allButtons = document.querySelectorAll('.apply-btn');
        
        allButtons.forEach(btn => {
            btn.disabled = true; // 모든 버튼 비활성화
            
            if (btn === buttonElement) {
                // 사용자가 클릭한 버튼
                btn.innerText = '신청 완료됨';
                btn.style.backgroundColor = '#28a745'; 
                btn.style.color = '#ffffff';
            } else {
                // 선택하지 않은 다른 과정의 버튼
                btn.innerText = '중복 신청 불가';
                btn.style.backgroundColor = '#e0e0e0';
                btn.style.color = '#888888';
            }
        });
    } else {
        alert("신청이 취소되었습니다.");
    }
}