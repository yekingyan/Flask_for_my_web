var log = function () {
    console.log.apply(console, arguments)
};

// 连接的实例
var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

// 触发连接
socket.on('connect', function () {
    console.log('try to connect server');
    socket.emit('connect_event', {'data': 'I\'m connected!'});
});

// 加载全部msg
var load_all_msg = function () {
    socket.on('server_response', function (msg) {
        var json = msg.data;
        for (var i = 0; i<Object.keys(json).length; i++) {
            log('in',i);
            json[i]['ct'] = json[i]['ut'];
            // log(json[i]['ut']);
            insertMesage(json[i]);
            request_remove_message();
        }
    });
};


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
    if (users.length === 0) {
        return ''
    } else {
        var name = (users[users.length - 1]).valueOf();
        return name.textContent
    }

};


//message的模板
var messageTemplate = function (msg) {
    var
        user = msg.user,
        message_user = msg.message_user,
        time = new Date(Number(msg.ct.toString() + '000')),
        ct = time.getDate() + '-' + time.getHours() + ':' + time.getMinutes(),
        id = msg.id,
        content = msg.content,
        del_button = msg.del_button;
    //log("转的时间",time);
    // 用户栏
    var t1 = function () {
        var temp;
        if (user === null) {
            temp = `
                <div>
                    <p class="d-inline">
                        <span class="text-black-50">${ct}</span>
                        <span class="ml-2 font-weight-bold"><span title="user">${message_user}</span><span class="text-white bg-info ml-1">&nbsp说&nbsp</span></span>
                    </p>

                </div>
        `
        } else {
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
                <span id= "del-${id}" class="list-group-item-action list-group-item-success d-inline-flex mb-2">
                    ${content}
                    
                
    `;
    var d_button = function () {
        var
            del,
            username=$('#user').text(),
            message_user_name=$('#message_user').text()
        ;
        // log(del_button);
        if (username===user) {
            del = `
                <a class="fa fa-times mt-1 text-danger" href="/message/delete/${id}"></a>
                <br>
                </span>
    `
        } else if(message_user_name===message_user){
            del = `
                <a class="fa fa-times mt-1 text-danger" href="/message/delete/${id}"></a>
                <br>
                </span>
    `
        }else{
            del = `
                <br>
                </span>
    `
        }
        return del
    };

    var t = function () {
        var temp;
        if (messageLastUser() === user) {
            temp = t2 + d_button();
        } else if (messageLastUser() === message_user) {
            temp = t2 + d_button();
        } else {
            temp =`<div class="cell-${id} cell">` + t1() + t2 + d_button() + '</div>';
        }
        return temp
    };

    // log(`页面中最后用户：${messageLastUser()}。当前用户：${user}`);
    return t()
};


//message的插入
var insertMesage = function (msg) {
    var messages = document.querySelector('#message');
    var message = messageTemplate(msg);
    if(messageLastUser()===msg.user){
        let cells = document.querySelectorAll('div.cell');
        let div = (cells[cells.length - 1]);
        div.insertAdjacentHTML('beforeend', message);

    }else if(messageLastUser()===msg.message_user){
        let cells = document.querySelectorAll('div.cell');
        let div = (cells[cells.length - 1]);
        div.insertAdjacentHTML('beforeend', message);
    }else {
        messages.insertAdjacentHTML('beforeend', message);
    }

    messages.scrollTop = messages.scrollHeight;
};


//message的插入事件绑定
var accept_message = function () {
    socket.on('new_message', function (msg) {
        console.log("accept:", msg);
        insertMesage(msg)
    });
};

// 请求删除 message
var request_remove_message = function (msg) {
    var dels = $('a.text-danger');
    for (var i = 0; i < dels.length; i++) {
        dels[i].addEventListener('click', function (event) {
            var self = event.target;
            var logg = self.getAttribute('href');
            var id = logg.slice(16);
            console.log("尝试删除：", id);
            socket.emit('delete_msg', {'id': id});
            event.preventDefault();
            return false;
        })
    }
};

// 删除事件监听
var delete_message = function () {
    socket.on('remove', function (msg) {
        log("delete:", msg);
        var id = msg.id;
        var child = $(`#del-${id}`);
        var childs = child.parent().children();
        log('cl',childs.length);
        if (childs.length <= 2){
            child.parent().remove();
        }else {
            child.remove();
        }

        // return false;
    })
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
        load_all_msg();
        send_message_from_input();
        accept_message();
        request_remove_message();
        delete_message();
        scroll_bottom();
        flash_message();
    });
};
main();
