import { Injectable, signal } from '@angular/core';
import { HttpService } from '../http/http.service';
import { ResAction } from '@jaslay/http';

interface Vote {
  id: string;
  date: string;
  userId: string;
  vote: string;
  pseudo: string;
}

@Injectable()
export class VoteService {
  votes = signal<Vote[]>([]);

  async loadVotes() {
    const response: ResAction = await this.httpService.quickHttp.get(
      'api/votes/'
    );
    const payload = response.payload as Vote[];
    this.votes.set(payload);
  }

  constructor(private readonly httpService: HttpService) {}
}
