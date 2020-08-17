import React, { Component } from "react";

import Login from "./components/Login";
import Signup from "./components/Signup";
import Post from "./components/Post";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: null,
      isAuthenticated: localStorage.getItem("token") ? true : false,
    };
  }

  // user가 로그인 중인지 확인하고, 로그인 중이라면 유저의 정보를 서버로부터 받아온다.
  componentDidMount() {
    // 토큰(access token)이 이미 존재하는 상황이라면 서버에 GET /validate 요청하여 해당 access token이 유효한지 확인
    if (this.state.isAuthenticated) {
      let handleErrors = (response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      };

      // 현재 JWT 토큰 값이 타당한지 GET /validate 요청을 통해 확인하고
      // 상태 코드가 200이라면 현재 GET /user/current 요청을 통해 user정보를 받아옴
      fetch("http://localhost:8000/validate/", {
        headers: {
          Authorization: `JWT ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          fetch("http://localhost:8000/user/current", {
            headers: {
              Authorization: `JWT ${localStorage.getItem("token")}`,
            },
          })
            .then(handleErrors)
            .then((res) => res.json())
            .then((json) => {
              // 현재 유저 정보 받아왔다면, 로그인 상태로 state 업데이트 하고
              if (json.username) {
                this.setState({ username: json.username });
              }

              // Refresh Token 발급 받아 token의 만료 시간 연장
              fetch("http://localhost:8000/refresh/", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  token: localStorage.getItem("token"),
                }),
              })
                .then(handleErrors)
                .then((res) => res.json())
                .then((json) => {
                  this.userHasAuthenticated(
                    true,
                    json.user.username,
                    json.token
                  );

                  console.log("Refresh Token 발급");
                  console.log(json.token);
                })
                .catch((error) => {
                  console.log(error);
                });
            })
            .catch((error) => {
              this.handleLogout();
            });
        })
        .catch((error) => {
          this.handleLogout();
        });
    }
  }

  // 새로운 User가 로그인 했다면 (서버로 부터 access token을 발급받았을 것이고) 해당 토큰을 localStorage에 저장
  userHasAuthenticated = (authenticated, username, token) => {
    this.setState({
      isAuthenticated: authenticated,
      username: username,
    });
    localStorage.setItem("token", token);
  };

  // 로그인 상태였던 유저가 로그아웃을 시도한다면 토큰을 지움
  handleLogout = () => {
    try {
      this.setState({
        isAuthenticated: false,
        username: "",
      });
      localStorage.removeItem("token");
      console.log("Logged out successfully");
    } catch {
      this.setState({
        isAuthenticated: false,
        username: "",
      });
      localStorage.removeItem("token");
      console.log("Logged out successfully");
    }
  };

  render() {
    let lists;
    if (this.state.isAuthenticated) {
      lists = <button onClick={this.handleLogout}> 로그아웃</button>;
    } else {
      lists = (
        <div>
          <Login
            username={this.state.username}
            isAuthenticated={this.state.isAuthenticated}
            userHasAuthenticated={this.userHasAuthenticated}
          ></Login>
          <br />
          <Signup
            username={this.state.username}
            isAuthenticated={this.state.isAuthenticated}
            userHasAuthenticated={this.userHasAuthenticated}
          ></Signup>
          <br />
        </div>
      );
    }

    return (
      <div>
        {lists}
        <Post token={localStorage.getItem("token")}></Post>
      </div>
    );
  }
}

export default App;
