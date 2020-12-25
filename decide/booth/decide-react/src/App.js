import React from 'react';
import Barra from './components/Barra';
import Login from './components/Login';
import Voting from './components/Voting';
import { FlatList, Text, TouchableOpacity, View, Button, SafeAreaView } from 'react-native';
import axios from 'axios';
import config from './config.json';
import { StyleSheet} from "react-native";

class App extends React.Component {

    state = {
        currentUser: undefined,
        selectedVoting: undefined,
        token: undefined,
        votings: [],
        signup: true,
    }

    setCurrentUser = (user) => {
        this.setState({currentUser:user});
    }

    setUser = (user2) => {
        this.setState({user:user2});
    }

    setToken = (token2) =>  {
        console.log('Token',token2);
        this.setState({token:token2});
    }

    setSignup = (signup2) =>  {
        this.setState({signup:signup2});
    }

    setSelectedVoting = (voting) => {
        this.setState({selectedVoting: voting});
    }


    loadVotings = () => {
        axios.get(config.VOTING_URL).then(response => {
            this.setState({votings: response.data});
            console.log(response.data);
        });

    }

    componentDidMount() {
        this.loadVotings();
    }


    render_voting = ({item}) => <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
        <View View style={styles.item}><Text style={styles.sectionHeader}>{item.name}</Text></View></TouchableOpacity>

    render() {
        
        return(
            <View>
                <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup} token={this.state.token} setToken={this.setToken} setUser={this.setUser}/>
                

                                {this.state.signup ? 
                                    <Login setUser={this.setUser} setToken={this.setToken} setSignup={this.setSignup} token={this.state.token} />
                                    : 
                                    (!this.state.selectedVoting ? 
                                        <View>
                                            <View View style={styles.html}>
                                                <View View style={styles.body}>
                                                    <View View style={styles.container}>
                                                        <View View style={styles.content}>
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
                                        <Voting voting={this.state.selectedVoting} user={this.state.user} token={this.state.token} resetSelected={() => this.setSelectedVoting(undefined)}/> )
                                }
  
            </View>);
    }
}

export default App;

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
        "display": "block",
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
        "transition": "all 0.4s",
        "backgroundRepeat": "repeat-x",
        "backgroundImage": "linear-gradient(top, #049cdb, #0064cd)",
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