import React from 'react';
import { shallow, configure } from 'enzyme';
import Login from '../components/Login';
import Adapter from 'enzyme-adapter-react-16';

describe('Test case for testing login',() => {

    let wrapper;
    
    configure({adapter: new Adapter()});
    it('username check',() => {
        wrapper = shallow(<Login/>);
        const container = wrapper.find('#username');
        wrapper.find('#username').simulate('changeText', 'decidehueznar');
        //wrapper.setState({username:'decidehueznar'})


        expect(container.length).toBe(1);
        expect(wrapper.state('form').username).toEqual('decidehueznar');
    });

    it('password check',() => {
        wrapper = shallow(<Login/>);
        wrapper.find('#password').simulate('changeText', 'decidehueznar');

        expect(wrapper.state('form').password).toEqual('decidehueznar');
    })
/*
    it('login check with right data',() => {
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'username', value: 'decidehueznar'}});
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'password', value: 'decidehueznar'}});
        wrapper.find('button').simulate('click');

        expect(wrapper.state('error')).toBe(false);
    })

    it('login check with wrong data',() => {
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'username', value: 'decidehueznar'}});
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'password', value: 'decidezapdos'}});
        wrapper.find('button').simulate('click');

        expect(wrapper.state('error')).toBe(true);
    })
//*/
})