import React, {Component} from 'react'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button';
import axios from 'axios';


export default class Login extends Component{
    constructor(props) {
        super(props);   
            
    }   

    decideLogout = (event) => {
        event.preventDefault();
        var data = {token: this.props.token};
        this.postData(this.props.urlLogout, data);
        this.props.setToken(null);
        this.props.setUser(null);
        document.cookie = 'decide=;';
        this.props.setSignup(true);
    }

    postData(url, data) {
        // Default options are marked with *
            var headers = {
                'content-type': 'application/json',
            };
            if (this.props.token) {        
                headers['Authorization'] = 'Token ' + this.props.token;
            }
            
            return axios.post(url, data, headers)
                .then(response => {
                    if (response.status === 200) { 
                        return response;
                    } else {
                        return Promise.reject(response.statusText);
                    }
                });
        }

    render(){
        return(
            <Navbar bg="light" expand="lg">
                <Navbar.Brand href="#home">Decide votacion</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="#home">Inicio</Nav.Link>
                    <Nav.Link href="#link">Link test</Nav.Link>
                    {this.props.signup ? <p></p>:<Button onClick={this.decideLogout}>Logout</Button>}
                </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
}
}
