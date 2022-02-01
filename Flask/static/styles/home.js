// console.log("hello")
const welocme_msg = (function() {
    var executed = false;
    return function(msg_classname, img_src, msg_text) {
        if (!executed) {
            executed = true;
            // do something
            insert_into_web(msg_classname, img_src, msg_text)
        }
    };
})();

document.querySelector('.chathead').addEventListener('click', ()=>{
    const chatcont = document.querySelectorAll('.chat_content')
    for (var i = 0; i < chatcont.length; i++) {
        chatcont[i].classList.toggle('chatmob')
    }

    document.querySelector('.mainbody').classList.toggle('restchat')
    document.querySelector('.sidebody').classList.toggle('restchat')
    document.querySelector('.chathead').classList.toggle('chathead_mob')
    document.querySelector('.chatter').classList.toggle('chatter_mob')

        // bot initial msg
        bot_initial_msg = "Hi! I am from Mirafra.\
        \nI can help you in booking the flight tickets\
        \nWelcome to our flight booking services."
        
        
        setTimeout(
            function(){
                welocme_msg("bot_msg_in_body", "https://support.upwork.com/hc/article_attachments/360040474034/chatbot-data.png", bot_initial_msg);
            }, 1000);

})



function create_block_to_add(){
    const user_msg_div = document.createElement("div")
    return user_msg_div
}

function img_icon_block(img_src){    
    const imguser = document.createElement("img")
    imguser.src = img_src
    return imguser
}

function message_content_block(msg_text){
    const puser = document.createElement("p")
    if(msg_text == ".msg_inp"){
        const actual_user_msg = document.querySelector(msg_text).value
        document.querySelector(msg_text).value = null
        puser.innerText = actual_user_msg
    }
    else{
        puser.innerText = msg_text      
    }
    return puser
}

function add_class_to_msg_block(user_msg_div, msg_classname){
    user_msg_div.classList.add("msg_in_body")
    user_msg_div.classList.add(msg_classname)
    return user_msg_div
}

function add_blocks_to_chat(msg_text, user_msg_div, chatb, imguser, puser){
    
    if(msg_text == ".msg_inp"){
        user_msg_div.appendChild(imguser)
        user_msg_div.appendChild(puser)
    }
    else{
        user_msg_div.appendChild(puser)
        user_msg_div.appendChild(imguser)
    }
    chatb.appendChild(user_msg_div)
}

function add_break_line(chatb){
    const bruser = document.createElement("br")
    chatb.appendChild(bruser)
    return chatb
}

function insert_into_web(msg_classname, img_src, msg_text){
    const chatb = document.querySelector(".chatbody")

    let user_msg_div = create_block_to_add()
    let imguser, puser

    imguser = img_icon_block(img_src)
    puser = message_content_block(msg_text)
    

    const actual_user_msg = puser.innerText

    user_msg_div = add_class_to_msg_block(user_msg_div, msg_classname)

    add_blocks_to_chat(msg_text, user_msg_div, chatb, imguser, puser)

    chatb.scrollTop = chatb.scrollHeight;

    // add_break_line(chatb)

    // console.log(actual_user_msg)
    return actual_user_msg
}

document.querySelector('.msg_button').addEventListener('click', ()=>{
    // user query
    const actual_user_msg = insert_into_web("user_msg_in_body", "https://nulm.gov.in/images/user.png", ".msg_inp")
    
    const user_query = {
        "sender": "user",
        "message": actual_user_msg
    }
    const myHeaders = new Headers({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Credentials" : true 
    })
    const options = {
        method: 'POST',
        mode: 'cors',
        headers: myHeaders,
        body: JSON.stringify(user_query)
    }

    const fetchRes = fetch('http://localhost:5005/webhooks/rest/webhook', options)
    fetchRes
    .then(response => response.json())
    .then(data => {
        for (var i = 0; i < data.length; i++) {
            // console.log(data[i]['text'])
            insert_into_web("bot_msg_in_body", "https://support.upwork.com/hc/article_attachments/360040474034/chatbot-data.png", data[i]['text'])
        }
    })


    
})