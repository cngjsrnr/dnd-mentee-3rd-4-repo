import React, { Component } from "react";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
    };
  }

  async componentDidMount() {
    try {
      fetch("http://localhost:8000/api/posts", {
        headers: {
          Authorization: `JWT ${this.props.token}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          console.log("posts: " + json);
          this.setState({
            posts: json,
          });
        });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    let lists = [];
    let data = this.state.posts;
    let i = 0;

    while (i < data.length) {
      lists.push(
        <div key={data[i].pk}>
          <h1>{data[i].fields.title}</h1>
          <span>{data[i].fields.content}</span>
        </div>
      );

      i += 1;
    }
    let test = [];
    test.push(<h1>test</h1>);
    return <div>{lists}</div>;
  }
}

export default App;
