import './App.css';
import React from 'react';
import Login from './components/Login';
import Voting from './components/Voting';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            currentUser: null,
            keybits : window.KEYBITS,
            urlLogin : window.urlLogin,
            urlStore : window.urlStore,
            urlGetUser : window.urlGetUser,
            urlLogout : window.urlLogout,
            voting : window.votingData,
            user: null,
            token: null,
            signup: true
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


    render() {
        return(
            <div className="App">
                    { <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup.bind(this)} token={this.state.token} setToken={this.setToken.bind(this)} setUser={this.setUser.bind(this)}/>}

                {!this.state.currentUser ? 
                    <Login setCurrentUser={this.setCurrentUser.bind(this)} />
                    : 
                    <Voting voting={this.state.voting} user={this.state.currentUser} /> }
            </div>);
    }
}

export default App;
