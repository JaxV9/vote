import { Injectable, signal } from '@angular/core';
import { HttpService } from '../http/http.service';
import { ResAction } from '@jaslay/http';
import { UserService } from '../user/user.service';

interface Vote {
  id: string;
  date: string;
  userId: string;
  vote: string;
  pseudo: string;
}

interface VotePayload {
  userId: string;
  vote: string;
}

@Injectable()
export class VoteService {
  votes = signal<Vote[]>([]);

  async loadVotes(): Promise<void> {
    const response: ResAction = await this.httpService.quickHttp.get(
      'api/votes/'
    );
    const payload = response.payload as Vote[];
    this.votes.set(payload);
  }

  async vote(vote: string): Promise<void> {
    const userIdValue = this.userService.currentUser()?.id;

    if (userIdValue === undefined) {
      return;
    }
    const payload: VotePayload = {
      userId: userIdValue,
      vote: vote,
    };
    const response: ResAction = await this.httpService.quickHttp.post(
      'api/vote',
      payload
    );

    if (response.status === 'Success') {
      this.loadVotes();
    }
  }

  constructor(
    private readonly httpService: HttpService,
    private readonly userService: UserService
  ) {}
}
