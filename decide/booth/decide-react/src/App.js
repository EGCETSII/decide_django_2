import axios from 'axios';
import React from 'react';
import { FlatList, Text, TouchableOpacity, View, Button } from 'react-native';
import Barra from './components/Barra';
import Login from './components/Login';
import Voting from './components/Voting';


class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            currentUser: null,
            keybits : 256,
            urlLogin : window.urlLogin,
            urlStore : window.urlStore,
            urlGetUser : window.urlGetUser,
            urlLogout : window.urlLogout,
            voting : window.votingData,
            user: null,
            token: null,
            signup: true,
            selectedVoting: undefined,
            votings: []
        };
    }


    setCurrentUser(user) {
        this.setState({currentUser:user});
    }

    setUser(user2) {
        this.setState({user:user2});
    }

    setToken(token2) {
        console.log('Token',token2)
        this.setState({token:token2});
    }

    setSignup(signup2) {
        this.setState({signup:signup2});
    }


    loadVotings = () => {
        axios.get("http://localhost:8000/voting/").then(response => {
            this.setState({votings: response.data})
            console.log(response.data)
        })

    }

    componentDidMount() {
        this.loadVotings()
    }

    setSelectedVoting = (voting) => {
        this.setState({selectedVoting: voting})
    }


    render_voting = ({item}) => {
       return <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
            <View style={{ padding: 20, backgroundColor: "#fff", borderRadius: 10, marginBottom: 15 }}><Text>{item.name}</Text></View></TouchableOpacity>;
    } 

    render() {
        
        return(
            <View style={{backgroundColor: "#f5f5f5", height: "100%"}}>
                <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup.bind(this)} token={this.state.token} setToken={this.setToken.bind(this)} setUser={this.setUser.bind(this)}/>
                <View style={{padding:20, maxWidth: 800}}>
                    {this.state.signup ? 
                        <Login setUser={this.setUser.bind(this)} setToken={this.setToken.bind(this)} setSignup={this.setSignup.bind(this)} token={this.state.token} />
                        : 
                        (!this.state.selectedVoting ? 
                            <View>
                                <Text style={{fontWeight: "bold", marginBottom: 15}}>Votaciones disponibles</Text>
                                <FlatList data={this.state.votings} renderItem={this.render_voting} />
                                <Button title="Recargar" color="#333" onPress={this.loadVotings} />
                            </View> :
                            <Voting voting={this.state.selectedVoting} user={this.state.user} token={this.state.token} resetSelected={() => this.setSelectedVoting(undefined)}/> )
                        }
                </View>
            </View>);
    }
}

export default App;
