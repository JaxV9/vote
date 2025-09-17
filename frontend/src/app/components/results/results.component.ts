import { Component, input } from '@angular/core';
import { Vote } from '../../services/vote/vote.service';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css',
})
export class ResultsComponent {
  votes = input<Vote[]>();
}
