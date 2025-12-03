import {Component, inject, signal} from '@angular/core';
import {AuthService} from '../../api/auth-service';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  private authService = inject(AuthService);
  readonly isAuthenticated = signal(this.authService.isAuthenticated());

  ngOnChanges() {
    this.isAuthenticated.set(this.authService.isAuthenticated());
  }

}
