import React, { Component } from 'react';
import { BigInt } from '../crypto/BigInt';
import { ElGamal } from '../crypto/ElGamal';
import { Alert, Button, Picker, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';

export default class Voting extends Component {

    state = {
        bigpk: {
            p: BigInt.fromJSONObject(this.props.voting.pub_key.p.toString()),
            g: BigInt.fromJSONObject(this.props.voting.pub_key.g.toString()),
            y: BigInt.fromJSONObject(this.props.voting.pub_key.y.toString()),
        },
        voting: null,
        selected: this.props.voting.question.options[0].number,
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
                Alert.alert('Enhorabuena, has votado correctamente');
                this.props.resetSelected();
            })
            .catch(error => {
                Alert.alert(`Error: ${error}`);
            });
    }

    render() {
        const { voting, resetSelected } = this.props;

        return <View>
            <Text style={{fontSize: 15}}>{voting.name}</Text>
            <Text style={{fontSize: 13}}>{voting.question.desc}</Text>
            <Picker selectedValue={this.state.selected} onValueChange={(itemValue, itemIndex) => this.setState({selected: itemValue})}>
                {voting.question.options.map(opt => 
                    <Picker.Item label={opt.option} value={opt.number} key={opt.number} />
                )}
            </Picker>
            <Button title="Votar" onPress={this.handleSubmit} />
            <Button title="Volver" color="#333" onPress={resetSelected} />
        </View>;
    }
}
