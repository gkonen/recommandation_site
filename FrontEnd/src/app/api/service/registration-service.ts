import { inject, Injectable, signal } from '@angular/core';
import { UserService } from './user-service';

@Injectable({
  providedIn: 'root',
})
export class RegistrationService {
  private userService = inject(UserService);

  register(username: string, password: string) {
    return this.userService.register(username, password);
  }
}
