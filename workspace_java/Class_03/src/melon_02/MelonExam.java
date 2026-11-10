package melon_02;

/**
 * [MelonExam 실행 클래스 - 실제 음악 객체를 만들고 멜론 서비스를 구동하는 메인 테스트]
 * 
 * 💡 핵심 흐름:
 * 1. Melon 서비스 객체 생성 (스트리밍 플랫폼 준비)
 * 2. Song 객체 생성 (실제 음원 데이터 제작)
 * 3. melon.addSong(...)으로 음원 등록 및 결과 확인
 * 4. melon.showList(...)로 등록된 곡 목록 출력 (방어 코딩 동작 확인: 저장된 건 2곡인데 10곡 출력을 요청해도 에러 없음)
 * 5. melon.playAll(...)로 전곡 순차 재생
 */
public class MelonExam {

	public static void main(String[] args) {
		
		// 1. Melon 플랫폼 객체 생성 (메모리에 멜론 시스템 적재)
		Melon melon = new Melon();
		
		// 2. 첫 번째 곡 객체 생성: 제목 "With", 가수 "리센느"
		Song s1 = new Song("With" , "리센느");
		
		// 멜론에 s1 추가 시도 후 성공 여부(true/false)를 result 변수에 저장
		boolean result = melon.addSong(s1);
		if (result) {
			System.out.println("s1이 정상적으로 추가되었습니다.");
		}else {
			System.out.println("추가되지 않았습니다. 관리자 콜!");
		}
		
		// 3. 두 번째 곡 객체 생성: 제목 "꿈꾸던 어른이 되었나요?", 가수 "머무르"
		Song s2 = new Song("꿈꾸던 어른이 되었나요?" , "머무르");
		melon.addSong(s2); // 멜론 목록에 추가
		
		// 4. 저장된 곡 목록 10개 출력 요청
		// 💡 방어 코딩 검증: 현재 2곡만 등록되어 있으므로, 10개를 요청해도 2곡만 깔끔하게 출력됨 (에러 방지)
		melon.showList(10);
		
		// 5. 보관함에 등록된 모든 곡 일괄 재생
		melon.playAll();

	}

}
