import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VotingListComponent } from './voting-list.component';

describe('VotingListComponent', () => {
  let component: VotingListComponent;
  let fixture: ComponentFixture<VotingListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VotingListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VotingListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // it('should create', () => {
  //   expect(component).toBeTruthy();
  // });
});
