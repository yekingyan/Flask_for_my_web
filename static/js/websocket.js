var log = function () {
    console.log.apply(console, arguments)
};

// 连接的实例
var socket = io.connect('http://' + document.domain + ':' + location.port);


socket.on('connect', function () {
    console.log('connect');
    socket.emit('connect_event', {data: 'I\'m connected!'});
});


socket.on('server_response', function (msg) {
    console.log(msg);
});

// 发送输入框的内容
var input = function () {
    $('#submit').click(function () {
        log('submit:', $('input')[1].value);
        socket.emit('client_event', {data: $('input')[1].value});
        return false;
    });
};



var main = function () {
    $(document).ready(function () {
        input();
    });
};
main();