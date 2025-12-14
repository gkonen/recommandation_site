import { Routes } from '@angular/router';
import { Home } from './page/Home/home';
import { Catalogue } from './page/Catalogue/catalogue';
import { NotFound } from './page/Not-found/not-found';
import { FilmDetail } from './page/Film/film-detail';
import { UserProfile } from './page/Profil/user-profile';
import { Login } from './page/Login/login';
import { Register } from './page/Register/register';

export const routes: Routes = [
  { path: '', redirectTo: 'catalogue', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'catalogue', component: Catalogue },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'film/:id', component: FilmDetail },
  { path: 'profile', component: UserProfile },
  { path: '**', component: NotFound },
];
