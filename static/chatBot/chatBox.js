function chatBtn()
{
    // 成功发送
    let send_message = document.getElementById("msg_container");
    let domBtm = document.getElementById("home-search");
    // 发送内容
    let message = document.getElementById("home-textinput");
    domBtm.addEventListener("click", function () {
        let str = message.value;
        let date = new Date();
        let hour = date.getHours();
        let mm = date.getMinutes();
        let time = hour + ':' + mm;
        let ans = '<div class="chat_right_item_1 clearfix">热巴</div>' +
            '<div class="chat_right_item_2">' +
            '<div class="chat_right_time clearfix">' + time + '</div>' +
            '<div class="chat_right_content clearfix">' + str + '</div>'
            + '</div>';
        let oLi = document.createElement("div");
        oLi.setAttribute("class", "chat_right");
        oLi.innerHTML = ans;
        send_message.append(oLi);
        message.value = "";
    });
}