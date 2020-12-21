import React, { Component } from 'react';
// import Navbar from 'react-bootstrap/Navbar';
// import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import Label from 'react-bootstrap/FormLabel';
import Control from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import FormGroup from 'react-bootstrap/FormGroup';
import axios from 'axios';

export default class Login extends Component {


    constructor(props) {
        super(props);
        this.state = {
            urlLogin : window.urlLogin,
            urlStore : window.urlStore,
            urlGetUser : window.urlGetUser,
            urlLogout : window.urlLogout,
            voting : window.votingData,
            selected : '',
            signup : true,
            alertShow : false,
            alertMsg : '',
            alertLvl : 'info',
            token : null,
            user : null,
            form : {
                username: '',
                password: ''
            }
        };

        this.onSubmitLogin = this.onSubmitLogin.bind(this);
        this.getUser = this.getUser.bind(this);
        this.postData = this.postData.bind(this);
        this.showAlert = this.showAlert.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    onSubmitLogin(event) {
        event.preventDefault();
        console.log(this.state.form);

        this.postData(this.state.urlLogin, this.state.form)
            .then(data => {
                document.cookie = 'decide='+data.token+'; Secure';
                this.setState({token: data.data.token});
                console.log(this.state.token);
                this.getUser();
            })
            .catch(error => {
                this.showAlert('danger', 'Error: ' + error);
            });
    }
      

    getUser() {
        var token = {
            token: this.state.token
        }; 
        this.postData(this.state.urlGetUser, token)
            .then(response => {
                this.props.setCurrentUser(response.data);
            }).catch(error => {
                this.showAlert('danger', 'Error: ' + error);
            });
    }
  

    postData(url, data) {
    // Default options are marked with *
        var headers = {
            'content-type': 'application/json',
        };
        if (this.state.token) {
            headers['Authorization'] = 'Token ' + this.state.token;
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
  
    showAlert(lvl, msg) {
        this.setState({alertLvl: lvl});
        this.setState({alertMsg: msg});
        this.setState({alertShow: true});
    }

    handleChange(event) {
        this.setState(
            {
                form: {
                    ...this.state.form,
                    [event.target.name]: event.target.value
                }
            }
        );
    }

    render() {
        return (
            <Form>
                <FormGroup >
                    <Label>Usuario</Label>
                    <Control type="text" name="username" onChange={this.handleChange} placeholder="Introduce tu usuario"></Control>
                </FormGroup>
                <FormGroup>
                    <Label>Contraseña</Label>
                    <Control type="password" name="password" onChange={this.handleChange} placeholder="Introduce tu contraseña"></Control>
                </FormGroup>
                <Button onClick={this.onSubmitLogin}>
                    Submit
                </Button>
            </Form>
        );
    }
}
