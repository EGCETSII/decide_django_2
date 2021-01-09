import React from 'react';
import Barra from './components/Barra';
import Login from './components/Login';
import Voting from './components/Voting';
import {StatusBar, FlatList, Text, TouchableOpacity, View, Button, Alert, SafeAreaView} from 'react-native';
import axios from 'axios';
import config from './config.json';
import { postData } from './utils';
import AsyncStorage from '@react-native-community/async-storage'
import { StyleSheet} from "react-native";


class App extends React.Component {

    state = {
        user: undefined,
        selectedVoting: undefined,
        token: undefined,
        votings: [],
        signup: true,
        done:false
    }

    init = () => {
        this.clearStorage()
        this.handleGetStorage('decide')        
    }

    //Sustituye a la gestión de las cookies
    handleSetStorage = (key, value) => {
        AsyncStorage.setItem(key, value)
    }

    //Sustituye a la gestión de las cookies. Actualiza el estado
    handleGetStorage = (key) => {
        return AsyncStorage.getItem(key).then((decide) =>{
            if (decide != null && decide != ""){
                this.setToken(decide)
                this.getUser(decide);
            }
        });
    }

    clearStorage = () => {
        AsyncStorage.clear
    }

    
    //Get User para la alternativa a las cookies
    getUser = (tokenStorage) => {
        const token = tokenStorage

        const data = {
            token
        };
        
        postData(config.GETUSER_URL, data, token)
            .then(response => {
                this.setUser(response.data);
                this.setSignup(false);
            }).catch(error => {
                alert(`Error: ${error}`);
            });
    }

    setUser = (user2) => {
        this.setState({user:user2});
    }

    setToken = (token2) =>  {
        this.setState({token:token2});
    }

    setSignup = (signup2) =>  {
        this.setState({signup:signup2});
    }

    setSelectedVoting = (voting) => {
        this.setState({selectedVoting: voting});
    }

    setDone = (done2) => {
        this.setState({done:done2});
    }

    loadVotings = () => {
        this.setDone(false)
        axios.get(config.VOTING_URL).then(response => {
            this.setState({votings: response.data});
        });

    }

    componentDidMount() {
        this.loadVotings();   
        this.init();
        this.render();
    }

    render_voting = ({item}) => <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
        <View View style={styles.item}><Text style={styles.sectionHeader}>{item.name}</Text></View></TouchableOpacity>

    render() {
        const statusHeight = StatusBar.currentHeight ? StatusBar.currentHeight : 0;

        return(
            <View>
                <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup} token={this.state.token} setToken={this.setToken} setUser={this.setUser} handleSetStorage={this.handleSetStorage}/>
                

                                {this.state.signup ? 
                                    <Login setUser={this.setUser} setToken={this.setToken} setSignup={this.setSignup} token={this.state.token} handleSetStorage={this.handleSetStorage}/>
                                    : 
                                    (!this.state.selectedVoting ? 
                                        <View>
                                            <View View style={styles.html}>
                                                <View View style={styles.body}>
                                                    <View View style={styles.container}>
                                                        <View View style={styles.content}>
                                                          <View>     
                                                            {this.state.done == true &&  <View style={{width: '100%', //Si la votación se ha realizado se muestra la barra verde.
                                                            backgroundColor: 'rgb(49, 250, 95)',
                                                            paddingHorizontal: 20,
                                                            paddingTop: statusHeight + 10,
                                                            paddingBottom: 10}}>
                                                                <Text style={{fontWeight:500, fontFamily: 'calibri', fontSize:'16px'}}>Votación enviada!</Text>
                                                            </View>}
                                                        </View>     
                                                        <Text style={styles.title}>Votaciones disponibles</Text>
                                                            <SafeAreaView style={styles.containerList}>
                                                                    <FlatList style={styles.item} data={this.state.votings} renderItem={this.render_voting} />
                                                            </SafeAreaView>
                                                            <View View style={styles.btnprimary}>
                                                                <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Recargar" onPress={this.loadVotings} />
                                                            </View>
                                                        </View>
                                                    </View>
                                                </View>
                                            </View>
                                        </View> :
                                        <Voting setDone={this.setDone} voting={this.state.selectedVoting} user={this.state.user} token={this.state.token} resetSelected={() => this.setSelectedVoting(undefined)}/> )
                                }
  
            </View>);
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
        "width": "100%",
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
    containerList: {
        flex: 1,
        paddingTop: 20
    },
    sectionHeader: {
        paddingTop: 2,
        paddingLeft: 10,
        paddingRight: 10,
        paddingBottom: 2,
        fontSize: 32,
        backgroundColor: 'rgba(247,247,247,1.0)',
     },
    item: {
        padding: 15,
        marginVertical: 8,
        marginHorizontal: 16,
    }
    
});
export default App;
