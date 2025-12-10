import {Component, inject, OnInit, signal} from '@angular/core';
import {CardMovie} from '../../component/card-movie/card-movie';
import {Movie} from '../../api/MovieModel';
import {Pagination} from '../../component/pagination/pagination';
import {HttpService} from '../../api/service/http-service';
import {SliderMovie} from '../../component/slider-movie/slider-movie';

@Component({
  selector: 'app-catalogue',
  imports: [
    CardMovie,
    Pagination,
    SliderMovie
  ],
  templateUrl: './catalogue.html',
  styleUrl: './catalogue.scss',
})
export class Catalogue implements OnInit {
  private httpService = inject(HttpService);

  readonly catalogMovie = signal<Movie[]>([]);
  readonly recommendMovie = signal<Movie[]>([]);
  readonly currentPage = signal<number>(1);

  ngOnInit() {
    this.loadMovies();
  }

  loadMovies(page: number= 1) {
    this.httpService.get_movies(page).subscribe((movies : Movie[]) => {
      console.log(movies);
      this.catalogMovie.set(movies);
      //this.recommendMovie.set(movies);
      this.currentPage.set(page);
    })
  }

  protected onPageChange($event: number) {
    this.loadMovies($event);
  }

}
