import React, { Component } from 'react'
import FormCheck from 'react-bootstrap/esm/FormCheck';

export default class Voting extends Component {

    state = {
        urlStore : window.urlStore,
        bigpk: {
        },
        voting: null,
        selected: null,
        voted: false,
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
                    <button onClick={() => alert("Enviado")}>Votar</button>
                </div>
            </div>: <>
                <div className="alert alert-success">
                    Has votao, enhorabuena crack.
                </div>
            </>;
    }
}
