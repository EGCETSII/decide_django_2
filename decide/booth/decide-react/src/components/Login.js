import React, { Component } from 'react';
import { Alert, Button, Text, TextInput, View } from 'react-native';
import config from '../config.json';
import { postData } from '../utils';

export default class Login extends Component {

    state = {
        form: {
            username: '',
            password: ''
        }
    }

    onSubmitLogin = () => {
        const { setToken, handleSetStorage } = this.props;
        postData(config.LOGIN_URL, this.state.form)
            .then(response => {
                handleSetStorage("decide", response.data.token)
                setToken(response.data.token)
                this.getUser();
            })
            .catch(error => {
                Alert.alert(`Error: ${error}`);
            });
    }    

    getUser = () => {
        const { token, setUser, setSignup } = this.props;
        const data = {
            token
        };
        
        postData(config.GETUSER_URL, data, token)
            .then(response => {
                setUser(response.data);
                setSignup(false);
            }).catch(error => {
                Alert.alert(`Error: ${error}`);
            });
    }
  
    handleChange = (name, value) => {        
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
                    <TextInput onChangeText={(val) => this.handleChange('username', val)} placeholder="Introduce tu usuario"></TextInput>
                </View>
                <View>
                    <Text>Contraseña</Text>
                    <TextInput secureTextEntry={true} onChangeText={(val) => this.handleChange('password', val)} placeholder="Introduce tu contraseña"></TextInput>
                </View>
                <Button  onPress={this.onSubmitLogin} title="Login" />
            </View>
        );
    }
}
