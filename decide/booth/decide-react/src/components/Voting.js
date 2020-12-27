import React, { Component } from 'react';
import { BigInt } from '../crypto/BigInt';
import { ElGamal } from '../crypto/ElGamal';
import { Alert, Button, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';
import RadioForm from 'react-native-simple-radio-button';

export default class Voting extends Component {

    state = {
        bigpk: {
            p: BigInt.fromJSONObject(this.props.voting.pub_key.p.toString()),
            g: BigInt.fromJSONObject(this.props.voting.pub_key.g.toString()),
            y: BigInt.fromJSONObject(this.props.voting.pub_key.y.toString()),
        },
        voting: null,
        selected: this.props.voting.question.options[0].number,
        options: new Array()

    }

    doneToFalse =() => {
        this.props.setDone(false);
    }

    handleSubmit = (event) => {
        event.preventDefault();
        if (!this.state.selected) {
            alert('Selecciona una opción');
        } else {
            const { voting, user } = this.props;
            const vote = this.encrypt();
            const data = {
                vote: {a: vote.alpha.toString(), b: vote.beta.toString()},
                voting: voting.id,
                voter: user.id,
                token: this.props.token
            };
            console.log('Data',data)
            this.send(data);
        }
    }

    encrypt = () =>  {
        const { selected } = this.state;
        const bigmsg = BigInt.fromJSONObject(selected.toString());
        const cipher = ElGamal.encrypt(this.state.bigpk, bigmsg);
        return cipher;
    }

    send = (data) => {
        postData(config.STORE_URL, data, this.props.token)
            .then(response => {
                this.props.setDone(true)
                this.props.resetSelected();
            })
            .catch(error => {
                alert(`Error: ${error}`);
            });
    }

    introduccion = (opt) => {
        const dict ={};
        dict['label'] = opt.option;
        dict['value'] = opt.number;
        this.state.options.push(dict);
    }

    options = (voting) => {
        voting.question.options.map(opt => 
        this.introduccion(opt))}

    componentDidMount() {
        this.doneToFalse();
        const { voting } = this.props;
        this.options(voting);
        this.setState({options:this.state.options})
    }

    render() {
        const { voting, resetSelected } = this.props;
        return <View>
            <Text style={{fontSize: 18, fontWeight:'bold'}}>{voting.name}</Text>
            <Text style={{fontSize: 14}}>{voting.question.desc}{'\n'}{'\n'}</Text>
            <RadioForm
                radio_props={this.state.options}
                onPress={(itemValue) => this.setState({selected: itemValue})}
                buttonSize={9}
            />
            <Button title="Votar" onPress={this.handleSubmit} />
            <Button title="Volver" color="#333" onPress={resetSelected} />
        </View>;
    }
}
