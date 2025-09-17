import { Component, input } from '@angular/core';

@Component({
  selector: 'app-hello-user',
  standalone: true,
  imports: [],
  templateUrl: './hello-user.component.html',
  styleUrl: './hello-user.component.css',
})
export class HelloUserComponent {
  display = input<boolean>();
  pseudo = input<string>();
}
