package webservice_07;

import java.util.ArrayList;
import java.util.List;

/**
 * [서비스 구현 클래스 (Service Implementation)]
 * - 개념: "실제 비즈니스 로직(업무 규칙)을 수행하는 일꾼(요리사)"
 * - 흐름:
 *   1) DAO에게 부탁해 원본 데이터(재료)를 받아옵니다.
 *   2) 우리 회사의 규칙(예: 번호가 3000보다 큰 사원만 필터링)에 맞춰 데이터를 가공/선별합니다.
 *   3) 가공된 결과를 호출한 쪽(Controller)에 전달합니다.
 */
public class EmpServiceImpl implements EmpService {

	@Override 
	public List getEmp() {
		// 1. 데이터 창고 관리자(DAO)를 불러옴
		EmpDAO empDAO = new EmpDAOImpl();
		
		// 2. DB에서 원본 사원 목록 조회 (1111, 2222, 3333, 4444, 5555)
		List list = empDAO.SelectEmp();
		
		// 3. 비즈니스 로직(업무 규칙) 적용: 3000 초과인 사원만 골라 담기
		List result = new ArrayList();
		for(int i = 0; i < list.size(); i++) {
			if((int) list.get(i) > 3000) {
				result.add(list.get(i)); // 3333, 4444, 5555만 추가됨
			}
		}
		
		// 4. 필터링된 최종 목록 반환
		return result;
	}

}
