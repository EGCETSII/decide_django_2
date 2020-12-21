import React from 'react'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

function Barra(props){
    return(
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="#home">Decide votacion</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
                <Nav.Link href="#home">Home</Nav.Link>
                <Nav.Link href="#link">Link test</Nav.Link>
            </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Barra;
