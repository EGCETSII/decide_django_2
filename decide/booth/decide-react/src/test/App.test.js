import React from 'react';
import { shallow, configure, mount, render } from 'enzyme';
import App from '../App';
import Adapter from 'enzyme-adapter-react-16';
import AsyncStorage from '@react-native-community/async-storage'
import 'jsdom-global/register';
import Login from '../components/Login';
import { Alert, Button, Text, TextInput, View } from 'react-native';
import Barra from '../components/Barra';

describe('Testing App component',() => {

    let wrapper;
    
    configure({adapter: new Adapter()});
    
    it('Full Login test Correct', async () => {
        wrapper = mount(<App/>);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapper.find(TextInput)
        const wrapperUsername = wrapper.find(TextInput).first()
        const wrapperPassword = wrapper.find(TextInput).at(1)
        const wrapperWithButton = wrapperLogin.find(Button)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");
        
        wrapperLogin.find(Button).simulate('click')

        await new Promise((r) => setTimeout(r, 250));

        expect(wrapper.find(Login)).toHaveLength(1);
        expect(wrapper.find(TextInput)).toHaveLength(2);
        expect(wrapper.find(TextInput).first()).toHaveLength(1);
        expect(wrapper.find(TextInput).at(1)).toHaveLength(1);
        expect(wrapper.find(Button)).toHaveLength(1);
        expect(wrapperLogin.state('form').username).toBe('decidehueznar');
        expect(wrapper.state('signup')).toBe(false);
        expect(wrapperLogin.state('error')).toBe(false);
        expect(wrapper.state('user')).toBeDefined();
    });
})