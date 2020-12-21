import './App.css';
import React from 'react';
import Login from './components/Login';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            currentUser: null,
            keybits : window.KEYBITS
        };
    }


    setCurrentUser(user) {
        console.log(user)
        this.setState({currentUser:user});
    }

    render() {
        return(
            <div className="App">
                {!this.state.currentUser ? <Login setCurrentUser={this.setCurrentUser.bind(this)} /> : <p>{this.state.currentUser.username}</p>}
            </div>);
    }
}

export default App;
