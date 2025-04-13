import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'

function ChatBox(){
    return(
        <>
        
        <div className=' rounded-4 p-2 mb-5 bg-light sticky-bottom' style={{width:'100%'}}>
            <FloatingLabel controlId="message" label="Message">
                    <Form.Control
                    as="textarea"
                    style={{ height: '130px', resize: 'none'}}
                    className='bg-light overflow-y'
                    />
                    <Button className="material-symbols-outlined">send</Button>
            </FloatingLabel>
        </div>

        
        </>
    )

}

export default ChatBox;