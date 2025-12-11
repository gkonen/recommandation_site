import {Component, input} from '@angular/core';
import {Movie} from '../../api/MovieModel';

@Component({
  selector: 'app-condensed-movie',
  imports: [],
  templateUrl: './condensed-movie.html',
  styleUrl: './condensed-movie.scss',
})
export class CondensedMovie {
  readonly movie = input.required<Movie>()
}
