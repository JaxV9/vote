import { Component, effect, OnInit } from '@angular/core';
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
  constructor(
    public readonly voteService: VoteService,
    public readonly userService: UserService
  ) {}

  userIsLogin(): boolean {
    return this.userService.currentUser() === undefined ? true : false;
  }

  ngOnInit(): void {
    this.voteService.loadVotes();
  }
}
