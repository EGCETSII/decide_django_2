import React, { Component } from 'react';
import { Alert, Button, Text, TextInput, View } from 'react-native';
import config from '../config.json';
import { postData } from '../utils';
import { StyleSheet} from "react-native";


export default class Login extends Component {

    state = {
        form: {
            username: '',
            password: ''
        },
        error: false

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
                this.setState({error:true})
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
                this.setState({error:true})
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
                <View style={styles.html}>
                    <View style={styles.body}>
                      <View style={styles.container}>                            
                            <View style={styles.content}>
                                <View style={styles.row}>
                                    <View style={styles.span14}>
                                        <View style={styles.clearfix}>
                                            <View>
                                                <Text style={styles.title}>Usuario</Text>
                                            </View>
                                            <View>
                                                <TextInput id='username'  name="username" hint="username" style={styles.input} onChangeText={(val) => this.handleChange('username', val)} placeholder="Introduce tu usuario"></TextInput>
                                            </View>
                                            <View>
                                                <Text style={styles.title}>Contraseña</Text>
                                            </View>
                                            <View>
                                                <TextInput id='password' name="password" hint="password" style={styles.input} secureTextEntry={true} onChangeText={(val) => this.handleChange('password', val)} placeholder="Introduce tu contraseña"></TextInput>
                                            </View>
                                        </View>
                                        <View style={styles.btnprimary}>
                                            <Button id='button' color="linear-gradient(top, #049cdb, #0064cd)" onPress={this.onSubmitLogin} title="Login" />
                                        </View>
                                    </View>
                                </View>
                            </View>
                        </View>
                    </View>
                </View>
                {this.state.error && <View style={{paddingTop:10, paddingBottom:7}}>
                <Text style={{fontWeight: 'bold', color:'rgb(192,26,26)', fontFamily: 'calibri', fontSize:'15px'}}>El usuario introducido no existe</Text>
                </View>}
            </View>
        );
    }
}

const styles = StyleSheet.create({
    html: {
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    body: {
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "paddingTop": 40,
        "fontFamily": "\"Helvetica Neue\",Helvetica,Arial,sans-serif",
        "fontSize": 18,
        "fontWeight": "normal",
        "lineHeight": 24
    },
    container: {
        "width": "100%",
        "minHeight": "100vh",
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "alignItems": "center"
    },
    content: {
        "width": 960,
        "backgroundColor": "#fff",
        "borderTopLeftRadius": 10,
        "borderTopRightRadius": 10,
        "borderBottomRightRadius": 10,
        "borderBottomLeftRadius": 10,
        "overflow": "hidden",
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "space-between",
        "paddingTop": 50,
        "paddingRight": 50,
        "paddingBottom": 50,
        "paddingLeft": 50
    },
    row: {
    },
    clearfix: {
        "marginBottom": 24,
    },
    input: {
        "fontSize": 15,
        "lineHeight": 1,
        "color": "#666666",
        "width": "100%",
        "backgroundColor": "#e6e6e6",
        "height": 50,
        "borderTopLeftRadius": 25,
        "borderTopRightRadius": 25,
        "borderBottomRightRadius": 25,
        "borderBottomLeftRadius": 25,
        "paddingTop": 0,
        "paddingRight": 30,
        "paddingBottom": 0,
        "paddingLeft": 68
    },
    btnprimary: {
        "width": "100%",
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "fontSize": 18,
        "lineHeight": 1.5,
        "color": "#fff",
        "textTransform": "uppercase",
        "height": 50,
        "borderTopLeftRadius": 25,
        "borderTopRightRadius": 25,
        "borderBottomRightRadius": 25,
        "borderBottomLeftRadius": 25,
        "backgroundColor": "#0064cd",
        "paddingTop": 0,
        "paddingRight": 25,
        "paddingBottom": 0,
        "paddingLeft": 25,
        "textShadowOffset": {
          "width": 0,
          "height": -1
        },
        "textShadowRadius": 0,
        "textShadowColor": "rgba(0, 0, 0, 0.25)",
        "borderTopColor": "#0064cd",
        "borderRightColor": "#0064cd",
        "borderBottomColor": "#003f81",
        "borderLeftColor": "#0064cd"
    },
    actions: {

    },
    title: {
        "fontSize": 24,
        "fontWeight": "bold",
        "color": "#333333",
        "lineHeight": 1.2,
        "textAlign": "center",
        "width": "100%",
        "paddingTop": 30,
        "paddingRight": 30,
        "paddingBottom": 30,
        "paddingLeft": 30
    }
  });