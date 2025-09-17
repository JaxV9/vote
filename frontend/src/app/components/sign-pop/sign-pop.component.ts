import { Component, input, signal } from '@angular/core';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-sign-pop',
  standalone: true,
  imports: [],
  templateUrl: './sign-pop.component.html',
  styleUrl: './sign-pop.component.css',
})
export class SignPopComponent {
  display = input<boolean>();
  signUp = signal<boolean>(false);

  constructor(public readonly userService: UserService) {}

  toggleSignIn(): void {
    this.signUp.update((prev) => !prev);
  }

  confirmSignUp(email: string, pseudo: string): void {
    this.userService.createNewUser(pseudo, email);
  }

  confirmSignIn(email: string): void {
    this.userService.login(email);
  }
}
