

import React from 'react'
import ReactMarkdown from 'react-markdown'


function ChatMessages({ message, isUser }) {
  return (
    <>

<div className={`d-flex pb-5 ${isUser ? "justify-content-end" : "justify-content-start"}`}>
      <div
        className={`p-3 rounded shadow-sm ${isUser ? "bg-primary text-white" : "bg-light text-dark"}`}
        style={{ maxWidth: "47%" }}
      >
        <ReactMarkdown>{message}</ReactMarkdown>
      </div>
    </div>
    </>
  )
}

export default ChatMessages;