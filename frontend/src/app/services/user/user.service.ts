import { Injectable, signal } from '@angular/core';
import { HttpService } from '../http/http.service';
import { ResAction } from '@jaslay/http';

interface User {
  id: string;
  pseudo: string;
  email: string;
}

@Injectable()
export class UserService {
  currentUser = signal<User | undefined>(undefined);

  async createNewUser(pseudo: string, email: string): Promise<ResAction> {
    const response: ResAction = await this.httpService.quickHttp.post(
      'api/user',
      {
        pseudo: pseudo,
        email: email,
      }
    );
    return response;
  }
  constructor(private readonly httpService: HttpService) {}
}
