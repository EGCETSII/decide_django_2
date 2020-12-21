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
        };
    }


    setCurrentUser(user) {
        this.setState({currentUser:user});
    }

    render() {
        return(
            <div className="App">
                {!this.state.currentUser ? 
                    <Login setCurrentUser={this.setCurrentUser.bind(this)} />
                    : 
                    <Voting voting={this.state.voting} user={this.state.currentUser} /> }
            </div>);
    }
}

export default App;
