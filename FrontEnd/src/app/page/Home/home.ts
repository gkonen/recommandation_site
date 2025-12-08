import {Component, inject} from '@angular/core';
import {AuthService} from '../../api/service/auth-service';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  private authService = inject(AuthService);
  readonly isAuthenticated = this.authService.isAuthenticated;

}
