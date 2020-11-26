import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import { DataService } from '../data.service';
import { Voting, Option } from '../voting.model';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-voting-form',
  templateUrl: './voting-form.component.html',
  styleUrls: ['./voting-form.component.css'],
  providers: [LoginComponent]
})
export class VotingFormComponent {
  votingForm: FormGroup;
  voting: Voting;
  optionsData: Option[] = [];
  isSubmitted = false;
  vointgId: number;
  token: string;
  userId: number;
  selected: number;

  constructor(private formBuilder: FormBuilder, public dataService: DataService, private loginComponent: LoginComponent) {
    this.votingForm = this.formBuilder.group({
      options: new FormArray([])
    });

    this.dataService.getVotings()
    .subscribe(data => {this.voting = data[0];
                        for (const op of this.voting.question.options) {
        this.optionsData.push(op);
      }
                        this.addCheckboxes();
                        this.vointgId = data[0].id;
    } );


    this.dataService.currentUserId.subscribe(data => this.userId = data);
    this.dataService.currentToken.subscribe(data => this.token = data);
  }


  private addCheckboxes() {
    this.optionsData.forEach((o, i) => {
    const control = new FormControl(); // if first item set to true, else false
    (this.votingForm.controls.options as FormArray).push(control);
    });
    }

  onSubmit() {
    console.log('current token: ' + this.token, 'current userId: ' + this.userId , 'current votingId: ' +  this.vointgId);
    const selectedOptions = this.votingForm.value.options
  .map((v, i) => v ? this.optionsData[i].number : null)
  .filter(v => v !== null);

    this.selected = selectedOptions[0];

    console.log('selected option: ' + this.selected);
  }

}
