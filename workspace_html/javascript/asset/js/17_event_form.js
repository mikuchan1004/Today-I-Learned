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