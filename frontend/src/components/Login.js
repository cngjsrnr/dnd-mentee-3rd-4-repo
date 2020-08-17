import React, { Component, Fragment } from "react";

// 로그인
export default class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password: "",
    };
  }

  // 로그인 되있으면 뉴스 보여주는 페이지로 이동
  componentDidMount() {
    if (this.props.isAuthenticated) {
      // 뉴스 보여주는 페이지로 이동코드 적어주세요
    }
  }

  validateForm(username, password) {
    return username && username.length > 0 && password && password.length > 0;
  }

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  // 서버에 등록되어있는 회원 정보로 로그인을 시도하는 경우
  handleSubmit = (submitEvent) => {
    let data = {
      email: this.state.email,
      password: this.state.password,
    };
    submitEvent.preventDefault();

    let handleErrors = (response) => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response;
    };

    // 서버로부터 새로운 access token 발급받음
    fetch("http://localhost:8000/user/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(handleErrors)
      .then((res) => res.json())
      .then((json) => {
        console.log(json.token);
        // 발급 완료 되었다면 해당 토큰을 클라이언트 Local Storage에 저장
        if (json.user && json.user.email && json.token) {
          this.props.userHasAuthenticated(
            true,
            json.user.email,
            json.user.username,
            json.token
          );
          // 뉴스 보여주는 페이지로 이동코드 적어주세요

          console.log("로그인 성공");
          alert("로그인 성공");
        }
      })
      .catch((error) =>
        alert(
          " 로그인을 실패했습니다\n ID또는 PW를 확인해주세요\n 내용(배포시 지워주세요):" +
            error
        )
      );
  };

  render() {
    return (
      <div className="Login">
        로그인 페이지 입니다.
        <form onSubmit={this.handleSubmit}>
          아이디:
          <input type="text" name="email" onChange={this.handleChange} />
          <br />
          비밀번호:
          <input type="password" name="password" onChange={this.handleChange} />
          <br />
          <button type="submit">로그인</button>
        </form>
      </div>
    );
  }
}
