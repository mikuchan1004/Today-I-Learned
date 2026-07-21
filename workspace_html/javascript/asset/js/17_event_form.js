function log(message) {
    const div =  document.createElement('div')
        div.classList.add('log')
        div.innerHTML = message
        const view = document.querySelector('#view')
         view.prepend(div)
}

window.addEventListener('load' , function(){
    const query = document.querySelector('#query')
    query.addEventListener('focus' , function(){
        query.style.background = 'yellow'
    })
    query.addEventListener('blur' , function(){
        query.style.background = ''
    })
    // 값이 변경될 때 잡아줌
    query.addEventListener('input' , function(){
        log(query.value)

        const r = parseInt(Math.random()*256)
        const g = parseInt(Math.random()*256)
        const b = parseInt(Math.random()*256)
        const a = Math.random()

        query.style.backgroundColor = `rgba(${r}, ${g}, ${b}, ${a})`
    })

    const form = document.querySelector('#form')
    form.addEventListener('submit' , function(event){

        // 태그의 기본(고유) 기능을 막아준다 
        event.preventDefault() 

        if(query.value.trim().length < 2) {
            alert('검색어는 두 글자 이상입니다')
        } else {
            form.submit()
        }
    })

    const parent = document.querySelector('#parent')
    parent.addEventListener('click' , function(event){
        log('부모 클릭')

        // target: 실제 이벤트가 발생한 DOM
        console.log('event.target' , event.target)

        // current : 이벤트가 적용되어 있는 DOM
        console.log('event.currentTarget' , event.currentTarget)

        // this 
        // addEventListener 안에서는 event.currentTarget
        // 대부분의 경우 window를 가지고 있다
        // 그래서 현재 this에 어떤 값이 있는지 알고 있을 때만 쓴다
        // arrow 함수의 경우 this === window
        console.log('this' , this)
        console.log( this === event.currentTarget)
    })

    const child1 = document.querySelector('#child1')
    child1.addEventListener('click' , function(event){

        // 전달 방지 
        // 부모로 전달되는 이벤트 중지 
        event.stopPropagation()

        log('자식1 클릭')
    })

    // const board = document.querySelector("#board")
    // board.addEventListener('click' , function(event){

    //     // click된 DOM 출력
    //     console.log('event.target' , event.target)

    //     // 지금 클릭 요소에 클래스 chk가 있는지 출력
    //     // 체크박스 일때만 value 출력
    //     if(event.target.classList.contains('chk')) {
    //         log(event.target.value)
    //     }

    //     // 제목을 클릭했을때 제목 출력
    //     if(event.target.classList.contains('title')) {
    //         log(event.target.innerText)
    //     }

    //     // 작성자를 클릭하면 속성 writer의 값을 출력
    //     if(event.target.hasAttribute('writer')) {
    //         log(event.target.getAttribute('writer'))
    //     }

    // })

    const trs = document.querySelectorAll('#board tr')
        
        for(let tr of trs) {
            tr.addEventListener('click' , function(event){

        
            console.log('event.target' , event.target)

       
            if(event.target.classList.contains('chk')) {
                log(event.target.value)
            }

        
            if(event.target.classList.contains('title')) {
                log(event.target.innerText)
            }

    
            if(event.target.hasAttribute('writer')) {
                log(event.target.getAttribute('writer'))
            }

        })

        tr.querySelector('input.chk').addEventListener('click' , function(event){
            
            event.stopPropagation()

            console.log(
                this.parentNode.parentNode.querySelector('.title').innerText
            )
            
        })
    }

})

console.log(this)

/*
문제 1 : 주문과 배송 
주문 정보 : input으로 이름, 주소
ㅁ 주문 정보와 배송 정보가 같습니다
배송 정보 : input으로 이름, 주소
* 체크하면 주문 정보가 배송 정보로 복사.
* 체크를 풀면 배송 정보 글씨 지우기


문제 2: 로그인창
로그인 버튼 눌렀을 때
아이디 또는 비밀번호가 없으면 빨간 글씨 나오게 
단, 아이디/비밀번호를 쓰고 로그인을 누르면 빨간 글씨 지우기 


문제 3: 피자 주문
1. 피자 종류 선택 : select 
- 불고기, 페퍼로니, 포테이토, 치즈, 파인애플, 고르곤졸라
2. 사이즈 선택 : radio
- small(18000), medium(20000), large(22000)
3. 도우 선택 : radio
- 씬, 고구마, 치즈, 소보로
4. 토핑 topping : checkbox
- 감자(2000), 고구마(2000), 치즈(2500), 베이컨(3000), 옥수수(500), 페페론치노(2500)
[확인]
+ 문제 3-1 : 선택 내역 모두 출력
+ 문제 3-2 : 선택 내역과 총액 출력 


문제 4 : 메뉴 선택 
인기상품순, 낮은가격순, 높은가격순, 신상품순, 상품평 많은순 
+ 클릭한 것만 굵은 글씨로 유지


문제 5 : Todo List 
할일을 적는 input, 추가 버튼
+ 5-1 : 추가 버튼을 누르면 체크박스와 할일이 하단에 추가된다
+ 5-2 : 개별 삭제 버튼이 있고, 클릭 시 그 줄이 지워진다. (dom.remove())
+ 5-3 : 전체 선택 checkbox가 있고 
        전체 선택 체크 시 : 모든 checkbox 체크 
        해제 시 : 모든 checkbox 체크 해제
+ 5-4 : 전체 선택 후에 하나라도 개별 해제가 되면 전체 선택도 해제
        개별로 모두 체크한 경우 전체 선택도 체크된다.
+ 5-5 : 선택 삭제 버튼 클릭 시 선택된 내용만 삭제
*/


