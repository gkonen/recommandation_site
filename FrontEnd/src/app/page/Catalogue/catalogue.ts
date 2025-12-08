import {Component, signal} from '@angular/core';
import {CardFilm} from '../../component/card-film/card-film';
import {Movie} from '../../api/MovieModel';
import {Pagination} from '../../component/pagination/pagination';

@Component({
  selector: 'app-catalogue',
  imports: [
    CardFilm,
    Pagination
  ],
  templateUrl: './catalogue.html',
  styleUrl: './catalogue.scss',
})
export class Catalogue {
  readonly movies = signal<Movie>({
    id: 1,
    title: "The Matrix",
    year: 1999,
    rating: 4.7,
    genres: ["Sci-Fi", "Action"],
    tags: ["must-watch"]
  });
}
