import { Component, OnInit } from '@angular/core';
import { Voting } from '../voting.model';
import { DataService } from '../data.service';

@Component({
  selector: 'app-voting-list',
  templateUrl: './voting-list.component.html',
  styleUrls: ['./voting-list.component.css']
})
export class VotingListComponent implements OnInit {

  votings: Voting[];


  constructor(private dataService: DataService) {}

  ngOnInit() {
    return this.dataService.getVotings()
    .subscribe(data => this.votings = data);

  }

}
