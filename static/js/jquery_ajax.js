        $(function () {
            //增加
            // 选择用于操作的元素，并绑定事件,如果返回false将取消请求href中的url
            $('#submit').bind('click', function () {
                //$.getJSON(url, data, func)
                //发送一个 GET 请求给 url
                //data 对象的内容将以查询参数的形式发送
                //一旦数据抵达，data将以返回值作为参数执行给定的函数
                $.getJSON($SCRIPT_ROOT + '/todo/add', {
                    title: $('input[name="title"]').val(),
                }, function (data) {
                    // 在页面显示内容
                    var tbody = document.querySelector('tbody');
                    var ids = document.querySelectorAll('[scope="row"]');
                    tbody.insertAdjacentHTML('beforeend', `
                        <tr class="table-warning">
                        <td class="d-none">${data.id}</td>
                        <td scope="row">${ids.length + 1}</td>
                        <td>${data.title}</td><td>${data.ct}</td>

                        <td><a id ="${data.id}" class="btn btn-danger" href="#">delete</a></td>
                        </tr>`
                        // todo/delete/${data.id}
                    );
                });
                return false;
            });

        });


        $(function () {
            //删除
            $('.btn-danger').bind('click', function (event) {
                $.getJSON($SCRIPT_ROOT + `/todo/delete/${$(event.target).attr("id")}`, '',
                    function (data) {
                        // 在页面显示
                        del = $(`#${$(event.target).attr("id")}`).parent().parent();
                        console.log(data.id);
                        del.remove();
                        return false
                        // event.stopPropagation();
                    });
            });
            return false
        });