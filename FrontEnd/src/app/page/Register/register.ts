import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RegistrationService } from '../../api/service/registration-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [FormsModule],
  templateUrl: './register.html',
  styleUrl: './register.scss',
})
export class Register {
  private regService = inject(RegistrationService);
  private router = inject(Router);

  username: string = '';
  password: string = '';
  errorMessage: string = '';
  isLoading: boolean = false;

  async onSubmit() {
    if (!this.username || !this.password) {
      this.errorMessage = 'Please fill in both fields';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.regService.register(this.username, this.password).subscribe({
      next: (response) => {
        console.log('Registration successful', response);
        // Navigate to login page after successful registration
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Registration failed', error);
        this.errorMessage = error.error?.message || 'Registration failed. Please try again.';
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }
}
