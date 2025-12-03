import {Component, inject, signal} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from '../../api/auth-service';

@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.html',
  styleUrl: './header.scss',
})
export class Header {
  private authService = inject(AuthService);
  readonly connectedState = signal(this.authService.isAuthenticated());
  private router: Router = inject(Router);

    async onConnectClick() {
      if (this.connectedState()) {
        this.authService.logout();
        await this.router.navigate(['/']);
      } else {
        this.connectedState.set(!this.connectedState())
        await this.router.navigate(['login']);
      }
    }

}
