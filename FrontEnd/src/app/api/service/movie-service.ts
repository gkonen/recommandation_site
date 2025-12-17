import {inject, Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {map} from 'rxjs';
import { ResponseCatalogue } from '../ResponseMovieModel';
import { MovieFilter } from '../../component/search-filter/MovieFilter';
import {ResponseGenre} from '../GenreModel';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private url = 'http://localhost:5000/';
  private http = inject(HttpClient);

  get_movies(page: number = 1) {
    return this.http.get<ResponseCatalogue>(this.url + 'movies', {
      params: {page: page.toString()}
    }).pipe(
      map(response => ({
        movies: response.movies.map(movie => ({
          id: movie.id,
          title: movie.title,
          year: movie.year,
          score: Math.round(movie.score * 10)/20,
          genres: movie.genres,
          tags: movie.tags
          })
        ),
        pagination : response.pagination
      }))
    );
  }

  get_movie_by_filter(filter: MovieFilter, page: number = 1) {
    return this.http.get<ResponseCatalogue>(this.url + 'movies', {
      params: { ...filter, page: page.toString()}
    }).pipe(
      map(response => ({
        movies: response.movies.map(movie => ({
          id: movie.id,
          title: movie.title,
          year: movie.year,
          score: Math.round(movie.score * 10)/20,
          genres: movie.genres,
          tags: movie.tags
          })
        ),
        pagination : response.pagination
      }))
    );
  }

  get_recommended_movies(user_id: number) {
    // TODO : insert real path and test inside catalog
    return this.http.get<ResponseCatalogue>(this.url + 'recommendations/' + user_id).pipe(
      map(response => ({
        movies: response.movies.map(movie => ({
          id: movie.id,
          title: movie.title,
          year: movie.year,
          score: Math.round(movie.score * 10)/20,
          genres: movie.genres,
          tags: movie.tags
        }))
      }))
    )
  }

  get_all_genres() {
    return this.http.get<ResponseGenre>(this.url + 'genres').pipe(
      map(response => response.genres)
    );
  }

  post_new_rating(movie_id: number, user_id: number, rating: number) {
    console.log("send server : ", movie_id, user_id, rating );
    return this.http.post<{ "user_id": number, "rating": number}>(
      this.url + 'movies/rating/' + movie_id,
      {
        user_id: user_id,
        rating: rating
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      });
  }

}
