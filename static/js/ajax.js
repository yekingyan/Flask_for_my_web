var log = function() {
    console.log.apply(console, arguments)
};

// 简化选择器
var e = function(sel) {
    return document.querySelector(sel)
};

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    // 创建 XMLHttpRequest 对象
    var r = new XMLHttpRequest();
    // 设置请求方法和请求地址，第三个参数，是否使用异步
    r.open(method, path, true);
    // 设置请求的头
    r.setRequestHeader('Content-Type', 'application/json');
    // 注册响应函数，获捉事件变化
    r.onreadystatechange = function() {
        // readyState为4的时候是一个响应，表求请求已经收到了服务器的响应
        if(r.readyState === 4) {
            responseCallback(r.response)
            // {ct: "20180916-16:27:31", id: 18, title: "test ajax"}
        }
    };
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data);
    // 发送请求
    r.send(data)
};

// 增加一个 todo
var apiTodoAdd = function(form, callback) {
    var path = '/todo/add';
    ajax('POST', path, form, callback)
};

// 插入的模板
var todoTemplate = function(todo) {
    var title = todo.title;
    var id = todo.id;
    var ct = todo.ct;
    var ids = document.querySelectorAll('[scope="row"]');
    var index = ids.length + 1
    var t = `
        <tr class="table-warning">
        <td class="d-none">${id}</td>
        <td scope="row">${index}</td>
        <td>${title}</td><td>${ct}</td>
        <td><a id ="${id}" class="btn btn-danger" href="#">delete</a></td>
        </tr>
    `;
    return t;
};

//添加一个todo
var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo);
    var todoList = e('tbody');
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

//绑定添加事件
var bindEventTodoAdd = function() {
    var b = e('#submit');
    b.addEventListener('click', function(){
        var input = e('input[name="title"]');
        var title = input.value;
        log('click add', title);
        var form = {
            'title': title,
        };
        apiTodoAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r);
            insertTodo(todo);
        });
    });
};

// main
var run = function() {
    bindEventTodoAdd();
};


window.onload = function(){
    run()
};