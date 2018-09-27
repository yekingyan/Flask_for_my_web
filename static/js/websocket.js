var log = function () {
    console.log.apply(console, arguments)
};

// 连接的实例
var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');


socket.on('connect', function () {
    console.log('connect');
    socket.emit('connect_event', {data: 'I\'m connected!'});
});


socket.on('server_response', function (msg) {
    console.log(msg);
});

// 发送输入框的内容
var send_message_from_input = function () {
    $('#submit').click(function () {
        log('submit:', $('#msg_input').val());
        socket.emit('client_event', {
            'content': $('#msg_input').val(),
            'user': $('input[name="user"]').val()
        });
        // return false;
    });
};

// message最新一条信息的所属用户
var messageLastUser = function () {
    var users = document.querySelectorAll('span[title="user"]');
    var lastUser = (users[users.length-1]).valueOf();
    return lastUser.textContent
};


//message的模板
var messageTemplate = function (msg) {
    var
        user = msg.user,
        message_user = msg.message_user,
        time = new Date(Number(msg.ct.toString() + '000')),
        ct = time.getDate()+'-'+time.getHours()+':'+time.getMinutes(),
        id = msg.id,
        content = msg.content,
        del_button = msg.del_button;
    //log("转的时间",time);
    // 用户栏
    var t1 = function () {
        var temp;
        if (user === null){
            temp = `
                <div>
                    <p class="d-inline">
                        <span class="text-black-50">${ct}</span>
                        <span class="ml-2 font-weight-bold"><span title="user">${message_user}</span><span class="text-white bg-info ml-1">&nbsp说&nbsp</span></span>
                    </p>

                </div>
        `
        }else {
            temp = `
                 <div>
                    <p class="d-inline">
                        <span class="text-black-50">${ct}</span>
                        <span class="ml-2 font-weight-bold"><span title="user">${user}</span><span class="text-white bg-info ml-1">&nbsp说&nbsp</span></span>
                    </p>
                </div>
            `
        }
        return temp
    };
    // message内容及删除按纽
    var t2 = `
        <span class="d-none">${id}</span>
                <span class="list-group-item-action list-group-item-success d-inline-flex mb-2">
                    ${content}
                    
                
    `
    var d_button = function () {
        var del;
        if (del_button === true){
            del = `
                <a class="fa fa-times mt-1 text-danger" href="/message/delete/${id}"></a>
                <br>
                </span>
    `
        }else {
            del = `
                <br>
                </span>
    `
        }
        return del
    }

    var t = function () {
        var temp;
        if(messageLastUser() === user){
            temp = t2 + d_button();
        }else if(messageLastUser() === message_user){
            temp = t2 + d_button();
        }else {
            temp = t1() + t2 + d_button();
        }
        return temp
    };

    log(`页面中最后用户：${messageLastUser()}。当前用户：${user}`);
    return t()
};


//message的插入
var insertMesage = function (msg) {
    var messages = document.querySelector('#message');
    var message = messageTemplate(msg);
    messages.insertAdjacentHTML('beforeend', message);
    messages.scrollTop = messages.scrollHeight;
};


//meesage的插入事件绑定
var accept_message = function () {
    socket.on('new_message', function (msg) {
        console.log("accept:", msg);
        insertMesage(msg)
    });
};


// flash的模板
var flashTemplate = function (msg) {
    var flash = msg.flash;
    var t = `
        <div class="alert alert-dismissible fade show alert-info" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
            </button>
            <strong>${flash}</strong>
        </div>
    `;
    return t
};

// flash的插入
var insertFlash = function (msg) {
    var nav = document.querySelector('nav');
    var flash = flashTemplate(msg);
    nav.insertAdjacentHTML('afterend', flash)
};

// flash 提醒信息绑定事件
var flash_message = function () {
    socket.on('flash_message', function (msg) {
        log("flash:", msg);
        insertFlash(msg);
    })
};

// 保持在滚动条底部
var scroll_bottom = function () {
    var messages = document.querySelector('#message');
    messages.scrollTop = messages.scrollHeight;
};


var main = function () {
    $(document).ready(function () {
        send_message_from_input();
        accept_message();
        flash_message();
        scroll_bottom();
    });
};
main();
