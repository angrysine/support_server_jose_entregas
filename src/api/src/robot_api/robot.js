const client_user = new net.Socket()

function sand(msg) {
        try {
            client_user.connect(4000, '127.0.0.1', () =>{
                client_user.write(msg)
            })
        } catch (error) {
            console.log(error)
        }
}