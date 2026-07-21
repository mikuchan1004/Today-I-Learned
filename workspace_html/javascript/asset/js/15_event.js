console.log('hello js')

// id btn1을 변수 btn1에 담아서 console.log로 출력 
const btn1 = document.querySelector('#btn1')
console.log(1, 'btn1', btn1)

console.log(window)

// 페이지 로딩 이벤트가 발생하면...
// window.onload = function(){
//     const btn1 = document.querySelector('#btn1')
//     console.log(2, 'btn1', btn1)
// }
function init(){
    const btn1 = document.querySelector('#btn1')
    console.log(2, 'btn1', btn1)

    bind()

    const game = document.querySelector('#game')
    game.style.left = '20px'
}
window.onload = init

// window.addEventListener('load' , init)

function bind() {
    const btn1 = document.querySelector('#btn1')

    btn1.onclick = function(){
        console.log('btn1 클릭')
    }

    btn1.onclick = function(){
        console.log('btn1 click')
    }
    
    // addEventListener : 동일한 이벤트에 여러 함수를 추가할 수 있다
    const btn2 = document.querySelector('#btn2')
    btn2.addEventListener('click' , function(){
        console.log('btn2 클릭')
    })
    btn2.addEventListener('click' , function(){
        console.log('btn2 click')
    })

    const btn4 = document.querySelector('#btn4')
    btn4.addEventListener('click' , btn4click)
    // removeEventListner 
    // 이벤트 제거
    // 단, 익명함수는 제거 못함
    btn4.removeEventListener('click' , btn4click)
    
    const login = document.querySelector('#login')
    login.addEventListener('click', function(){
        const id = document.querySelector('#id')
        const pw = document.querySelector('#pw')
        const warning = document.querySelector('.warning')
    
        console.log('id.value :' , id.value)
        console.log('pw.value :' , pw.value)
    
        // id를 적었는지 판단 
        if(id.value.trim() == '') {
            // console.log('아이디는 필수입니다.')
            warning.innerText = '아이디는 필수입니다.'
            log('아이디는 필수입니다')
        } 
        else if(pw.value.trim() == '') {
            warning.innerText = '비밀번호는 필수입니다.'
            log('비밀번호는 필수입니다')
        }
    })

    document.querySelector('#id').addEventListener('keydown', function(){
        // log('keydown 발생')
    })
    document.querySelector('#id').addEventListener('keyup', function(event){
        // log('keyup 발생')
        // console.log(event)
        // log('key: ' + event.key)
        log('keyCode: ' + event.keyCode)

        // log('shiftKey: ' + event.shiftKey)
        // log('ctrlKey: ' + event.ctrlKey)
        // log('altKey: ' + event.altKey)

        if (event.keyCode == 13) { // 엔터
            log('엔터 빵')
            const pw = document.querySelector('#pw')
            pw.focus()

        }

        if(event.ctrlKey && event.keyCode == 67) {
            alert('ctrl + c')
        }

    })
    document.querySelector('#pw').addEventListener('keyup' , function(){
        if(event.keyCode == 13) {
            const login = document.querySelector('#login')
            login.click()
        }
    })
    document.querySelector('#top').addEventListener('click' , function(event){
        // document.documentElement.scrollTop = 0
        window.scrollTo({
                top : 0, 
                behavior : 'smooth'
            })
    })
    window.addEventListener('scroll', function(){
        // console.log('window.scrollY' , window.scrollY)
    })
    
    const game = document.querySelector('#game')
    let x = 0
    let y = 0
    const speed = 10
    
    document.querySelector('body').addEventListener('keydown' , function(event){
        log(event.keyCode)

        switch(event.key) {
            case 'ArrowUp' : 
                y -= speed
                break
            case 'ArrowDown' :
                y += speed
                break
            case 'ArrowLeft' :
                x -= speed
                break
            case 'ArrowRight' :
                x += speed
                break
            default : 
                return
        }
        event.preventDefault()

        game.style.left = x + 'px'
        game.style.top = y + 'px'
       
        // if(event.keyCode == 39) {
        //  game.style.left = (parseInt(game.style.left) + 10) + 'px'
        // }
    })
    
function btn3click() {
    console.log('btn3 click')
}
function btn4click() {
    console.log('btn4 click')
}
function log(message) {
    const div =  document.createElement('div')
        div.classList.add('log')
        div.innerHTML = message
        const view = document.querySelector('#view')
         view.prepend(div)
}

}
