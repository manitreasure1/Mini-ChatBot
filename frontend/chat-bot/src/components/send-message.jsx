import {io} from 'socket.io-client'
import { useEffect } from 'react'


function SendMessage({message}) {
    const socket = io(import.meta.env.VITE_SOCKET_SERVER_URL);

    useEffect(()=>{
        socket.on('recieve_message', (data)=>{
            if (data.sender === "client") {
                console.log("You:", data.message);
              } else if (data.sender === "bot") {
                console.log("AI Bot:", data.message);
              }
        })
        socket.on("error", (error) => {
            console.error("Error:", error.error);
          });
        return ()=> {
            socket.off('recieve_message');
            socket.off('error');
            socket.disconnect();
        }
    }, [socket]);

    useEffect(() => {
        if (message) {
            socket.emit("send_message", { message });
        }
    }, [message, socket]);


  return (
    <div>

    </div>
  )
}

export default SendMessage;