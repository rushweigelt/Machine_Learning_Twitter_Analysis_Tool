
import React, { Component } from "react";
import { render } from "react-dom";
/*
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <ul>
        {this.state.data.map(search => {
          return (
            <li key={search.ml_model}>
              {search.user_hashtag} - {search.map_bool} - {search.created_at}
            </li>
          );
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
*/
/*
import React, { Component } from "react";
import { render } from "react-dom";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    ml_model: '',
    user_hashtag: '',
    map_bool: false
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const ml_model = target.ml_model;
    const user_hashtag = target.user_hashtag;
    const map_bool = target.map_bool

    this.setState({ml_model: event.target.ml_model, user_hashtag: event.target.user_hashtag, map_bool: event.target.map_bool});
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Model:
          <select value={this.state.ml_model} onChange={this.handleInputChange}>
          <option value='rf'>Random Forest</option>
          <option value='nb'>Naive Bayes</option>
          <option value='ada'>Ada Boost </option>
          <option value='lstm'>LSTM</option>
          </select>
        </label>
        <label>Hashtag:
        <input type="text" value={this.state.user_hashtag} onChange={this.handleInputChange} />
        <input type="submit" value="Submit" />
      </form>
    );
  }
}
/*
ReactDOM.render(
  <NameForm />,
  document.getElementById('root')
);

export default App;

const container = document.getElementById("app");
render(<App />, container);
*/
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ml_model: '',
      user_hashtag: '',
      map_bool: false,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    this.setState({
    [event.target.name] : event.target.value});
    console.log(event.target.value)
  }

  handleSubmit(event){
    alert(this.state.ml_model.value)
    this.setState({
    ml_model: ml_model.value,
    user_hashtag: user_hashtag.value,
    map_bool: map_bool.value});
    console.log(this.state.map_bool)
    event.preventDefault()
 }
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
      <label>
          Hashtag to Analyze:
          <input
            name="user_hashtag"
            type="text"
            value={this.state.user_hashtag}
            onChange={this.handleInputChange} />
        </label>
        <br />
        <label>
          Machine Learning Model:
          <select value={this.state.value} handleInputChange={this.handleInputChange} name="ml_model">
            <option value="rf">Random Forest</option>
            <option value="nb">Naive Bayes</option>
            <option value='ada'>Ada Boost</option>
            <option value="lstm">LSTM</option>
            </select>
        </label>
        <br />
        <label>
          Heatmap of Bot Locations?:
          <input
            name="map_bool"
            type="checkbox"
            checked={this.state.map_bool}
            onChange={this.handleInputChange} />
        </label>
        <br />
        <input type="submit" value="Search for Bots!" />
      </form>
    );
  }
}
/*
ReactDOM.render(
  <Reservation />,
  document.getElementById('root')
);
*/
export default App;

const container = document.getElementById("app");
render(<App />, container);