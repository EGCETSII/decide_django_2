import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  registerForm: FormGroup;
  username = '';
  password = '';
  buttonDisabled: boolean;
  submitted = false;
  //showVotings: whether to show the component voting-list
  showVotings: boolean;
  //showVoting: whether to show the component voting-form
  showVoting: boolean;
  //showLogin: whether to show the component login
  showLogin: boolean;


  constructor(private formBuilder: FormBuilder, public dataService: DataService) {
  }

  ngOnInit() {
    this.buttonDisabled = false;
    this.registerForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  async onSubmit() {
    this.submitted = true;

    if (this.registerForm.invalid) {
      return;
    }

    const tokenR = await this.dataService.logUser(this.registerForm.get('username').value, this.registerForm.get('password').value);
    const userR = await this.dataService.getUserId(tokenR);

    this.dataService.changeToken(tokenR.token);
    this.dataService.changeUserId(userR.id);

    //If the token is not null, the user logged in correctly.
    if (tokenR.token != null) {
      //Since the user logged in correctly, show the listing of all available votings.
      //In a future version, only the votings for which the user is part of the census should be shown.
      this.dataService.changeShowVotings(true);
      //Since the user logged in correctly, show the voting form
      //In a future version, the user should select which voting he wants to participate in and that form should be shown.
      this.dataService.changeShowVoting(true);
      //Since the user logged in correctly, hide the login component
      this.dataService.changeShowLogin(false);
    }

    console.log('the username: ' + this.registerForm.get('username').value);
    console.log('the password: ' + this.registerForm.get('password').value);
    console.log('the token: ' + tokenR.token);
    console.log('my user id: ' + userR.id );
  }

}


