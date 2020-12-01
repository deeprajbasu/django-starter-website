console.log('hi' )

var updatebtns=document.getElementsByClassName('update-cart') 
//get all buttons with class update-cart

for(var i=0;i<updatebtns.length;i++){//go through all buttons

    updatebtns[i].addEventListener('click',function(){ //add click listeners to all buttons with update cart
        //function upon event
        var productID= this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productID,'action:',action )

        console.log('user:',user)
        if(user=='AnonymousUser'){
            addCookieItem(productID,action)

        }else{
            updateUserOrder(productID,action)
            // location.reload()
        }


    })
    

}

var detailbuttons=document.getElementsByClassName('show-item') 

for(var i=0;i<detailbuttons.length;i++){//go through all buttons

    detailbuttons[i].addEventListener('click',function(){ //add click listeners to all buttons with update cart
        //function upon event
        console.log('cliclllllkkkkk:' )
        var productID= this.dataset.product
        show_item(productID)



    })
    

}

function addCookieItem(productID,action){
    console.log('not logged in................')
    if (action=='add'){
        if (cart[productID]==undefined){
            cart[productID] =  {'quantity':1} 

        }else{
            cart[productID]['quantity']+=1

        }}
    if (action=='remove'){
        
        cart[productID]['quantity']-=1
        if (cart[productID]['quantity']<=0){
            delete cart[productID]

        }
    }
    document.cookie='cart='+JSON.stringify(cart)+";domain;path=/"
    
    console.log('cart',cart)
    location.reload()

}

function updateUserOrder(productID,action){
    console.log('user is logged sending data')
    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{'content-type':'application/json',
                 'X-CSRFToken':csrftoken,
                },
                credentials: 'include',
                //send data to backend to update order and cart*****************
                body:JSON.stringify({'productID':productID,'action':action})
    
    })
    .then((response)=>{return response.json()})
    .then((data)=>{console.log('data',data)
                    location.reload()    
                    })
    

}

function show_item(productID,action){
    console.log('working')
    var url = '/item_details/'
    fetch(url,{
        method:'POST',
        headers:{'content-type':'application/json',
                 'X-CSRFToken':csrftoken,
                },
                credentials: 'include',
                //send data to backend to update order and cart*****************
                body:JSON.stringify({'productID':productID,'action':action})
    
    }).then(function (response) {
        return response.text()
      }).then(function (html) {
        // This is the HTML from our response as a text string
        console.log(html)
        console.log('helloooooooo')
        toggleModal()
        document.getElementById("ITEMITEM").innerHTML = html
        // ( "html" ).replaceWith( html );
        

      })
    //                 location.reload()    
                  


}
var closemodal = document.querySelectorAll('.modal-close')
for (var i = 0; i < closemodal.length; i++) {
    closemodal[i].addEventListener('click', Closemodal)
}   
function Closemodal (){
    location.reload()    

}
function toggleModal () {
    const body = document.querySelector('body')
    const modal = document.querySelector('.modal')
    modal.classList.toggle('opacity-0')
    modal.classList.toggle('pointer-events-none')
    body.classList.toggle('modal-active')
  }
    