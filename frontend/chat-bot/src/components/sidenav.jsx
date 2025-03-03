import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import ListGroup from 'react-bootstrap/ListGroup';


function SideNav(){

    const [show, setShow] = useState(false);

    const handleShow = () =>{
      setShow(!show)
    } ;
    return(
        <>      
      <Offcanvas show={true} onHide={handleShow} placement='start' backdrop={false} scroll={true} style={{width: show ? '300px' : '100px', transition: 'width 0.5s'}}>
        <Offcanvas.Header className='mb-4'>
          <Button className='btn btn-light ' onClick={handleShow}>
          <span className="material-symbols-outlined ">menu</span>
          </Button>
        </Offcanvas.Header>
        
        <Offcanvas.Body>
          <ListGroup as="ul" style={{height:'100%'}} className='d-flex flex-column justify-content-between'>

            <Button className='btn btn-light'>
                <span className="material-symbols-outlined align-middle mx-2">
                  add
                </span>
                {show && "New Chat"}
            </Button>
            <div>
              {show && (
                <>
                  <ListGroup.Item action as='li' className='border border-0'>
                    <span className="material-symbols-outlined align-middle mx-3">
                      sort
                    </span>
                  </ListGroup.Item>
                  <ListGroup.Item action as='li' className='border border-0'>
                    <span className="material-symbols-outlined align-middle mx-3">
                      sort
                    </span>
                  </ListGroup.Item>
                  <ListGroup.Item action as='li' className='border border-0'>
                    <span className="material-symbols-outlined align-middle mx-3">
                      sort
                    </span>
                  </ListGroup.Item>
                  <ListGroup.Item action as='li' className='border border-0'>
                    <span className="material-symbols-outlined align-middle mx-3">
                      sort
                    </span>
                  </ListGroup.Item>
                </>
              )}
      
            </div>
            <div>

              <ListGroup.Item action as='li' className='border border-0'>
                <span className="material-symbols-outlined align-middle mx-3">
                  history
                </span>
                {show && "Activity"}
                
              </ListGroup.Item>
              <ListGroup.Item action as='li' className='border border-0'>
                <span className="material-symbols-outlined align-middle mx-3">
                  help
                </span>
                {show && "Help"}
              </ListGroup.Item>
              <ListGroup.Item action as='li' className='border border-0'>
                <span className="material-symbols-outlined align-middle mx-3">
                  settings
                </span>
                {show && "Settings"}
              </ListGroup.Item>
            </div>
        </ListGroup>
        </Offcanvas.Body>
      </Offcanvas>
        
        </>
    )
}

export default SideNav;