import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';

function ChatBox(){
    return(
        <>
        
        <div className='border rounded-4 p-2 mb-3 mx-5 position-fixed bottom-0 start-50 translate-middle-x ' style={{width:'60vw'}}>

            <FloatingLabel controlId="message" label="Message">
                    <Form.Control
                    as="textarea"
                    style={{ height: '150px', resize: 'none'}}
                    className='bg-light overflow-y'
                    />
            </FloatingLabel>
        </div>

        
        </>
    )

}

export default ChatBox;