var log = function () {
    console.log.apply(console, arguments)
};

// 简化选择器
var e = function (sel) {
    return document.querySelector(sel)
};

/*
 ajax 函数
*/
var ajax = function (method, path, data, responseCallback) {
    // 创建 XMLHttpRequest 对象
    var r = new XMLHttpRequest();
    // 设置请求方法和请求地址，第三个参数，是否使用异步
    r.open(method, path, true);
    // 设置请求的头
    r.setRequestHeader('Content-Type', 'application/json');
    // 注册响应函数，获捉事件变化
    r.onreadystatechange = function () {
        // readyState为4的时候是一个响应，表求请求已经收到了服务器的响应
        if (r.readyState === 4) {
            responseCallback(r.response)
            // {ct: "20180916-16:27:31", id: 18, title: "test ajax"}
        }
    };
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data);
    // 发送请求
    r.send(data)
};

// 增加一个todo到服务器
var apiTodoAdd = function (form, responseCallback) {
    var path = '/todo/add';
    ajax('POST', path, form, responseCallback)
};

// 插入的模板
var todoTemplate = function (todo) {
    var title = todo.title;
    var id = todo.id;
    var ct = todo.ct;
    var ids = document.querySelectorAll('[scope="row"]');
    var index = ids.length + 1;
    var t = `
        <tr class="table-warning">
        <td class="d-none">${id}</td>
        <td scope="row">${index}</td>
        <td>${title}</td><td>${ct}</td>
        <td><a id ="todo-${id}" class="btn btn-danger" href="#">delete</a></td>
        </tr>
    `;
    return t;
};


//添加一个todo到html中
var insertTodo = function (todo) {
    var todoCell = todoTemplate(todo);
    var todoList = e('tbody');
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

// flash
var flashTemplate = function (todo) {
    var flash = todo.flash;
    var t = `
        <div class="alert alert-dismissible fade show alert-info" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
            </button>
            <strong>${flash}</strong>
        </div>
    `;
    return t
}

var insertFlash = function (todo) {
    var nav = e('nav');
    var flash = flashTemplate(todo);
    nav.insertAdjacentHTML('afterend', flash)
};


//绑定添加事件
var bindEventTodoAdd = function () {
    var b = e('#submit');
    b.addEventListener('click', function () {
        var input = e('input[name="title"]');
        var title = input.value;
        // log('click add', title);
        var form = {
            'title': title,
        };
        apiTodoAdd(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r);
            if (todo.status === 200) {
                insertTodo(todo);
                log("成功新增：", todo.id, todo.title)
            }
            else {
                insertFlash(todo)
            }
        });
    });
};

// 删除一个todo到服务器
var apiTodoDelete = function (id, responseCallback) {
    var url = '/todo/delete/';
    ajax('get', url + id, null, responseCallback)
};

// 新增的不能删除，可能是循环问题，亦可能是没有监听父节点的问题
var bindEvenTodoDelete = function () {
    var deletes = document.querySelectorAll('.btn-danger');
    for (var i = 0; i < deletes.length; i++) {
        deletes[i].addEventListener('click', function (event) {
            self = event.target;
            var id = self.getAttribute("id");
            // console.log(id);
            id = id.slice(5);
            apiTodoDelete(id, function (r) {
                tr = self.parentElement.parentElement;
                tr.remove();
                log('成功删除：', r.response)
            })
        })
    }
    ;
};


var bindEvenTodoDelete2 = function () {
    deletes = e('tbody');
    deletes.addEventListener('click', function (event) {
        var self = event.target;
        if (self.classList.contains('btn-danger')) {
            var tr = self.parentElement.parentElement;
            var id = self.getAttribute("id");
            // log(id);
            id = id.slice(5);
            apiTodoDelete(id, function (r) {
                // tr.remove();
                var todo = JSON.parse(r);
                if (todo.status === 200) {
                    tr.remove();
                    log('成功删除：', todo.id, todo.title)
                }
                else {
                    insertFlash(todo)
                }
            })
        }
    })
};


// main
var run = function () {
    bindEventTodoAdd();
    bindEvenTodoDelete2();
};


window.onload = function () {
    run()
};