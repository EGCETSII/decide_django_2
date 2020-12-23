import React from 'react';
import Barra from './components/Barra';
import Login from './components/Login';
import Voting from './components/Voting';
import { FlatList, Text, TouchableOpacity, View, Button } from 'react-native';
import axios from 'axios';
import config from './config.json';

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
        <View style={{ padding: 20, backgroundColor: '#fff', borderRadius: 10, marginBottom: 15 }}><Text>{item.name}</Text></View></TouchableOpacity>

    render() {
        
        return(
            <View style={{backgroundColor: '#f5f5f5', height: '100%'}}>
                <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup} token={this.state.token} setToken={this.setToken} setUser={this.setUser}/>
                
                <View style={{padding:20, maxWidth: 800}}>
                    {this.state.signup ? 
                        <Login setUser={this.setUser} setToken={this.setToken} setSignup={this.setSignup} token={this.state.token} />
                        : 
                        (!this.state.selectedVoting ? 
                            <View>
                                <Text style={{fontWeight: 'bold', marginBottom: 15}}>Votaciones disponibles</Text>
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
