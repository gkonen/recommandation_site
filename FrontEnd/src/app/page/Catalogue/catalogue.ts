import {Component, inject, OnInit, signal} from '@angular/core';
import {CardMovie} from '../../component/card-movie/card-movie';
import {Movie} from '../../api/MovieModel';
import {Pagination} from '../../component/pagination/pagination';
import {MovieService} from '../../api/service/movie-service';
import {SliderMovie} from '../../component/slider-movie/slider-movie';
import {SearchFilter} from '../../component/search-filter/search-filter';
import {MovieFilter} from '../../component/search-filter/MovieFilter';
import {ResponseCatalogue} from '../../api/ResponseMovieModel';
import {PaginationDetail} from '../../api/service/PaginationDetailModel';

type CatalogueState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'view' }
  | { status: 'no-result' };

@Component({
  selector: 'app-catalogue',
  imports: [
    CardMovie,
    Pagination,
    SliderMovie,
    SearchFilter
  ],
  templateUrl: './catalogue.html',
  styleUrl: './catalogue.scss',
})
export class Catalogue implements OnInit {
  private httpService = inject(MovieService);
  private searchFilter = signal<MovieFilter | null>(null);

  readonly state = signal<CatalogueState>({ status: 'idle' });

  readonly catalogMovie = signal<Movie[]>([]);
  readonly genreMovie = signal<string[]>([]);
  readonly recommendMovie = signal<Movie[]>([]);
  readonly pagination = signal<PaginationDetail>({
    has_next: false,
    has_prev: false,
    page: 1,
    per_page: 50,
    total: 1,
    total_pages: 1
  });

  ngOnInit() {
    this.loadMovies();
    this.loadGenre();
  }

  loadGenre() {
    this.httpService.get_all_genres().subscribe((genres) => {
      this.genreMovie.set(genres);
    })
  }

  loadMovies(page: number= 1) {
    this.state.set({ status: 'loading' });
    this.httpService.get_movies(page).subscribe({
      // When we receive a response, we update the state and set our catalogue
      next: (response : ResponseCatalogue) => {
        this.catalogMovie.set(response.movies);
        this.pagination.set(response.pagination);
      },
      // When we receive an error
      error: () => {
        this.state.set({ status: 'no-result' });
      },
      // When the request is complete
      complete: () => {
        if(this.catalogMovie().length == 0) {
          this.state.set({ status: 'no-result' });
        } else {
          this.state.set({ status: 'view' });
        }
      }
    })
  }

  protected onSearchFilter(filters: any, page: number = 1) {
    this.state.set({ status: 'loading' });
    this.httpService.get_movie_by_filter(filters, page).subscribe({
      next: (response : ResponseCatalogue) => {
        this.searchFilter.set(filters);
        this.catalogMovie.set(response.movies);
        this.pagination.set(response.pagination);
      },
      error: () => {
        this.state.set({ status: 'no-result' });
      },
      complete: () => {
        if(this.catalogMovie().length == 0) {
          this.state.set({ status: 'no-result' });
        } else {
          this.state.set({ status: 'view' });
        }
      }
    })
  }

  protected onPageChange($event: number) {
    if (this.searchFilter() != null) {
      this.onSearchFilter(this.searchFilter(), $event)
    } else {
      this.loadMovies($event);
    }
  }
}
