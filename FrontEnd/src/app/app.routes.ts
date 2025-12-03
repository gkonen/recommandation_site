import { Routes } from '@angular/router';
import {Home} from './page/Home/home';
import {Catalogue} from './page/Catalogue/catalogue';
import {NotFound} from './page/Not-found/not-found';
import {FilmDetail} from './page/Film/film-detail';
import {UserProfil} from './page/Profil/user-profil';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'catalogue', component: Catalogue},
  { path: 'film/:id', component: FilmDetail },
  { path: 'profile/:id', component: UserProfil},
  { path: '**', component: NotFound }
];
