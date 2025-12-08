import {Component, inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {AuthService} from '../../api/service/auth-service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-Login',
  imports: [
    FormsModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private authService = inject(AuthService);
  private router = inject(Router);

  username: string = '';
  password: string = '';

  async onSubmit() {
    console.log('Form submitted:', this.username, this.password);
    console.log('response:', this.authService.login(this.username, this.password));
    await this.router.navigate(['/']);
  }

}
