import { Component, input } from '@angular/core';
import { Vote } from '../../services/vote/vote.service';

@Component({
  selector: 'app-vote',
  standalone: true,
  imports: [],
  templateUrl: './vote.component.html',
  styleUrl: './vote.component.css',
})
export class VoteComponent {
  votes = input<Vote[]>();
}
