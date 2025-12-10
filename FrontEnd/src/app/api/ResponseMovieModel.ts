import {Movie} from './MovieModel';
import {PaginationDetail} from './service/PaginationDetailModel';

export interface ResponseCatalogue {
  movies: Movie[];
  pagination: PaginationDetail
}
