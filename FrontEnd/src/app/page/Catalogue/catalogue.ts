import {Component, inject, signal} from '@angular/core';
import {CardFilm} from '../../component/card-film/card-film';
import {Movie} from '../../api/MovieModel';
import {Pagination} from '../../component/pagination/pagination';
import {HttpService} from '../../api/service/http-service';

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
  private httpService = inject(HttpService);

  readonly movies = signal<Movie[]>([{
    id: 1,
    title: "The Matrix",
    year: 1999,
    rating: 4.7,
    genres: ["Sci-Fi", "Action"],
    tags: ["must-watch"]
  }]);

  ngOnInit() {
    this.loadMovies();
  }

  loadMovies() {
    this.httpService.get_movies().subscribe((movies : Movie[]) => {
      console.log(movies);
      this.movies.set(movies);
    })
  }

  readonly currentPage = signal<number>(1);

  protected onPageChange($event: number) {
    this.currentPage.set($event);
  }
}
