import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';

function ChatBox(){
    return(
        <>
        
        <div className='border rounded-4 p-2 mb-3 bg-light sticky-bottom' style={{width:'100%'}}>

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