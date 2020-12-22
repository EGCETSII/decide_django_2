import React, { Component } from 'react'
import FormCheck from 'react-bootstrap/esm/FormCheck';
import axios from 'axios';
import { BigInteger as BigInt } from "jsbn";
import { ElGamal } from "../crypto/ElGamal";

// why not?
// ZERO AND ONE are already taken care of
BigInt.TWO = new BigInt("2", 10);

BigInt.setup = function(callback, fail_callback) {
    // nothing to do but go
    callback();
};

BigInt.prototype.toJSONObject = function() {
    return this.toString();
};

BigInt.fromJSONObject = function(s) {
    return new BigInt(s, 10);
};

BigInt.fromInt = function(i) {
    return BigInt.fromJSONObject("" + i);
};

BigInt.use_applet = false;
/* jshint ignore:end */



export default class Voting extends Component {

    state = {
        urlStore : window.urlStore,
        bigpk: {
            p: BigInt.fromJSONObject(this.props.voting.pub_key.p.toString()),
            g: BigInt.fromJSONObject(this.props.voting.pub_key.g.toString()),
            y: BigInt.fromJSONObject(this.props.voting.pub_key.y.toString()),
        },
        voting: null,
        selected: null,
        voted: false,
    }

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.decideEncrypt = this.decideEncrypt.bind(this);
        this.decideSend = this.decideSend.bind(this);
        this.postData = this.postData.bind(this);
    }

    decideEncrypt() {
        const { selected } = this.state;
        const bigmsg = BigInt.fromJSONObject(selected.toString());
        console.log(bigmsg);
        console.log(this.state.bigpk);
        const cipher = ElGamal.encrypt(this.state.bigpk, bigmsg);
        return cipher;
    }

    handleSubmit(event) {
        event.preventDefault();
        if (!this.state.selected) {
            alert("Selecciona una opción");
        } else {
            const { voting, user } = this.props;
            console.log(user)
            const vote = this.decideEncrypt();
            const data = {
                vote: {a: vote.alpha.toString(), b: vote.beta.toString()},
                voting: voting.id,
                voter: user.id,
                token: this.props.token
            }
            this.decideSend(data);
        }
    }

    decideSend(data) {
        this.postData(this.state.urlStore, data)
            .then(response => {
                // this.showAlert("success", '{% trans "Congratulations. Your vote has been sent" %}');
                this.setState({voted: true});
            })
            .catch(error => {
                // this.showAlert("danger", '{% trans "Error: " %}' + error);
                alert("Peto algo wey");
            });

            
    }

    postData(url, data) {
        // Default options are marked with *
        var headers = {
            'content-type': 'application/json',
        };
        if (this.props.token) {
            headers['Authorization'] = 'Token ' + this.props.token;
        }
        return axios.post(url, data, {headers})
            .then(response => {
                if (response.status === 200) { 
                    return response;
                } else {
                    return Promise.reject(response.statusText);
                }
        });
    }

    render() {
        const { voting } = this.props;
        const { voted } = this.state;

        return !voted ? <div class="voting">
                <h1>{voting.id} - {voting.name}</h1>
                <div>
                    <h2>{voting.question.desc}</h2>
                    {voting.question.options.map(opt => <>
                            <FormCheck type="radio" name="question" label={opt.option} onClick={() => this.setState({selected: opt.number})} />
                        </>
                    )}
                    <button onClick={this.handleSubmit}>Votar</button>
                </div>
            </div>: <>
                <div className="alert alert-success">
                    Has votao, enhorabuena crack.
                </div>
            </>;
    }
}
