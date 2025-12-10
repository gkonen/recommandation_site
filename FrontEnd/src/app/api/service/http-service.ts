import {inject, Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {map} from 'rxjs';
import {ResponseMovie} from '../ResponseMovieModel';
import {MovieFilter} from '../../component/search-filter/MovieFilter';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private url = 'http://localhost:5000/';
  private http = inject(HttpClient);

  get_movies(page: number = 1) {
    return this.http.get<ResponseMovie>(this.url + 'movies', {
      params: {page: page.toString()}
    }).pipe(
      map(response =>
        response.movies.map(movie => ({
            id: movie.id,
            title: movie.title,
            year: movie.year,
            score: Math.round(movie.score * 10)/20,
            genres: movie.genres,
            tags: movie.tags
          }))
      )
    );
  }

  get_movie_by_filter(filter: MovieFilter, page: number = 1) {
    return this.http.get<ResponseMovie>(this.url + 'movies', {
      params: { ...filter, page: page.toString()}
    }).pipe(
      map(response =>
        response.movies.map(movie => ({
          id: movie.id,
          title: movie.title,
          year: movie.year,
          score: Math.round(movie.score * 10)/20,
          genres: movie.genres,
          tags: movie.tags
        }))
      )
    );
  }

}
