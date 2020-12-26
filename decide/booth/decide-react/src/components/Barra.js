import React, {Component} from 'react';
import { StatusBar, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';

export default class Barra extends Component{

    logout = () => {
        const {token, setToken, setUser, setSignup } = this.props;
        const data = {token};  

        postData(config.LOGOUT_URL, data, token);
        setToken(null);
        setUser(null);
        this.props.handleSetStorage("decide", "")
        setSignup(true);
    }

    render(){
        const statusHeight = StatusBar.currentHeight ? StatusBar.currentHeight : 0;

        return(
            <View style={{                    
                width: '100%',
                backgroundColor: 'rgb(7, 7, 76)',
                justifyContent: 'space-between',
                paddingHorizontal: 20,
                paddingTop: statusHeight + 15,
                paddingBottom: 15,
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center'}}>
                <View>
                    <Text style={{color:'white', fontSize: 18}}>DecideHueznar</Text>
                </View>
                {!this.props.signup && <View>
                    <Text style={{color:'white'}} onPress={this.logout}>Logout</Text>
                </View>}
            </View>
        );
    }
}
