function log(message) {
    const div =  document.createElement('div')
        div.classList.add('log')
        div.innerHTML = message
        const view = document.querySelector('#view')
         view.prepend(div)
}

window.onload = function() {
    bind()
}

function bind() {
    const area = document.querySelector('#area')
    area.oncontextmenu = () => {
        alert('오른쪽 버튼 금지입니다')
        return  false
    }
    area.onselectstart = function() {
        return false
    }
    const area2 = document.querySelector('#area2')
    area2.addEventListener('copy' , function(event){
        event.preventDefault()

        const selection = window.getSelection().toString
        if(selection.length == 0) {
            return
        }
        const str = '[출처] www.naver.com'
        const result = selection + str

        event.clipboardData.setDate('text/plain' , result)
    })

    area2.addEventListener('doubleclick' , function(){
        log('더블클릭 발생')
    })

    area2.addEventListener('mousedown' , function(){
        log('mousedown')
    })
    area2.addEventListener('mouseup' , function(){
        log('mouseup')
    })
    area2.addEventListener('click' , function(evt){
        log('click')
        /*
            offset :  DOM 최상단 기준
            page : 스크롤에 관계없이 문서 최상단 기준

            client : 지금 딱 보는 브라우저 좌상단 기준
            screen : 실제 모니터 좌상단 기준
        */

        log('offsetY :' + evt.offsetY )
        log('pageY :' + evt.pageY )
        log('clientY :' + evt.clientY )
        log('screenY :' + evt.screenY )
    })
    area2.addEventListener('mouseover' , function(evt) {
        log('mouseover')
        area2.style.backgroundColor = 'yellow'
    })

    area2.addEventListener('mouseout' , function(evt){
        log('mouseout')
        area2.style.backgroundColor = 'white'
    })
    
    area2.addEventListener('mousemove' , function(evt){
        log('mousemove')
        log(`offsetX : ${evt.offsetX} , offsetY: ${evt.offsetY}` )
    })

    document.querySelector('body').addEventListener('mousemove' , function(evt){
        const game = document.querySelector('#game')

        game.style.top = evt.pageY+1 + 'px'
        game.style.left = evt.pageX+1 + 'px'

        log(`X : ${evt.offsetX} , Y: ${evt.offsetY}` )
    })

}