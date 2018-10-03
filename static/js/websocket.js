var log = function () {
    console.log.apply(console, arguments)
};

// 连接的实例
var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

// 触发连接
var first_connect = function () {
    socket.on('connect', function () {
        console.log('try to connect server');
        ($('#message').children()).remove();
        socket.emit('connect_event', {'data': 'I\'m connected!'});
    });
};


// 加载全部msg
var load_all_msg = function () {
    socket.on('server_response', function (msg) {
        var json = msg.data;
        for (var i = 0; i < Object.keys(json).length; i++) {
            log("<--加载条数");
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

// 发送输入框的内容，回车键
var send_message_form_enter = function () {
    $('#msg_input').keydown(function (e) {
        var e = e || window.event;
        if (e.keyCode === 13) {
            log('submit:', $('#msg_input').val());
            socket.emit('client_event', {
                'content': $('#msg_input').val(),
                'user': $('input[name="user"]').val()
            });
            event.returnValue = false;
        }
    });
    return false;
};

// message最新一条信息的所属用户
var messageLastUser = function () {
    var users = $('span[title="user"]');
    if (users.length === 0) {
        return false
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
        content = msg.content;
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
                <div id= "del-${id}" class="list-group-item-action list-group-item-success d-inline-flex mb-2">
                    ${content}
                    
                
    `;
    var d_button = function () {
        var
            del,
            username = $('#user').text(),
            message_user_name = $('#message_user').text().replace(/[\s*]/gm, '')
        ;
        // log(username === user);
        if (username === user && user !== '') {
            del = `
                <a id= "del-a-${id}" class="fa fa-times mt-1 text-danger" href="/message/delete/${id}"></a>
                </div>
    `
        } else if (message_user_name === message_user && message_user !== '') {
            del = `
                <a id= "del-a-${id}" class="fa fa-times mt-1 text-danger" href="/message/delete/${id}"></a>
                </div>
    `
        } else {
            del = `
                </div>
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
            temp = `<div class="cell-${id} cell">` + t1() + t2 + d_button() + '</div>';
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
    if (messageLastUser() === msg.user) {
        let cells = document.querySelectorAll('div.cell');
        let div = (cells[cells.length - 1]);
        div.insertAdjacentHTML('beforeend', message);

    } else if (messageLastUser() === msg.message_user) {
        let cells = document.querySelectorAll('div.cell');
        let div = (cells[cells.length - 1]);
        div.insertAdjacentHTML('beforeend', message);
    } else {
        messages.insertAdjacentHTML('beforeend', message);
    }

    messages.scrollTop = messages.scrollHeight;
};


// 去掉输入档下方的用户名栏
var after_input_user_commit = function (msg) {
    var input_user = $('input[name="user"]');
    if (msg.message_user === input_user.val()) {
        //去除
        $('p.mt-2').remove();
        input_user.val('');
        input_user.css({'visibility': 'hidden'});
        //加入
        ($('form')[1]).insertAdjacentHTML(
            'afterbegin', `
            <span class="fa fa-user-secret font-weight-bold ml-2" id="message_user">
                ${msg.message_user}
            </span>
        `);
    }
};


//message的插入事件绑定
var accept_message = function () {
    socket.on('new_message', function (msg) {
        console.log("accept:", msg);
        after_input_user_commit(msg);
        insertMesage(msg);

    });
};


// 请求删除 message
var request_remove_message = function (msg) {

    $(document).off('click').on('click', `a.text-danger`, function (event) {
        var self = event.target;
        var logg = self.getAttribute('href');
        var id = logg.slice(16);
        console.log("尝试删除：", id);
        socket.emit('delete_msg', {'id': id});
        event.preventDefault();
        return false;
    });
};

// 删除事件监听
var delete_message = function () {
    socket.on('remove', function (msg) {
        log("delete:", msg);
        var id = msg.id;
        var child = $(`#del-${id}`);
        var childs = child.parent().children();
        // log('cl', childs.length);
        if (childs.length <= 2) {
            child.parent().remove();
        } else {
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

// 重载数据
var reload = function () {
    // 时间控制
    function* sleep(ms) {
        yield new Promise(function (resolve, reject) {
            setTimeout(resolve, ms);
        })
    }

    // 重发请求
    // var count = 0;

    sleep(2000).next().value.then(() => {
        var cell = $(".cell");
        log("检测cell");
        // count = count+1;
        if (cell.length === 0) {
            // ($('#message').children()).remove();
            socket.emit('connect_event', {'data': 'I\'m connected!'});
            log('reload msg')
        }
    })
};

var main = function () {
    $(document).ready(function () {
        first_connect();
        load_all_msg();
        send_message_from_input();
        send_message_form_enter();
        accept_message();
        request_remove_message();
        delete_message();
        scroll_bottom();
        flash_message();
        reload();
    });
};
main();

//天气
// ip to address
var get_city = function (responseCallback) {
    $.ajax({
        url: 'http://api.map.baidu.com/location/ip?ak=ia6HfFL660Bvh43exmH9LrI6',
        type: 'POST',
        dataType: 'jsonp',
        success: function (data) {
            // log('a', typeof(JSON.stringify(data.content.address_detail.province + "," + data.content.address_detail.city)));
            responseCallback(data.content.address_detail.province, data.content.address_detail.city)
        }
    });
};


var city_code = function (province, city) {
    if (city.substr(-1) === '市') {
        city = city.substring(0, city.length - 1)
    }
    // log(code);
    socket.emit('city_addr', {'city_addr': city});
};


// 根据地址显示天气 todo
var get_weather = function () {
    socket.on('weather', function (data) {
        log(data);
        log(typeof(data))
    })
}


var weather = function () {
    $(document).ready(function () {
        get_city(city_code);
        get_weather()
    })
};

weather();

