import React, { Component } from 'react';
import axios from 'axios';
import { Alert, Button, Text, TextInput, View } from "react-native";


export default class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            urlLogin : "http://localhost:8000/authentication/login/",
            urlStore : window.urlStore,
            urlGetUser : "http://localhost:8000/authentication/getuser/",
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

    onSubmitLogin() {
        console.log(this.state.form)
        this.postData(this.state.urlLogin, this.state.form)
            .then(data => {
                // document.cookie = 'decide='+data.token+'; Secure';
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
        // console.log(this.state.alertLvl,'MSG', this.state.alertMsg, 'Show', this.state.alertShow)
    }

    handleChange(name, value) {
        
        this.setState(
            {
                form: {
                    ...this.state.form,
                    [name]: value
                }
            }
        );
    }

    render() {
        return (
            <View>
                <View>
                    <Text>Usuario</Text>
                    <TextInput onChangeText={(val) => this.handleChange("username", val)} placeholder="Introduce tu usuario"></TextInput>
                </View>
                <View>
                    <Text>Contraseña</Text>
                    <TextInput secureTextEntry={true} onChangeText={(val) => this.handleChange("password", val)} placeholder="Introduce tu contraseña"></TextInput>
                </View>
                <Button  onPress={this.onSubmitLogin} title="Login" />
            </View>
        );
    }
}
