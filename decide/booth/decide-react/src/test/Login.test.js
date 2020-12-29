import React from 'react';
import { shallow, configure } from 'enzyme';
import Login from '../components/Login';
import Adapter from 'enzyme-adapter-react-16';

describe('Test case for testing login',() =>{

    let wrapper;
    
    configure({adapter: new Adapter()});
    test('username check',()=>
    {
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'username', value: 'decidehueznar'}});

        expect(wrapper.state('username')).toEqual('decidehueznar');
    })

    it('password check',()=>{
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'password', value: 'decidehueznar'}});

        expect(wrapper.state('password')).toEqual('decidehueznar');
    })

    it('login check with right data',()=>{
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'username', value: 'decidehueznar'}});
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'password', value: 'decidehueznar'}});
        wrapper.find('button').simulate('click');

        expect(wrapper.state('error')).toBe(false);
    })

    it('login check with wrong data',()=>{
        wrapper = shallow(<Login/>);
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'username', value: 'decidehueznar'}});
        wrapper.find('TextInput').simulate('changeText', {target: {name: 'password', value: 'decidezapdos'}});
        wrapper.find('button').simulate('click');

        expect(wrapper.state('error')).toBe(true);
    })

})