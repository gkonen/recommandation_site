import {Component, input} from '@angular/core';
import {Movie} from '../../api/MovieModel';



@Component({
  selector: 'app-card-film',
  imports: [],
  templateUrl: './card-film.html',
  styleUrl: './card-film.scss',
})
export class CardFilm {

  readonly movie = input.required<Movie>()



}
