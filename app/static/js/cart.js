function handleBuy(productId,action){
    if (user == 'AnonymousUser'){
        alert('Bạn cần đăng nhập!')
    }
    else{
        updateOrder(productId,action)
    }
}


function updateOrder(productId,action){
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
        window.location.reload(true);
    })



}

