import React, { Component } from "react";

// 회원가입
export default class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password1: "",
      password2: "",
      username:"",
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
      email:this.state.email,
      password: this.state.password1,
      password2: this.state.password2,
      username: this.state.username,
    };
    submitEvent.preventDefault();
    
    //여기에 회원정보 유효성 검사하는 코드 추가해야함

    let handleErrors = (response) => {
      if (!response.ok) {
        throw response;
      }
      return response;
    };

    fetch("http://localhost:8000/user/signup/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(handleErrors)
      .then((res) => res.json())
      .then((json) => {
        console.log("1");
        if (json.username && json.token) {
          console.log("2");
          //this.props.userHasAuthenticated(true,json.email, json.username, json.token);
          //회원가임후 메일 인증해야되니까 메일 인증하라고 알람 띄움
          alert("메일인증후에 서비스 이용이 가능합니다");
          
        }else{
          console.log("3");
          alert(json)
        }
        console.log("4");
      })
      .catch((error) => {})      
  };

  render() {
    return (
      <div className="Signup">
        회원가입 페이지 입니다. <br />
        <form onSubmit={this.handleSubmit}>
        이메일:
          <input type="email" name="email" onChange={this.handleChange} />
          <br />
          비밀번호:
          <input type="password" name="password1" onChange={this.handleChange} />
          <br />
          비밀번호 확인:
          <input type="password" name="password2" onChange={this.handleChange} />
          <br />
          닉네임:
          <input type="text" name="username" onChange={this.handleChange} />
          <br />
          
          
          <button type="submit">확인</button>
        </form>
      </div>
    );
  }
}
