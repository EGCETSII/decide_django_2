import { Component, OnInit } from '@angular/core';
import { Voting } from './voting.model';
import { DataService } from './data.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  votings: Voting[];
  //showVotings: whether to show the component voting-list
  showVotings: boolean;
  //showVoting: whether to show the component voting-form
  showVoting: boolean;
  //showLogin: whether to show the component login
  showLogin: boolean;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    //Retrieve global variables from dataService as observables
    this.dataService.getShowVotings().subscribe(data => this.showVotings = data);
    this.dataService.getShowVoting().subscribe(data => this.showVoting = data);
    this.dataService.getShowLogin().subscribe(data => this.showLogin = data);

    return this.dataService.getVotings()
    .subscribe(data => this.votings = data);

  }

}
