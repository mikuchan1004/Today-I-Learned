package melon_02;

/**
 * [Song 클래스 - 음악 1곡의 정보를 담는 설계도]
 * 
 * 💡 핵심 개념:
 * 1. 클래스(Class)와 객체(Object):
 *    - 클래스는 '음악'이라는 개념을 표현하기 위한 붕어빵 틀(설계도)입니다.
 *    - new Song(...)으로 실제 음악 데이터 1곡(객체/인스턴스)을 찍어냅니다.
 * 2. 접근 제어자(Access Modifier)와 캡슐화(Encapsulation):
 *    - private: 클래스 내부에서만 접근 가능하도록 감춥니다(중요한 데이터인 순위, 좋아요 수를 외부에서 임의 조작 방지).
 *    - default(생략): 같은 패키지(melon_02) 안에서 자유롭게 접근할 수 있습니다.
 */
public class Song {
	// ==========================================
	// 1. 필드(Field) : 음악 1곡이 가지는 고유한 속성(데이터)들
	// ==========================================
	// 제목, 가수명, 앨범명, 순위, 좋아요 수, 앨범아트
	String title;        // 곡 제목 (예: "With", "꿈꾸던 어른이 되었나요?")
	String singer;       // 가수 이름 (예: "리센느", "머무르")
	String album;        // 앨범 이름
	
	// private: 외부에서 마음대로 song.rank = 1; 처럼 조작할 수 없도록 안전하게 숨김(보호)
	private int rank;    // 음원 차트 순위
	private long like;   // 좋아요 수 (숫자가 매우 커질 수 있으므로 long 사용)
	
	String albumArtUrl;  // 앨범 재킷 이미지 파일 경로나 웹 주소
	boolean useYN;       // 음원 서비스 사용 가능 여부 (true: 재생가능, false: 서비스중지)
	
	// ==========================================
	// 2. 생성자(Constructor) : 객체를 처음 만들 때(new) 자동으로 실행되는 초기화 함수
	// ==========================================
	// 제목, 가수
	/**
	 * Song 객체 생성자
	 * @param title  곡 제목
	 * @param singer 가수명
	 * 
	 * 💡 this 키워드:
	 *  - 'this.title'은 이 클래스 자체의 필드 변수를 가리키고,
	 *  - 뒤의 'title'은 매개변수로 외부에서 넘겨받은 값을 뜻합니다.
	 */
	public Song(String title, String singer) {
		// 필수 정보는 외부에서 직접 전달받아 세팅
		this.title = title;
		this.singer = singer;
		
		// 그 외의 필드들은 기본 초기값으로 안전하게 세팅
		this.album = title;              // 앨범명을 따로 정하지 않으면 기본적으로 곡 제목과 동일하게 설정
		this.rank = -1;                  // 순위가 아직 매겨지지 않았음을 나타내는 임의의 초기값(-1)
		this.like = 0;                   // 좋아요 수는 처음엔 0개부터 시작
		this.albumArtUrl = "기본이미지";  // 앨범 이미지가 없을 때 띄울 기본 이미지 경로
		this.useYN = true;               // 기본적으로 이용 가능한 상태로 설정
	}
	
	// ==========================================
	// 3. 메소드(Method) : 음악 객체가 수행할 수 있는 동작/기능
	// ==========================================
	// 재생, 다운로드
	
	/**
	 * 음악 재생 기능
	 * 콘솔창에 현재 곡이 재생된다는 메시지를 출력합니다.
	 */
	public void play() {
		System.out.println(this.title + "을 재생합니다.");
	}
	
	/**
	 * 음원 다운로드 기능
	 * 다운로드할 수 있는 가상의 주소를 문자열로 만들어 돌려줍니다(return).
	 */
	String download() {
		return this.title + "다운로드 주소";
	}
	
	/**
	 * 좋아요 숫자를 변경한다
	 * - 좋아요를 눌렀을 때 1 증가 
	 * - 좋아요를 뺐을 때 1 감소 
	 *  
	 * @param boolean action
	 * 		true  : 좋아요를 눌렀을 때 (추천 +1)
	 * 		false : 좋아요를 취소했을 때 (추천 -1)
	 * @return long 변경된 최종 좋아요 수
	 * 
	 * 💡 private으로 감춰둔 like 변수를 안전하게 변경할 수 있도록 제공하는 비즈니스 메서드입니다.
	 */
	long updateLike(boolean action) {
		if(action) {
			this.like++;   // action이 true면 1 증가
		}else {
			this.like--;   // action이 false면 1 감소
		}
		
		return this.like;  // 계산이 끝난 최종 좋아요 수를 호출한 곳으로 반환
	}
}
