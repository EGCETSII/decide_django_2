import { User, Voting, Token, Auth, PubKey } from './voting.model';

describe('Model creation', () => {

  it('should create an instance of User', () => {
    expect(new User()).toBeTruthy();
  });

  it('should create an instance of Voting', () => {
    expect(new Voting()).toBeTruthy();
  });

  it('should create an instance of Token', () => {
    expect(new Token()).toBeTruthy();
  });

  it('should create an instance of Auth', () => {
    expect(new Auth()).toBeTruthy();
  });

  it('should create an instance of Pubkey', () => {
    expect(new PubKey()).toBeTruthy();
  });
});
