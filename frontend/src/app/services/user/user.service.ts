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
  constructor(private readonly httpService: HttpService) {}

  async createNewUser(pseudo: string, email: string): Promise<void> {
    const response: ResAction = await this.httpService.quickHttp.post(
      'api/user',
      {
        pseudo: pseudo,
        email: email,
      }
    );
    const payload = response.payload as User;
    if (response.status === 'Success') {
      this.setUser(payload.id, payload.pseudo, payload.email);
    }
  }

  async login(email: string): Promise<void> {
    const response: ResAction = await this.httpService.quickHttp.get(
      'api/user',
      {
        email: email,
      }
    );
    const payload = response.payload as User;
    if (response.status === 'Success') {
      this.setUser(payload.id, payload.pseudo, payload.email);
    }
  }

  logout(): void {
    this.currentUser.set(undefined);
  }

  private setUser(id: string, pseudo: string, email: string): void {
    this.currentUser.set({
      id: id,
      pseudo: pseudo,
      email: email,
    });
  }
}
