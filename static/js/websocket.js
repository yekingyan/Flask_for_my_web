// 连接的实例
var socket = io.connect('http://' + document.domain + ':' + location.port);


socket.on('connect', function () {
    console.log('connect');
    socket.emit('connect_event', {data: 'I\'m connected!'});
});


socket.on('server_response', function (msg) {
    console.log(msg);
});
