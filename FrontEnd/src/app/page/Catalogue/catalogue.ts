import {Component, effect, inject, OnInit, signal} from '@angular/core';
import {CardMovie} from '../../component/card-movie/card-movie';
import {Movie} from '../../api/MovieModel';
import {Pagination} from '../../component/pagination/pagination';
import {MovieService} from '../../api/service/movie-service';
import {SliderMovie} from '../../component/slider-movie/slider-movie';
import {SearchFilter} from '../../component/search-filter/search-filter';
import {MovieFilter} from '../../component/search-filter/MovieFilter';
import {ResponseCatalogue} from '../../api/ResponseMovieModel';
import {PaginationDetail} from '../../api/service/PaginationDetailModel';
import {PopupModal} from '../../component/popup-modal/popup-modal';
import {AuthService} from '../../api/service/auth-service';
import {Subscription} from 'rxjs';

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
    SearchFilter,
    PopupModal
  ],
  templateUrl: './catalogue.html',
  styleUrl: './catalogue.scss',
})
export class Catalogue implements OnInit {
  private movieService = inject(MovieService);
  private authService = inject(AuthService);

  private searchFilter = signal<MovieFilter | null>(null);

  readonly state = signal<CatalogueState>({ status: 'idle' });
  readonly isAuthenticated = this.authService.isAuthenticated;

  readonly isPopupVisible = signal<boolean>(false);
  readonly selectedMovie = signal<Movie | null>(null);

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

  constructor() {
    // effect permit to react directly when the signal change
    // the on cleanup permit unsubscribing when the component is destroyed to avoid memory leakage
    effect((onCleanup) => {
      let subscription: Subscription | null = null
      if(this.isAuthenticated()) {
        subscription = this.loadRecommendation(this.authService.getUser().id);
      } else {
        this.recommendMovie.set([]);
      }
      onCleanup(() => {
        subscription?.unsubscribe();
      })
    })
  }

  ngOnInit() {
    this.loadMovies();
    this.loadGenre();
  }

  loadGenre() {
    this.movieService.get_all_genres().subscribe((genres) => {
      this.genreMovie.set(genres);
    })
  }

  loadMovies(page: number= 1) {
    this.state.set({ status: 'loading' });
    this.movieService.get_movies(page).subscribe({
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

  loadRecommendation(userId: number) {
    return this.movieService.get_recommended_movies(userId)
      .subscribe({
        next: (response) => {
          this.recommendMovie.set(response.movies);
        },
        error: () => {
          console.error('Error while fetching recommendations');
        },
        complete: () => {
          console.log("All is fine")
        }
      });
  }

  openPopup(movie: Movie) {
    if( this.authService.isAuthenticated() ) {
      this.isPopupVisible.set(true);
      this.selectedMovie.set(movie);
    }
  }

  confirmPopup($event: number) {
    const user = this.authService.getUser();
    console.log(user);
    if (user.id !== -1) {
      this.movieService.post_new_rating(this.selectedMovie()!.id, user.id, $event)
        .subscribe({
          next: (response) => {
            console.log('Rating envoyé avec succès:', response);
            this.closePopup();
          },
          error: (error) => {
            console.error('Erreur lors de l\'envoi du rating:', error);
          }
        });
    }
  }

  closePopup() {
    this.isPopupVisible.set(false);
  }

  protected onSearchFilter(filters: any, page: number = 1) {
    this.state.set({ status: 'loading' });
    this.movieService.get_movie_by_filter(filters, page).subscribe({
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
