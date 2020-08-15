import React, { Component } from "react";

// 회원가입
export default class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      password: "",
      first_name:"",
      email:"",
    };
  }

  //로그인이 되있으면 뉴스보여주는 페이지로 이동
  componentDidMount() {
    if (this.props.isAuthenticated) {
      //뉴스 보여주는 페이지로 이동코드 적어주세요
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

  handleSubmit = (submitEvent) => {
    let data = {
      username: this.state.username,
      password: this.state.password,
      first_name:this.state.first_name,
      email:this.state.email,
    };
    submitEvent.preventDefault();
    
    //여기에 회원정보 유효성 검사하는 코드 추가해야함

    let handleErrors = (response) => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response;
    };

    fetch("http://localhost:8000/user/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(handleErrors)
      .then((res) => res.json())
      .then((json) => {
        if (json.username && json.token) {
          this.props.userHasAuthenticated(true, json.username, json.token);
          //로그인이 되있으면 뉴스보여주는 페이지로 이동
          //뉴스 보여주는 페이지로 이동코드 적어주세요
        }
      })
      .catch((error) => alert(error));
  };

  render() {
    return (
      <div className="Signup">
        회원가입 페이지 입니다. <br />
        <form onSubmit={this.handleSubmit}>
        아이디:
          <input type="text" name="username" onChange={this.handleChange} />
          <br />
          비밀번호:
          <input type="password" name="password" onChange={this.handleChange} />
          <br />
          닉네임:
          <input type="text" name="first_name" onChange={this.handleChange} />
          <br />
          이메일:
          <input type="email" name="email" onChange={this.handleChange} />
          <br />
          
          <button type="submit">확인</button>
        </form>
      </div>
    );
  }
}
