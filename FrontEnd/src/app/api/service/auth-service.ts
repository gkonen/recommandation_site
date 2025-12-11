import {computed, inject, Injectable, signal} from '@angular/core';
import {UserService} from './user-service';
import {DefaultUser, UserModel} from '../UserModel';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private userService = inject(UserService);
  readonly user = signal<UserModel>(DefaultUser());
  readonly isAuthenticated = computed(() => this.user().logged);

  login(username: string, password: string) {
    const user = this.userService.connect(username, password);
    // Change this to the actual user
    this.user.set(user);
  }

  logout() {
    this.user.set(DefaultUser());
  }

  getUser() : UserModel {
    return this.user();
  }

}
