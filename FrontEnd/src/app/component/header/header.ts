import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../api/service/auth-service';

@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.html',
  styleUrl: './header.scss',
})
export class Header {
  private authService = inject(AuthService);
  private router: Router = inject(Router);

  readonly connectedState = this.authService.isAuthenticated;

  async onConnectClick() {
    console.log('Connection state:', this.connectedState());
    if (this.connectedState()) {
      this.authService.logout();
      await this.router.navigate(['/']);
    } else {
      await this.router.navigate(['login']);
    }
  }

  async onRegisterClick() {
    console.log('Connection state:', this.connectedState());
    console.log('User data:', this.authService.getUser());
    if (this.connectedState()) {
      const user = this.authService.getUser();
      await this.router.navigate(['/profile'], {
        queryParams: { id: user.id, username: user.username, logged: user.logged },
      });
    } else {
      await this.router.navigate(['/register']);
    }
  }

  async onTitleClick() {
    await this.router.navigate(['/']);
  }
}
