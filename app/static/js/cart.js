let updateBtn = document.getElementsByClassName("update-cart");

for(i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function (){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log(productId)
        console.log(action)
        if (user === 'AnomymousUser'){
            console.log('user not login')
        }
        else{
            updateOrder(productId,action)
        }
    })
}
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
const csrftoken = getCookie('csrftoken');

function updateOrder(productId,action){
console.log('token :'+csrftoken)

    let url='/update_item/'
    fetch(url,{
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId':productId,'action':action})

    })
    .then((res)=>{
        return res.json()
    })
    .then((data) =>{
        console.log('data',data)
    })
}