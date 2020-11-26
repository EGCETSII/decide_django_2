export class Voting {
    id: number;
    name: string;
    desc: string;
    question: Question;
    start_date: Date;
    end_date: Date;
    pub_key: PubKey;
    auths: Auth[];
    tally: any;
    postproc: any;
}

export class Auth {
  name: string;
  url: string;
  me: boolean;
}

export class PubKey {
  p: number;
  g: number;
  y: number;
}

export class Question {
  desc: string;
  options: Option[];
}

export class Option {
  number: number;
  option: string;
}

export class Token {
  token: string;
}

export class User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_staff: boolean;
}
