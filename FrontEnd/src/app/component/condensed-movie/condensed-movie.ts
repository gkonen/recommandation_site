import {Component, input} from '@angular/core';
import {MovieData} from '../../api/UserDataModel';

type category = {id : number, name : string}

@Component({
  selector: 'app-condensed-movie',
  imports: [],
  templateUrl: './condensed-movie.html',
  styleUrl: './condensed-movie.scss',
})
export class CondensedMovie {
  readonly movie = input.required<MovieData>()
  readonly category = input.required<category>()
}
