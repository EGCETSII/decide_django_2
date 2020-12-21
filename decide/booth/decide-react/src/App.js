import logo from './logo.svg';
import './App.css';
import React from 'react';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Form from 'react-bootstrap/Form'
import FormText from 'react-bootstrap/FormCheckInput'
import FormGroup from 'react-bootstrap/FormGroup'
import axios from 'axios'

class App extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      keybits : window.KEYBITS,
      voting : window.votingData,
      selected : "",
      signup : true,
      alertShow : false,
      alertMsg : "",
      alertLvl : "info",
      token : null,
      user : null,
      form : {
        username: "votante3",
        password: "1234abcd"
      }
    };

    this.postData = this.postData.bind(this);
    this.onSubmitLogin = this.onSubmitLogin.bind(this);
    this.getUser = this.getUser.bind(this);
  }

  onSubmitLogin(event) {
    event.preventDefault();
    this.postData("http://localhost:8000/gateway/authentication/login/", this.state.form)
        .then(data => {
            document.cookie = 'decide='+data.token+'; Secure';
            this.state.token = data.data.token
            console.log(this.state.token)
            this.getUser();
        })
        .catch(error => {
            this.showAlert("danger", 'Error: ' + error);
        });
      }

  getUser(evt) {
    var token = {
      token: this.state.token
    } 
    this.postData("http://localhost:8000/gateway/authentication/getuser/", token)
        .then(data => {
            this.state.user = data;
            this.state.signup = false;
        }).catch(error => {
            this.showAlert("danger", 'Error: ' + error);
        });
    }

  postData(url, data) {
    // Default options are marked with *
    var headers = {
      'content-type': 'application/json',
    }
    if (this.state.token) {
        headers['Authorization'] = 'Token ' + this.state.token;
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
  
    showAlert(lvl, msg) {
      this.state.alertLvl = lvl;
      this.state.alertMsg = msg;
      this.state.alertShow = true;
  }

  render() {
    return(
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
        {this.state.voting.id}
        {window.urlGateway}
        </p>
        <button onClick = {this.onSubmitLogin}></button>
        <Form onSubmit={this.onSubmitLogin}>
          <FormGroup>
            
          </FormGroup>
          <FormGroup>

          </FormGroup>
        </Form>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>)
  };
}

export default App;
