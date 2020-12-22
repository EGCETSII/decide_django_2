import React, { Component } from 'react';
import axios from 'axios';
import './Login.css';


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
            <div className="html">
                <div className="body">
                    <div className="container">
                        <div className="content">
                            <div className="row">
                                <div className="span14">
                                    <div className="clearfix">

                                                        <label>Usuario</label>
                                                        <div className="input">
                                                            <input type="text" name="username" onChange={this.handleChange} placeholder="Introduce tu usuario"/>
                                                        </div>
                                                        <label>Contraseña</label>
                                                        <div className="input">
                                                            <input type="password" name="password" onChange={this.handleChange} placeholder="Introduce tu contraseña"/>
                                                        </div>
                                    </div>
                                    <div className="actions">
                                        
                                                    <button type="subm+it" className="btn-primary" onClick={this.onSubmitLogin}>
                                                        Entrar
                                                    </button>
                                                    <br/>
                                                    {this.state.alertShow === true ? <span  style={{fontSize:"12px", color:"red"}}>Usuario incorrecto</span> :<span/>}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
