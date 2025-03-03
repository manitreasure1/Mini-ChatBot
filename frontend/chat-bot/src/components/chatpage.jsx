import React from 'react'
import ChatMessages from './chatmessages';
import ChatBox from './chatbox';
import SideNav from './sidenav';
import { useState } from 'react';

function ChatPage({messages}) {
    const [sideNavWidth, setSideNavWidth] = useState('7%');

    const handleSideNavToggle = (isExpanded) => {
        setSideNavWidth(isExpanded ? '25%' : '7%');
    };
  return (
    <>
    <div className='d-flex flex-column' style={{height:'100vh'}}>

        <SideNav onToggle={handleSideNavToggle}/>
        <div className='d-flex flex-column' style={{width: `calc(80% - ${sideNavWidth})`, transition:'width 0.5s', margin:'0 10% 0 auto'}} >
            <div className="d-flex flex-column" style={{overflowY:'hidden' }}>
                <div className=' mt-3  d-flex flex-column' style={{overflowY:'auto'}}>
                    {messages.map((msg, index) => (
                        <ChatMessages key={index} message={msg.content} isUser={msg.role === "user"} />
                    ))}
                </div>
            </div>
            <ChatBox/>
        </div>
    </div>
    </>
  )
}
export default ChatPage;



