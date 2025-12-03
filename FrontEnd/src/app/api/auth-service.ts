import {Injectable, signal} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  readonly isAuthenticated = signal(false);

  login(username: string, password: string) {
    this.isAuthenticated.set(true);
    return true
  }

  logout() {
    this.isAuthenticated.set(false);
  }

}
