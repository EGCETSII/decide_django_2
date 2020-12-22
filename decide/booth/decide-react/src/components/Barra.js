import React, {Component} from 'react'
import axios from 'axios';
import { Button, StatusBar, Text, View } from 'react-native';


export default class Barra extends Component{
    constructor(props) {
        super(props);   
            
    }   

    decideLogout = (event) => {
        event.preventDefault();
        var data = {token: this.props.token};
        this.postData(this.props.urlLogout, data);
        this.props.setToken(null);
        this.props.setUser(null);
        // document.cookie = 'decide=;';
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
        const statusHeight = StatusBar.currentHeight ? StatusBar.currentHeight : 0;

        return(
            <View style={{
                    
                    width: "100%",
                    backgroundColor: "rgb(7, 7, 76)",
                    justifyContent: "space-between",
                    paddingHorizontal: 20,
                    paddingTop: statusHeight + 15,
                    paddingBottom: 15,
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center"}}>
                <View>
                    <Text style={{color:"white", fontSize: 18}}>DecideHueznar</Text>
                </View>
                {!this.props.signup && <View>
                    <Text style={{color:"white"}} onPress={this.decideLogout}>Logout</Text>
                </View>}
            </View>
        );
}
}
