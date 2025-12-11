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

  async onSubmit() {}
}
