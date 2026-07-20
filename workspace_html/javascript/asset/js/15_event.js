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
}
// window.onload = init

window.addEventListener('load' , init)

function bind() {

}