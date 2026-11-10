package melon_02;

import java.util.ArrayList;
import java.util.List;

/**
 * [Melon 클래스 - 음원 스트리밍 서비스 플랫폼]
 * 
 * 💡 핵심 개념:
 * 1. 컬렉션 프레임워크 (List & ArrayList):
 *    - 고정 크기의 일반 배열(Song[]) 대신, 필요할 때마다 곡을 무제한으로 담을 수 있는 '동적 리스트'를 사용합니다.
 *    - songs.add(곡): 곡 추가
 *    - songs.get(순번): 순번(인덱스)에 위치한 곡 가져오기
 *    - songs.size(): 현재 저장된 총 곡 수
 * 2. 방어적 프로그래밍(Defensive Coding):
 *    - 사용자가 저장된 곡 수보다 더 많은 수를 출력해달라고 요청해도,
 *      프로그램이 에러(IndexOutOfBoundsException)로 튕기지 않도록 안전장치를 두는 기법입니다.
 */
public class Melon {
	
	// ==========================================
	// 1. 필드(Field) : 멜론 서비스가 관리하는 데이터
	// ==========================================
//	Song[] songs = new Song[0]; // 일반 배열: 크기가 고정되어 데이터 추가/삭제가 매우 불편함
	List<Song> songs = new ArrayList<Song>(); // List: 크기가 자유자재로 늘어나는 편리한 리스트 바구니
	
	// ==========================================
	// 2. 생성자(Constructor) : 기본 생성자 사용 (별도 정의 없음)
	// ==========================================
	
	
	// ==========================================
	// 3. 메소드(Method) : 멜론의 주요 기능
	// ==========================================
	
	/**
	 * 목록 보여주기 
	 * 메소드명 : showList
	 * 전달인자 : int count 보여줄 개수
	 * 리턴타입 : void (반환값 없음)
	 * 
	 * songs의 내용 보여줄 count 만큼만 출력하기 
	 */
	void showList(int count) {
		// [방어 코딩 (Defensive Coding)]
		// 만약 보관 중인 곡이 2곡뿐인데 count로 10개를 보여달라고 하면
		// 존재하지 않는 인덱스를 조회하여 에러가 발생하므로,
		// count 값을 현재 저장된 최대 크기(songs.size())로 제한해줍니다.
		if (count > songs.size()) {
			count = songs.size();
		}
		
		// 0번 곡부터 요청한 count 개수까지만 반복하며 화면에 출력
		for (int i=0; i<count; i++) {
			Song song = songs.get(i); // i번째 인덱스의 곡 객체를 하나 꺼냄
			System.out.println("title :" + song.title);
			System.out.println("singer :" + song.singer);
		}
	}
	
	/**
	 * 곡 추가 
	 * 받은 Song을 songs에 추가
	 * 단, 제목과 가수가 같으면 추가하지 않는다. 
	 * 메소드명 : addSong
	 * 전달인자 : Song (추가하려는 음악 객체)
	 * 리턴타입 : 추가 성공 여부 (true: 성공, false: 실패)
	 */
	boolean addSong(Song song) {
		boolean result = false; // 추가 성공 여부를 저장할 변수 (기본값: 실패)
		
		// [케이스 1] 멜론 보관함이 완전히 비어있는 경우 (곡 개수가 0일 때)
		if(this.songs.size() == 0) {
			songs.add(song); // 중복 검사할 대상이 없으므로 바로 추가
			result = true;   // 성공으로 변경
		}else{
			// [케이스 2] 이미 보관함에 다른 곡들이 들어있는 경우
			// 기존 곡들을 하나씩 꺼내어 새로 들어온 song과 중복인지 검사
			for(int i=0; i<this.songs.size(); i++) {
				Song s = songs.get(i);
				
				// 제목(title)과 가수(singer)가 모두 일치하지 않는 경우(! 연산자)에만 추가
				if(!(s.title.equals(song.title) && s.singer.equals(song.singer))) {
					
					songs.add(song); // 목록에 새 곡 추가
					result = true;   // 성공으로 변경
				}
			}
		
		}
		
		return result; // 최종 성공/실패 여부를 호출한 곳으로 반환
	}
	
	/**
	 * 전곡 재생 기능
	 * 현재 멜론에 담겨있는 모든 곡의 play() 메서드를 순서대로 실행합니다.
	 */
	void playAll() {
		// 0번부터 마지막 곡(songs.size() - 1)까지 순회
		for (int i=0; i<this.songs.size(); i++) {
			songs.get(i).play(); // 각 Song 객체의 재생 메서드 호출
		}
	}
	
}
