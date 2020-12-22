import React, { Component } from 'react';
// import Navbar from 'react-bootstrap/Navbar';
// import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import Label from 'react-bootstrap/FormLabel';
import Control from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import FormGroup from 'react-bootstrap/FormGroup';
import axios from 'axios';
import Barra from './Barra';


export default class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            urlLogin : window.urlLogin,
            urlStore : window.urlStore,
            urlGetUser : window.urlGetUser,
            voting : window.votingData,
            selected : '',
            alertShow : false,
            alertMsg : '',
            alertLvl : 'info',
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
        this.postData(this.state.urlLogin, this.state.form)
            .then(data => {
                document.cookie = 'decide='+data.token+'; Secure';
                this.props.setToken(data.data.token);
                this.getUser();
            })
            .catch(error => {
                this.showAlert('danger', 'Error: ' + error);
            });
    }
      

    getUser() {
        var token = {
            token: this.props.token
        };
        
        this.postData(this.state.urlGetUser, token)
            .then(response => {
                this.props.setUser(response.data);
                this.props.setSignup(false);
            }).catch(error => {
                this.showAlert('danger', 'Error: ' + error);
            });
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
  
    showAlert(lvl, msg) {
        this.setState({alertLvl: lvl});
        this.setState({alertMsg: msg});
        this.setState({alertShow: true});
        console.log(this.state.alertLvl,'MSG', this.state.alertMsg, 'Show', this.state.alertShow)
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
            <div>
                <Form>
                    <FormGroup >
                        <Label>Usuario</Label>
                        <Control type="text" name="username" onChange={this.handleChange} placeholder="Introduce tu usuario"></Control>
                    </FormGroup>
                    <FormGroup>
                        <Label>Contraseña</Label>
                        <Control type="password" name="password" onChange={this.handleChange} placeholder="Introduce tu contraseña"></Control>
                    </FormGroup>
                    <Button type="submit" onClick={this.onSubmitLogin}>
                        Entrar
                    </Button>
                    <br/>
                    {this.state.alertShow === true ? <span  style={{fontSize:"12px", color:"red"}}>Usuario incorrecto</span> :<span/>}
                </Form>
            </div>
        );
    }
}
