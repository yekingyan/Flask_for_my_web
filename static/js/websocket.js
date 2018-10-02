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
            responseCallback(data.content.address_detail.province,data.content.address_detail.city)
        }
    });
};

// address code
var city_code_obj = {"\u5317\u4eac": "101010100", "\u4e0a\u6d77": "101020100", "\u5929\u6d25": "101030100", "\u91cd\u5e86": "101040100", "\u9999\u6e2f\u7279\u522b\u884c\u653f\u533a": "101320101", "\u6fb3\u95e8\u7279\u522b\u884c\u653f\u533a": "101330101", "\u54c8\u5c14\u6ee8": "101050101", "\u9f50\u9f50\u54c8\u5c14": "101050201", "\u7261\u4e39\u6c5f": "101050301", "\u5927\u5e86": "101050901", "\u4f0a\u6625": "101050801", "\u53cc\u9e2d\u5c71": "101051301", "\u9e64\u5c97": "101051201", "\u9e21\u897f": "101051101", "\u4f73\u6728\u65af": "101050401", "\u4e03\u53f0\u6cb3": "101051002", "\u9ed1\u6cb3": "101050601", "\u7ee5\u5316": "101050501", "\u5927\u5174\u5b89\u5cad": "101050701", "\u957f\u6625": "101060101", "\u5ef6\u5409": "101060301", "\u5409\u6797": "101060201", "\u767d\u5c71": "101060901", "\u767d\u57ce": "101060601", "\u56db\u5e73": "101060401", "\u677e\u539f": "101060801", "\u8fbd\u6e90": "101060701", "\u5927\u5b89": "101060603", "\u901a\u5316": "101060501", "\u6c88\u9633": "101070101", "\u5927\u8fde": "101070201", "\u846b\u82a6\u5c9b": "101071401", "\u76d8\u9526": "101071301", "\u672c\u6eaa": "101070501", "\u629a\u987a": "101070401", "\u94c1\u5cad": "101071101", "\u8fbd\u9633": "101071001", "\u8425\u53e3": "101070801", "\u961c\u65b0": "101070901", "\u671d\u9633": "101071201", "\u9526\u5dde": "101070701", "\u4e39\u4e1c": "101070601", "\u978d\u5c71": "101070301", "\u547c\u548c\u6d69\u7279": "101080101", "\u9521\u6797\u6d69\u7279": "101080901", "\u5305\u5934": "101080201", "\u8d64\u5cf0": "101080601", "\u6d77\u62c9\u5c14": "101081001", "\u4e4c\u6d77": "101080301", "\u9102\u5c14\u591a\u65af": "101080701", "\u901a\u8fbd": "101080501", "\u77f3\u5bb6\u5e84": "101090101", "\u5510\u5c71": "101090501", "\u5f20\u5bb6\u53e3": "101090301", "\u5eca\u574a": "101090601", "\u90a2\u53f0": "101090901", "\u90af\u90f8": "101091001", "\u6ca7\u5dde": "101090701", "\u8861\u6c34": "101090801", "\u627f\u5fb7": "101090402", "\u4fdd\u5b9a": "101090201", "\u79e6\u7687\u5c9b": "101091101", "\u90d1\u5dde": "101180101", "\u5f00\u5c01": "101180801", "\u6d1b\u9633": "101180901", "\u5e73\u9876\u5c71": "101180501", "\u7126\u4f5c": "101181101", "\u9e64\u58c1": "101181201", "\u65b0\u4e61": "101180301", "\u5b89\u9633": "101180201", "\u6fee\u9633": "101181301", "\u8bb8\u660c": "101180401", "\u6f2f\u6cb3": "101181501", "\u4e09\u95e8\u5ce1": "101181701", "\u5357\u9633": "101180701", "\u5546\u4e18": "101181001", "\u4fe1\u9633": "101180601", "\u5468\u53e3": "101181401", "\u9a7b\u9a6c\u5e97": "101181601", "\u6d4e\u5357": "101120101", "\u9752\u5c9b": "101120201", "\u6dc4\u535a": "101120301", "\u5a01\u6d77": "101121301", "\u66f2\u961c": "101120710", "\u4e34\u6c82": "101120901", "\u70df\u53f0": "101120501", "\u67a3\u5e84": "101121401", "\u804a\u57ce": "101121701", "\u6d4e\u5b81": "101120701", "\u83cf\u6cfd": "101121001", "\u6cf0\u5b89": "101120801", "\u65e5\u7167": "101121501", "\u4e1c\u8425": "101121201", "\u5fb7\u5dde": "101120401", "\u6ee8\u5dde": "101121101", "\u83b1\u829c": "101121601", "\u6f4d\u574a": "101120601", "\u592a\u539f": "101100101", "\u9633\u6cc9": "101100301", "\u664b\u57ce": "101100601", "\u664b\u4e2d": "101100401", "\u4e34\u6c7e": "101100701", "\u8fd0\u57ce": "101100801", "\u957f\u6cbb": "101100501", "\u6714\u5dde": "101100901", "\u5ffb\u5dde": "101101001", "\u5927\u540c": "101100201", "\u5415\u6881": "101101101", "\u5357\u4eac": "101190101", "\u82cf\u5dde": "101190401", "\u6606\u5c71": "101190404", "\u5357\u901a": "101190501", "\u592a\u4ed3": "101190408", "\u5434\u53bf": "101190406", "\u5f90\u5dde": "101190801", "\u5b9c\u5174": "101190203", "\u9547\u6c5f": "101190301", "\u6dee\u5b89": "101190901", "\u5e38\u719f": "101190402", "\u76d0\u57ce": "101190701", "\u6cf0\u5dde": "101191201", "\u65e0\u9521": "101190201", "\u8fde\u4e91\u6e2f": "101191001", "\u626c\u5dde": "101190601", "\u5e38\u5dde": "101191101", "\u5bbf\u8fc1": "101191301", "\u5408\u80a5": "101220101", "\u5de2\u6e56": "101221601", "\u868c\u57e0": "101220201", "\u5b89\u5e86": "101220601", "\u516d\u5b89": "101221501", "\u6ec1\u5dde": "101221101", "\u9a6c\u978d\u5c71": "101220501", "\u961c\u9633": "101220801", "\u5ba3\u57ce": "101221401", "\u94dc\u9675": "101221301", "\u6dee\u5317": "101221201", "\u829c\u6e56": "101220301", "\u4eb3\u5dde": "101220901", "\u5bbf\u5dde": "101220701", "\u6dee\u5357": "101220401", "\u6c60\u5dde": "101221701", "\u897f\u5b89": "101110101", "\u97e9\u57ce": "101110510", "\u5b89\u5eb7": "101110701", "\u6c49\u4e2d": "101110801", "\u5b9d\u9e21": "101110901", "\u54b8\u9633": "101110200", "\u6986\u6797": "101110401", "\u6e2d\u5357": "101110501", "\u5546\u6d1b": "101110601", "\u94dc\u5ddd": "101111001", "\u5ef6\u5b89": "101110300", "\u94f6\u5ddd": "101170101", "\u56fa\u539f": "101170401", "\u4e2d\u536b": "101170501", "\u77f3\u5634\u5c71": "101170201", "\u5434\u5fe0": "101170301", "\u5170\u5dde": "101160101", "\u767d\u94f6": "101161301", "\u5e86\u9633": "101160401", "\u9152\u6cc9": "101160801", "\u5929\u6c34": "101160901", "\u6b66\u5a01": "101160501", "\u5f20\u6396": "101160701", "\u7518\u5357": "101050204", "\u4e34\u590f": "101161101", "\u5e73\u51c9": "101160301", "\u5b9a\u897f": "101160201", "\u91d1\u660c": "101160601", "\u897f\u5b81": "101150101", "\u6d77\u5317": "101150801", "\u6d77\u897f": "101150701", "\u9ec4\u5357": "101150301", "\u679c\u6d1b": "101150501", "\u7389\u6811": "101150601", "\u6d77\u4e1c": "101150201", "\u6d77\u5357": "101150401", "\u6b66\u6c49": "101200101", "\u5b9c\u660c": "101200901", "\u9ec4\u5188": "101200501", "\u6069\u65bd": "101201001", "\u8346\u5dde": "101200801", "\u795e\u519c\u67b6": "101201201", "\u5341\u5830": "101201101", "\u54b8\u5b81": "101200701", "\u8944\u9633": "101200201", "\u5b5d\u611f": "101200401", "\u968f\u5dde": "101201301", "\u9ec4\u77f3": "101200601", "\u8346\u95e8": "101201401", "\u9102\u5dde": "101200301", "\u957f\u6c99": "101250101", "\u90b5\u9633": "101250901", "\u5e38\u5fb7": "101250601", "\u90f4\u5dde": "101250501", "\u5409\u9996": "101251501", "\u682a\u6d32": "101250301", "\u5a04\u5e95": "101250801", "\u6e58\u6f6d": "101250201", "\u76ca\u9633": "101250701", "\u6c38\u5dde": "101251401", "\u5cb3\u9633": "101251001", "\u8861\u9633": "101250401", "\u6000\u5316": "101251201", "\u97f6\u5c71": "101250202", "\u5f20\u5bb6\u754c": "101251101", "\u676d\u5dde": "101210101", "\u6e56\u5dde": "101210201", "\u91d1\u534e": "101210901", "\u5b81\u6ce2": "101210401", "\u4e3d\u6c34": "101210801", "\u7ecd\u5174": "101210501", "\u8862\u5dde": "101211001", "\u5609\u5174": "101210301", "\u53f0\u5dde": "101210601", "\u821f\u5c71": "101211101", "\u6e29\u5dde": "101210701", "\u5357\u660c": "101240101", "\u840d\u4e61": "101240901", "\u4e5d\u6c5f": "101240201", "\u4e0a\u9976": "101240301", "\u629a\u5dde": "101240401", "\u5409\u5b89": "101240601", "\u9e70\u6f6d": "101241101", "\u5b9c\u6625": "101240501", "\u65b0\u4f59": "101241001", "\u666f\u5fb7\u9547": "101240801", "\u8d63\u5dde": "101240701", "\u798f\u5dde": "101230101", "\u53a6\u95e8": "101230201", "\u9f99\u5ca9": "101230701", "\u5357\u5e73": "101230901", "\u5b81\u5fb7": "101230301", "\u8386\u7530": "101230401", "\u6cc9\u5dde": "101230501", "\u4e09\u660e": "101230801", "\u6f33\u5dde": "101230601", "\u8d35\u9633": "101260101", "\u5b89\u987a": "101260301", "\u8d64\u6c34": "101260208", "\u9075\u4e49": "101260201", "\u94dc\u4ec1": "101260601", "\u516d\u76d8\u6c34": "101260801", "\u6bd5\u8282": "101260701", "\u51ef\u91cc": "101260501", "\u90fd\u5300": "101260401", "\u6210\u90fd": "101270101", "\u6cf8\u5dde": "101271001", "\u5185\u6c5f": "101271201", "\u51c9\u5c71": "101271601", "\u963f\u575d": "101271901", "\u5df4\u4e2d": "101270901", "\u5e7f\u5143": "101272101", "\u4e50\u5c71": "101271401", "\u7ef5\u9633": "101270401", "\u5fb7\u9633": "101272001", "\u6500\u679d\u82b1": "101270201", "\u96c5\u5b89": "101271701", "\u5b9c\u5bbe": "101271101", "\u81ea\u8d21": "101270301", "\u7518\u5b5c\u5dde": "101271801", "\u8fbe\u5dde": "101270601", "\u8d44\u9633": "101271301", "\u5e7f\u5b89": "101270801", "\u9042\u5b81": "101270701", "\u7709\u5c71": "101271501", "\u5357\u5145": "101270501", "\u5e7f\u5dde": "101280101", "\u6df1\u5733": "101280601", "\u6f6e\u5dde": "101281501", "\u97f6\u5173": "101280201", "\u6e5b\u6c5f": "101281001", "\u60e0\u5dde": "101280301", "\u6e05\u8fdc": "101281301", "\u4e1c\u839e": "101281601", "\u6c5f\u95e8": "101281101", "\u8302\u540d": "101282001", "\u8087\u5e86": "101280901", "\u6c55\u5c3e": "101282101", "\u6cb3\u6e90": "101281201", "\u63ed\u9633": "101281901", "\u6885\u5dde": "101280401", "\u4e2d\u5c71": "101281701", "\u5fb7\u5e86": "101280905", "\u9633\u6c5f": "101281801", "\u4e91\u6d6e": "101281401", "\u73e0\u6d77": "101280701", "\u6c55\u5934": "101280501", "\u4f5b\u5c71": "101280800", "\u5357\u5b81": "101300101", "\u6842\u6797": "101300501", "\u9633\u6714": "101300510", "\u67f3\u5dde": "101300301", "\u68a7\u5dde": "101300601", "\u7389\u6797": "101300901", "\u6842\u5e73": "101300802", "\u8d3a\u5dde": "101300701", "\u94a6\u5dde": "101301101", "\u8d35\u6e2f": "101300801", "\u9632\u57ce\u6e2f": "101301401", "\u767e\u8272": "101301001", "\u5317\u6d77": "101301301", "\u6cb3\u6c60": "101301201", "\u6765\u5bbe": "101300401", "\u5d07\u5de6": "101300201", "\u6606\u660e": "101290101", "\u4fdd\u5c71": "101290501", "\u695a\u96c4": "101290801", "\u5fb7\u5b8f": "101291501", "\u7ea2\u6cb3": "101290301", "\u4e34\u6ca7": "101291101", "\u6012\u6c5f": "101291201", "\u66f2\u9756": "101290401", "\u601d\u8305": "101290901", "\u6587\u5c71": "101290601", "\u7389\u6eaa": "101290701", "\u662d\u901a": "101291001", "\u4e3d\u6c5f": "101291401", "\u5927\u7406": "101290201", "\u6d77\u53e3": "101310101", "\u4e09\u4e9a": "101310201", "\u510b\u5dde": "101310205", "\u743c\u5c71": "101310102", "\u901a\u4ec0": "101310222", "\u6587\u660c": "101310212", "\u4e4c\u9c81\u6728\u9f50": "101130101", "\u963f\u52d2\u6cf0": "101131401", "\u963f\u514b\u82cf": "101130801", "\u660c\u5409": "101130401", "\u54c8\u5bc6": "101131201", "\u548c\u7530": "101131301", "\u5580\u4ec0": "101130901", "\u514b\u62c9\u739b\u4f9d": "101130201", "\u77f3\u6cb3\u5b50": "101130301", "\u5854\u57ce": "101131101", "\u5e93\u5c14\u52d2": "101130601", "\u5410\u9c81\u756a": "101130501", "\u4f0a\u5b81": "101131001", "\u62c9\u8428": "101140101", "\u963f\u91cc": "101140701", "\u660c\u90fd": "101140501", "\u90a3\u66f2": "101140601", "\u65e5\u5580\u5219": "101140201", "\u5c71\u5357": "101140301", "\u6797\u829d": "101140401", "\u53f0\u5317": "101340101", "\u9ad8\u96c4": "101340201", "\u9999\u6e2f": "101320101", "\u6fb3\u95e8": "101330101"};
var city_code = function (city) {
    if(city.substr(-1) === '市'){
                city = city.substring(0,city.length-1)
            }
            var code = city_code_obj[city];
            log(code);
            socket.emit('city_code',{'city_dode': code});
};


// 根据地址显示天气 todo
var get_weather = function () {
    socket.on('weather',function (data) {
        log(data)
    })
}


var weather = function () {
    $(document).ready(function () {
        get_city(function (p, c) {
            city_code(c);
        });
        get_weather()
    })
};

weather();