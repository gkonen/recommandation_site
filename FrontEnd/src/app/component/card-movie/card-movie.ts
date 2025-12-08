import {Component, input} from '@angular/core';
import {Movie} from '../../api/MovieModel';



@Component({
  selector: 'app-card-movie',
  imports: [],
  templateUrl: './card-movie.html',
  styleUrl: './card-movie.scss',
})
export class CardMovie {

  readonly movie = input.required<Movie>()

}
