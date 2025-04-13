

import React from 'react'
import ReactMarkdown from 'react-markdown'


function ChatMessages({ message, isUser }) {
  return (
    <>

<div className={`d-flex pb-5 ${isUser ? "justify-content-end" : "justify-content-start"}`}>
      <div
        className={`pt-2 px-2 shadow-sm ${isUser ? "bg-primary text-white" : "bg-light text-dark"}`}
        style={{ maxWidth: "47%", borderRadius:"5px", lineHeight:"1.8rem" }}
      >
        <ReactMarkdown>{message}</ReactMarkdown>
      </div>
    </div>
    </>
  )
}

export default ChatMessages;