import { Component, effect, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { VoteService } from './services/vote/vote.service';
import { HttpService } from './services/http/http.service';
import { UserService } from './services/user/user.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [HttpService, VoteService, UserService],
})
export class AppComponent implements OnInit {
  signUp = signal<boolean>(false);

  constructor(
    public readonly voteService: VoteService,
    public readonly userService: UserService
  ) {}

  userIsLogin(): boolean {
    return this.userService.currentUser() === undefined ? true : false;
  }

  toggleSignIn(): void {
    this.signUp.update((prev) => !prev);
  }

  confirmSignUp(email: string, pseudo: string): void {
    this.userService.createNewUser(pseudo, email);
    console.log(email, pseudo);
  }

  confirmSignIn(email: string): void {
    this.userService.login(email);
  }

  ngOnInit(): void {
    this.confirmSignIn('layanj.pro@gmail.com');
    this.voteService.loadVotes();
  }
}
