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
        selected: null,
        options: new Array(),
        noSelection: false

    }

    doneToFalse =() => {
        this.props.setDone(false);
    }

    handleSubmit = (event) => {
        event.preventDefault();
        if (!this.state.selected) {
            this.setState({noSelection:true})
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
            <Text style={{fontSize: 14, paddingBottom:15, paddingTop:5}}>{voting.question.desc}</Text>
            <RadioForm
                radio_props={this.state.options}
                initial={-1}
                onPress={(itemValue) => this.setState({selected: itemValue})}
                buttonSize={9}
                
            />
            {this.state.noSelection && <View style={{paddingTop:10, paddingBottom:7}}>
                <Text style={{fontWeight: 'bold', color:'rgb(192,26,26)', fontFamily: 'calibri', fontSize:'15px'}}>Debe seleccionar una opción</Text>
            </View>}
            <Button title="Votar" onPress={this.handleSubmit} />
            <Button title="Volver" color="#333" onPress={resetSelected} />
        </View>;
    }
}
