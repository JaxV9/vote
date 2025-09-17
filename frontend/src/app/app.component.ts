import { Component, effect, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { VoteService } from './services/vote/vote.service';
import { HttpService } from './services/http/http.service';
import { UserService } from './services/user/user.service';
import { HelloUserComponent } from './components/hello-user/hello-user.component';
import { VoteComponent } from './components/vote/vote.component';
import { ResultsComponent } from './components/results/results.component';
import { ChoiceComponent } from './components/vote/choice/choice.component';
import { SignPopComponent } from './components/sign-pop/sign-pop.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    HelloUserComponent,
    VoteComponent,
    ResultsComponent,
    ChoiceComponent,
    SignPopComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [HttpService, VoteService, UserService],
})
export class AppComponent implements OnInit {
  constructor(
    public readonly voteService: VoteService,
    public readonly userService: UserService
  ) {}

  userIsLogin(): boolean {
    return this.userService.currentUser() !== undefined ? true : false;
  }

  vote(vote: string): void {
    this.voteService.vote(vote);
  }

  logout(): void {
    this.userService.logout();
    this.voteService.hasAlreadyVoted.set(false);
  }

  ngOnInit(): void {
    this.voteService.loadVotes();
  }
}
