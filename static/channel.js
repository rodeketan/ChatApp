

document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    socket.on('connect', () => {


        socket.emit('joined');


        document.querySelector('#newChannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });


        document.querySelector('#leave').addEventListener('click', () => {


            socket.emit('left');

            localStorage.removeItem('last_channel');
            window.location.replace('/');
        });


        document.querySelector('#logout').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });


        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });


        document.querySelector('#send-button').addEventListener("click", () => {


            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();


            let msg = document.getElementById("comment").value;

            socket.emit('send message', msg, timestamp);


            document.getElementById("comment").value = '';
        });




    });


    socket.on('status', data => {


        let row = '<' + `${data.msg}` + '>'
        document.querySelector('#chat').value += row + '\n';


        localStorage.setItem('last_channel', data.channel)
    })


    socket.on('announce message', data => {

    
        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
        document.querySelector('#chat').value += row + '\n'

    })


    var private_socket = io('http://127.0.0.1:5000/private')


    $('#send_private_message').on('click', function() {


        var recipient = $('#send_to_username').val();
        var message_to_send = $('#private_message').val();

        private_socket.emit('private_message', {'username' : recipient, 'message' : message_to_send});
    });

    private_socket.on('new_private_message', function(data) {
      // alert(`${data.msg}`)
      let row ='[' + `${data.user}` + ']:  ' + `${data.msg}`
      document.querySelector('#private').value += row + '\n'

    });



});
