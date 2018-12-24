$(document).ready(function() {

        //Khi bàn phím được nhấn và thả ra thì sẽ chạy phương thức này
        $("#formDemo").validate({
            rules: {
                name: "required",
                adano: "required",
                adapass: {
                    required: true,
                    maxlength: 8
                },
                cadapass: {
                    required: true,
                    maxlength: 8,
                    equalTo: "#adapass"
                },
                email: {
                    required: true,
                    email: true
                },
                admincode: {
                    required: true,
                    maxlength: 8,
                    equalTo: '#admincodehidden'
                }
            },
            messages: {
                name: "Tài khoản không quá 8 ký tự",
                adano: "Vui lòng nhập mã ADA",
                adapass: {
                    required: "Vui lòng nhập mật khẩu",
                    maxlength: "Mật khẩu chỉ được 8 ký tự"
                },
                cadapass: {
                    required: "Vui lòng nhập lại mật khẩu",
                    maxlength: "Mật khẩu chỉ được 8 ký tự",
                    equalTo: 'Mật khẩu không trùng'
                },
                email: {
                    required: "Vui lòng nhập email",
                    email: "Vui lòng nhập đúng định dạng email"
                },
                admincode: {
                    required: "Vui lòng nhập Mã quản lý",
                    maxlength: "Mã quản lý chỉ 8 ký tự",
                    equalTo: 'Bạn nhập sai. Vui lòng liên hệ BQT Website'
                }
            }
        });
    });