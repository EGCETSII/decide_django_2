import axios from 'axios';

export const postData = (url, data, token=undefined) => {
    const headers = {
        'content-type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = 'Token ' + token;
    }
    const options = {headers};
    return axios.post(url, data, options)
        .then(response => {
            if (response.status === 200) { 
                return response;
            } else {
                return Promise.reject(response.statusText);
            }
        });
};
