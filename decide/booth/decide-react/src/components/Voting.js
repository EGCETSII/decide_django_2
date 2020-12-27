import React, { Component } from 'react';
import { BigInt } from '../crypto/BigInt';
import { ElGamal } from '../crypto/ElGamal';
import { Alert, Button, Picker, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';
import { StyleSheet} from "react-native";


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

        return <View style={styles.htmlStyle}>
                <View style={styles.containerStyle}>
                    <View style={styles.contentStyle}>
                        <View style={styles.row}>
                            <View style={styles.clearfix}>
                                <Text style={styles.textStyle}>{voting.name}</Text>
                                <Text style={styles.textStyle}>{voting.question.desc}</Text>
                                <View style={{flex: 1, backgroundColor: 'powderblue'}} />
                            </View>
                            <View style={styles.clearfix}>
                                <Picker style={styles.pickerStyle} selectedValue={this.state.selected} onValueChange={(itemValue, itemIndex) => this.setState({selected: itemValue})}>
                                    {voting.question.options.map(opt => 
                                        <Picker.Item label={opt.option} value={opt.number} key={opt.number} />
                                    )}
                                </Picker>
                            </View>
                            <View style={styles.clearfix}> 
                                <View style={styles.button1Style}>
                                    <Button title="Votar" color="linear-gradient(top, #049cdb, #0064cd)" onPress={this.handleSubmit} />
                                </View>
                            </View>
                            <View style={styles.clearfix}> 
                                <View style={styles.button2Style}>
                                    <Button title="Volver" color="linear-gradient(top, #696969, #000000)" onPress={resetSelected} />
                                </View>
                            </View>
                        </View>    
                    </View>
                </View>
        </View>
    }
}

const styles = StyleSheet.create ({
    htmlStyle: {
        marginTop: 0,
        marginBottom: 0,
        marginRight: 0,
        marginLeft: 0,
        paddingTop: 0,
        paddingBottom: 0,
        paddingRight: 0,
        paddingLeft: 0
    },

    containerStyle: {
        justifyContent: 'center',
        alignItems: 'center'
    },
    contentStyle: {
        width: 960,
        backgroundColor: 'fff',
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        borderBottomRightRadius: 10,
        borderBottomLeftRadius: 10,
        overflow: 'hidden',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        paddingTop: 50,
        paddingRight: 50,
        paddingBottom: 50,
        paddingLeft: 50
    },
    textStyle:{
        fontSize: 18,
        lineHeight: 24,
        justifyContent: 'center',
        alignSelf: 'center'
    },
    pickerStyle:{  
        height: 40,  
        width: 800,  
        color: 'rgb(7, 7, 76)',  
        justifyContent: 'center',
        alignSelf: 'center'  
    },
    row: {
    },
    clearfix: {
        "marginBottom": 24,
        "zoom": 1
    },
    button1Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#0064cd",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        transition: "all 0.4s",
        backgroundRepeat: "repeat-x",
        backgroundImage: "linear-gradient(top, #049cdb, #0064cd)",
        textShadowOffset: {
          width: 0,
          height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#0064cd",
        borderRightColor: "#0064cd",
        borderBottomColor: "#0064cd",
        borderLeftColor: "#0064cd"
    },
    button2Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#000000",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        transition: "all 0.4s",
        backgroundRepeat: "repeat-x",
        backgroundImage: "linear-gradient(top, #696969, #000000)",
        textShadowOffset: {
          width: 0,
          height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#000000",
        borderRightColor: "#000000",
        borderBottomColor: "#000000",
        borderLeftColor: "#000000"
    },
});
