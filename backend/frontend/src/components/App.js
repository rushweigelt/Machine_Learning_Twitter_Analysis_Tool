
import React, { Component } from "react";
import { render } from "react-dom";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data : [], //a container for any return data we get for results
      ml_model: '', //user-selected machine learning model to use
      user_hashtag: '', //user-hashtag to post and search
      map_bool: false, //map boolean
      placeholder: "Loading", //placeholder so we know if we're not loading properly
      loaded: false,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  //Handle Input Changes by overwriting the current state that changed
  handleInputChange(event) {
    this.setState({
    [event.target.name] : event.target.value});
    console.log(event.target.value)
  }
  //Handle Submit of Form. Need to add Post Method
  handleSubmit(event){
    this.setState({
    ml_model: ml_model.value,
    user_hashtag: user_hashtag.value,
    map_bool: map_bool.value});
    console.log(this.state.map_bool)
    event.preventDefault()
 }

 //load from db
 componentDidMount() {
  fetch("api/")
  .then(response => {
   if (response.status > 400) {
    return this.setState(() => {
     return { placeholder: "Something went wrong!"};
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
  //what we're rendering. In this case, a form that will get the info we need from user
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
      //user-hashtag
      <label>
          Hashtag to Analyze:
          <input
            name="user_hashtag"
            type="text"
            value={this.state.user_hashtag}
            onChange={this.handleInputChange} />
        </label>
        <br />
        //machine learning select dropdown
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
        //heatmap checkbox
        <label>
          Heatmap of Bot Locations?:
          <input
            name="map_bool"
            type="checkbox"
            checked={this.state.map_bool}
            onChange={this.handleInputChange} />
        </label>
        <br />
        //submit button
        <input type="submit" value="Search for Bots!" />
        //a spot for our return data (results)
        <ul>
      {this.state.data.map(search => {
       return (
        <li key="foo">
         {search.ml_model} - {search.user_hashtag} - {search.map_bool}
         </li>
         );
         })}
         </ul>
      </form>
         );
  }
}
export default App;

const container = document.getElementById("app");
render(<App />, container);