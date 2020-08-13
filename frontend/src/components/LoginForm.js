import React from 'react';
import { Button, FormGroup, FormControl } from "react-bootstrap";

// presentational component, only a stateless function
// gets props by destructuring the props object
// note that the input fields use the props to render their value attribute
const LoginForm = ({
    username, password, 
    handleChangeUsername,  
    handleChangePassword, 
    handleSubmit,
    validate,
  }) => {
    return (
      <div className="Login">
        <form onSubmit={handleSubmit}>
          <FormGroup controlId="username" >
            <FormControl
              autoFocus
              value={username}
              onChange={handleChangeUsername}
            />
          </FormGroup>
          <FormGroup controlId="password">

            <FormControl
              value={password}
              onChange={handleChangePassword}
              type="password"
            />
          </FormGroup>
          <Button
            block
            //disabled={!validate(username, password)}
            type="submit"
          >
            Login
          </Button>              
        </form>

      </div>
    );
  }

export default LoginForm;