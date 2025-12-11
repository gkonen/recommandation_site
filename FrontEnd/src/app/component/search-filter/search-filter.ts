import {Component, inject, input, output} from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {MovieFilter} from './MovieFilter';

@Component({
  selector: 'app-search-filter',
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './search-filter.html',
  styleUrl: './search-filter.scss',
})
export class SearchFilter {
  private fb = inject(FormBuilder);

  availableGenres = input.required<string[]>()
  isLoading = input.required<boolean>()

  onSearchFilter = output<MovieFilter>()

  protected filterForm : FormGroup = this.fb.group({
    title: this.fb.control<string | null>('', Validators.minLength(3)),
    genre_name:  this.fb.control<string | null>(''),
    year:  this.fb.control<string | null>('')
  });

  onSubmit() {
    const { title, genre_name, year } = this.filterForm.value;
    const filters : MovieFilter = {
      ...(title && { title }),
      ...(genre_name && { genre_name: genre_name }),
      ...(year && { year: Number(year) })
    };
    console.log(filters);
    this.onSearchFilter.emit(filters);
  }

}
